"""Offline replay against hash-pinned historical splice inputs and controls.

Requires an already provisioned licensed runtime. No weights or patient inputs
are distributed. Predictions are not measured RNA or proof of protein function.
"""
import argparse
import contextlib
import importlib.metadata
import json
import os
from pathlib import Path
import time
from scripts.portable_phase_snapshot import sha
from scripts.local_lead_splice import parse_score, gene_score
from scripts.splice_transcript_controls import donor_position


def compare_predictions(expected, actual):
    if len(expected)!=len(actual):return False
    return all(a==b for a,b in zip(expected,actual))


def run(prior_path, prior_hash, transcript_path, transcript_hash, output):
    if output.exists():raise ValueError('fresh output required')
    os.umask(0o077)
    os.environ.update(CUDA_VISIBLE_DEVICES='-1',TF_CPP_MIN_LOG_LEVEL='2',TF_NUM_INTEROP_THREADS='1',TF_NUM_INTRAOP_THREADS='2',OMP_NUM_THREADS='2')
    started=time.monotonic();pins={};size=0
    def check(path, expected):
        nonlocal size
        path=Path(path)
        if path.is_symlink() or not path.is_file():raise ValueError('input path')
        if path not in pins:size+=path.stat().st_size
        if size>8_000_000_000 or time.monotonic()-started>300:raise ValueError('splice budget')
        if sha(path)!=expected:raise ValueError('input drift')
        pins[path]=expected
    check(prior_path,prior_hash);check(transcript_path,transcript_hash)
    if prior_path.stat().st_size>8_000_000 or transcript_path.stat().st_size>8_000_000:raise ValueError('metadata cap')
    prior=json.loads(prior_path.read_text());transcripts=json.loads(transcript_path.read_text())
    if transcripts['prior_splice_sha256']!=prior_hash:raise ValueError('prior lineage')
    if not 1<=len(prior['rows'])<=10:raise ValueError('lead cap')
    for path,h in prior['input_hashes'].items():check(Path(path),h)
    refpaths=[Path(p) for p in prior['input_hashes'] if p.endswith('.fa')]
    if len(refpaths)!=1:raise ValueError('reference ambiguity')
    ref=refpaths[0];annotation=transcript_path.parent/'preferred-transcripts.tsv'
    check(annotation,transcripts['custom_annotation_sha256'])
    output.mkdir(mode=0o700);(output/'INCOMPLETE').touch()
    with (output/'private.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
        import tensorflow as tf
        import pysam
        import spliceai
        from spliceai.utils import Annotator,get_delta_scores
        tf.config.set_visible_devices([],'GPU')
        versions={name:importlib.metadata.version(name) for name in prior['versions']}
        if versions!=prior['versions']:raise ValueError('runtime version mismatch')
        package=Path(spliceai.__file__).parent
        for path in [package/'utils.py',package/'annotations/grch38.txt',*[package/f'models/spliceai{i}.h5' for i in range(1,6)]]:
            if str(path) not in prior['input_hashes']:raise ValueError('imported model resource not pinned')
            check(path,prior['input_hashes'][str(path)])
        ann=Annotator(str(ref),'grch38');custom=Annotator(str(ref),str(annotation))
        header=pysam.VariantHeader()
        for c in {r['key'][0] for r in prior['rows']}:header.contigs.add(c)
        rows=[];sensitivity=[];nulls=0
        for old in prior['rows']:
            c,pos,r,a=old['key'];record=header.new_record(contig=c,start=pos-1,alleles=(r,a))
            raw=[parse_score(x) for x in get_delta_scores(record,ann,500,0)]
            masked=[parse_score(x) for x in get_delta_scores(record,ann,500,1)]
            rows.append(dict(key=old['key'],raw=gene_score(raw),masked=gene_score(masked),all_gene_raw=raw,all_gene_masked=masked))
            null=header.new_record(contig=c,start=pos-1,alleles=(r,r))
            if gene_score([parse_score(x) for x in get_delta_scores(null,ann,500,0)])['max_delta']!=0:raise ValueError('null control failure')
            nulls+=1
            sensitivity.append(dict(key=old['key'],raw=[parse_score(x) for x in get_delta_scores(record,custom,500,0)],
                                    masked=[parse_score(x) for x in get_delta_scores(record,custom,500,1)]))
        indices=[i for i,g in enumerate(ann.genes) if g=='BUB1B']
        if len(indices)!=1:raise ValueError('gene annotation ambiguity')
        i=indices[0];c=str(ann.chroms[i]).removeprefix('chr')
        pos,r,a=donor_position(list(ann.exon_starts[i]),list(ann.exon_ends[i]),ann.strands[i])
        if ann.ref_fasta[c][pos-1:pos].seq.upper()!=r:raise ValueError('donor reference')
        controls=[]
        for alt,label in ((r,'unchanged'),(a,'synthetic_canonical_donor_disruption')):
            record=header.new_record(contig=c,start=int(pos)-1,alleles=(r,alt))
            controls.append(dict(label=label,score=gene_score([parse_score(x) for x in get_delta_scores(record,ann,500,1)])))
        for path,h in pins.items():check(path,h)
        checks=dict(lead_predictions=compare_predictions(prior['rows'],rows),
                    preferred_transcript_predictions=compare_predictions(transcripts['isoform_predictions'],sensitivity),
                    synthetic_controls=compare_predictions(transcripts['controls'],controls))
        result=dict(checks=checks,all_match=all(checks.values()),unchanged_allele_controls_passed=nulls,
                    prior_sha256=prior_hash,transcript_prior_sha256=transcript_hash,versions=versions,
                    input_hashes={str(p):h for p,h in pins.items()},script_sha256=sha(Path(__file__)),
                    model_output_precision='upstream two-decimal values',reference_protein_reconstruction_replayed=False,
                    measured_RNA=False,function_gap_closed=False)
        (output/'result.json').write_text(json.dumps(result,indent=2))
        (output/'manifest.json').write_text(json.dumps(dict(artifacts={'result.json':sha(output/'result.json')})))
        if not result['all_match']:raise ValueError('splice comparison mismatch')
        (output/'INCOMPLETE').unlink()
    print(json.dumps(dict(all_match=result['all_match'],checks=checks,unchanged_allele_controls_passed=nulls,
                         measured_RNA=False,function_gap_closed=False)))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('prior','transcripts','output'):p.add_argument('--'+n,type=Path,required=True)
    for n in ('prior-sha256','transcripts-sha256'):p.add_argument('--'+n,required=True)
    a=p.parse_args()
    try:run(a.prior,a.prior_sha256,a.transcripts,a.transcripts_sha256,a.output)
    except Exception as e:
        print('SPLICE_REPLAY_FAILED: '+type(e).__name__)
        raise SystemExit(1)
