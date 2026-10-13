"""Bounded local provenance + journal gate. No controllers, network or cleanup.

All detailed inputs, contexts and receipts stay in ignored private output.
Only aggregate stage labels/counts are printed. Existing sources remain sealed.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from scripts.portable_phase_snapshot import sha
from scripts.phase_marker_provenance import build
from scripts.phase_journal_adapter import run as journal_contract

ROOT = Path(__file__).resolve().parents[1]


def main(workspace_root=None, alignment_data=None, output=None):
    # Versioned legacy resource layout; never import executable code from it.
    ROOT = Path(workspace_root).resolve() if workspace_root else Path(__file__).resolve().parents[1]
    os.umask(0o077)
    base = ROOT/'data/intermediate'; control = base/'corrected-pair-alignment-control'
    started = time.monotonic(); pins = {}; total = 0
    def check(path, expected=None):
        nonlocal total
        path = Path(path)
        if path.is_symlink() or not path.is_file(): raise ValueError('input path')
        if path not in pins: total += path.stat().st_size
        if total > 8_000_000_000 or time.monotonic()-started > 300: raise ValueError('provenance budget')
        digest = sha(path)
        if expected is not None and digest != expected: raise ValueError('provenance hash mismatch')
        if path in pins and pins[path] != digest: raise ValueError('provenance drift')
        pins[path] = digest
        return digest
    def read(path, expected=None):
        check(path, expected)
        if path.stat().st_size > 8_000_000: raise ValueError('metadata cap')
        return json.loads(path.read_text())
    def verified(folder):
        if (folder/'INCOMPLETE').exists(): raise ValueError('incomplete source')
        manifest = read(folder/'manifest.json')
        return read(folder/'result.json', manifest['artifacts']['result.json'])
    graph = verified(base/'paired-marker-graph-1791913158725419000')
    inventory = verified(base/'lead-gap-inventory-1791910682226016000')
    indels = verified(base/'extended-indel-feasibility-1791910867608531000')
    for name,h in graph['input_hashes'].items(): check(control/name,h)
    for name,h in inventory['plan_hashes'].items(): check(control/name,h)
    check(base/'lead-gap-inventory-1791910682226016000/result.json',graph['extended_inventory_sha256'])
    check(base/'extended-indel-feasibility-1791910867608531000/result.json',graph['indel_inventory_sha256'])
    check(base/'lead-gap-inventory-1791910682226016000/result.json',indels['inventory_sha256'])
    check(ROOT/'scripts/simple_indel_support.py',indels['assessor_sha256'])
    check(ROOT/'scripts/repeat_haplotype_support.py',graph['repeat_assessor_sha256'])
    check(ROOT/'scripts/paired_marker_graph.py',graph['script_sha256'])
    plan = read(control/'plan.json'); scope = read(control/'scope-contract.json')
    leads = sorted(tuple(k) for k in scope['required_sites'])
    old = read(base/'marker-bridges-20260923/results.json',graph['marker_input_sha256'])
    intake_path = base/'intake_manifest.json'
    intake = read(intake_path,old['sha256']['intake'])
    vcf = None
    for item in intake['files']:
        if item['role'] in ('source_vcf','source_vcf_index'):
            path = (ROOT/'data/raw'/item['name']).resolve()
            if not path.is_relative_to((ROOT/'data/raw').resolve()): raise ValueError('VCF path')
            check(path,item['sha256'])
            if item['sha256'] != old['sha256'][item['role']]: raise ValueError('VCF lineage')
            if item['role']=='source_vcf': vcf=path
    if vcf is None: raise ValueError('missing VCF')
    bcftools = Path(shutil.which('bcftools') or '/missing').resolve(); check(bcftools)
    windows = [w for w in plan['windows'] if w[0]==leads[0][0]]
    proc = subprocess.run([str(bcftools),'query','-r',','.join(f'{c}:{a}-{b}' for c,a,b in windows),
        '-f','%CHROM\t%POS\t%REF\t%ALT\t%FILTER\t[%GT]\n',str(vcf)],capture_output=True,text=True,timeout=90)
    if proc.returncode or len(proc.stdout)>2_000_000: raise ValueError('original call query')
    fresh = {}
    for line in proc.stdout.splitlines():
        f=line.split('\t')
        if len(f)!=6: raise ValueError('single sample schema')
        key=(f[0],int(f[1]),f[2],f[3]); value=(f[4],f[5])
        if key in fresh and fresh[key]!=value: raise ValueError('duplicate call conflict')
        fresh[key]=value
    if fresh != {tuple(r['key']):(r['filter'],r['gt']) for r in inventory['rows']}:
        raise ValueError('original marker inventory mismatch')
    rows = [r for r in old['results'] if sorted(tuple(k) for k in r['members'])==leads]
    if len(rows)!=1: raise ValueError('original endpoint selection')
    def heterozygous(gt):
        bits=re.split(r'[/|]',gt)
        return len(bits)==2 and all(x.isdigit() for x in bits) and bits[0]!=bits[1]
    keys={tuple(r['key']) for r in rows[0]['rows'] if heterozygous(r['gt']) and
          (r['filter']=='PASS' or tuple(r['key']) in leads) and
          len(r['key'][2])==len(r['key'][3])==1 and all(x in 'ACGT' for x in r['key'][2:])}
    # Recheck original interval rows against the fresh retention-window query.
    for row in rows[0]['rows']:
        if fresh.get(tuple(row['key'])) != (row['filter'],row['gt']): raise ValueError('original interval drift')
    keys |= {tuple(r['key']) for r in inventory['rows'] if r['category']=='outside_snv'}
    kinds={k:'snv' for k in keys}
    for row in indels['rows']:
        if row['eligibility'] in ('READY','REPEAT_SHIFT_AMBIGUITY'):
            kinds[tuple(row['key'])]='simple_indel' if row['eligibility']=='READY' else 'repeat_indel'
    keys=[list(k) for k in sorted(kinds)]
    if keys != graph['markers']: raise ValueError('historical marker selection mismatch')
    print('ORIGINAL_MARKER_SELECTION_VERIFIED',flush=True)
    ref=ROOT/'data/cache/ensembl-116/Homo_sapiens.GRCh38.dna.primary_assembly.fa'
    check(ref,indels['reference_sha256']);check(Path(str(ref)+'.fai'),indels['fai_sha256'])
    samtools=Path(shutil.which('samtools') or '/missing').resolve();check(samtools)
    def fetch(chrom,lo,hi):
        p=subprocess.run([str(samtools),'faidx',str(ref),f'{chrom}:{lo}-{hi}'],capture_output=True,text=True,timeout=30)
        if p.returncode or len(p.stdout)>20000: raise ValueError('reference extraction')
        return ''.join(p.stdout.splitlines()[1:]).upper()
    markers=build(keys,kinds,leads,plan['windows'],fetch)
    for p,h in list(pins.items()): check(p,h)
    print('REFERENCE_CONTEXTS_VERIFIED',flush=True)
    out=Path(output) if output else base/f'portable-patient-snapshot-{time.time_ns()}'
    if not out.resolve().is_relative_to(base.resolve()):raise ValueError('private output required')
    out.mkdir(mode=0o700);(out/'INCOMPLETE').touch()
    markerpath=out/'markers.json';markerpath.write_text(json.dumps(markers))
    spec=dict(schema='corrected-journal-adapter-v1',source_root=str(ROOT/'scripts'),
              data_root=str(alignment_data or '/Volumes/MVA_WORK/mva-alignment-pilot-20260927/corrected-pair-20261008'))
    for n,p in [('plan',control/'plan.json'),('scope',control/'scope-contract.json'),
                ('complete',control/'complete.json'),('markers',markerpath)]:
        spec[n]=dict(path=str(p),sha256=sha(p))
    for n,p in [('journal',control/'journal.json'),('focus',control/'focus.json'),
        ('census_receipt',base/'read-census-control/complete.json'),('census_checkpoint',base/'read-census-control/checkpoint.json'),
        ('download_receipt',base/'read-pair-control/complete.json'),('download_plan',base/'read-pair-control/plan.json'),
        ('download_checkpoint',base/'read-pair-control/download.json')]:spec[n]=str(p)
    specpath=out/'spec.json';specpath.write_text(json.dumps(spec))
    contract=journal_contract(specpath,sha(specpath),out/'journal')
    for p,h in list(pins.items()): check(p,h)
    summary=dict(markers=len(keys),chunks=len(contract['chunks']),reference_contexts_verified=True,
                 original_marker_selection_reproduced=True,journal_chain_verified=True,
                 raw_census_recomputed=False,patient_graph_replayed=False,phase_established=False)
    (out/'provenance.json').write_text(json.dumps(dict(summary=summary,input_hashes={str(p):h for p,h in pins.items()},
        markers_sha256=sha(markerpath),contract_sha256=sha(out/'journal/contract.json'))))
    (out/'INCOMPLETE').unlink()
    print(json.dumps(summary));print(out.relative_to(ROOT))
    return out


if __name__=='__main__':
    try: main()
    except Exception as exc:
        # Deliberately suppress exception payloads, paths, coordinates and tool stderr.
        print('PROVENANCE_GATE_FAILED: '+type(exc).__name__)
        raise SystemExit(1)
