"""Create hash-audited marker-contig subsets; never modify source chunks.

Matches the historical graph's contig filter before name accounting. Pair ranges
still describe source chunks, not retained counts. No off-contig evidence claim.
"""
import gzip
import json
from pathlib import Path
import time
from scripts.portable_phase_snapshot import sha

UNIT_CAP = 64*1024*1024
MAX_BATCHES = 2


def pack_batches(records):
    """Whole chunks, exactly once; two bounded scan units, no result pooling."""
    batches=[]; current=[]; size=0
    for index, record in enumerate(records):
        n=record['source_bytes']
        if type(n) is not int or not 0 <= n <= UNIT_CAP: raise ValueError('chunk budget')
        if current and size+n>UNIT_CAP:
            batches.append(dict(indices=current,source_bytes=size));current=[];size=0
        current.append(index);size+=n
    if current:batches.append(dict(indices=current,source_bytes=size))
    if len(batches)>MAX_BATCHES:raise ValueError('batch count cap')
    if [i for b in batches for i in b['indices']]!=list(range(len(records))):raise ValueError('batch coverage')
    return batches


def run(contract_path, expected_sha256, output):
    if output.exists(): raise ValueError('output exists')
    if sha(contract_path)!=expected_sha256: raise ValueError('contract hash')
    c=json.loads(contract_path.read_text())
    if c.get('schema')!='phase-multichunk-v1' or c.get('complete') is not True or not 1<=len(c['chunks'])<=256:
        raise ValueError('contract scope')
    contigs={row['key'][0] for row in c['markers']}
    if len(contigs)!=1: raise ValueError('single-contig scope required')
    output.mkdir(mode=0o700);(output/'INCOMPLETE').touch()
    size=kept=excluded=output_bytes=compressed=0;cursor=0;identities=set();pins=[];chunks=[];records=[]
    started=time.monotonic()
    for i,item in enumerate(c['chunks']):
        p=Path(item['path'])
        if p.is_symlink() or not p.is_file() or sha(p)!=item['sha256']: raise ValueError('source hash/path')
        stat=p.stat();identity=(stat.st_dev,stat.st_ino)
        compressed+=stat.st_size
        if compressed>UNIT_CAP:raise ValueError('compressed source cap')
        if identity in identities: raise ValueError('duplicate source')
        identities.add(identity)
        if item['start_pairs']!=cursor or item['end_pairs']<=cursor: raise ValueError('source ranges')
        cursor=item['end_pairs'];pins.append((p,item['sha256']))
        dest=output/f'chunk-{i:06d}.sam.gz'
        chunk_bytes=0
        with gzip.open(p,'rb') as source, dest.open('wb') as raw:
            with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as sink:
                while line:=source.readline(65537):
                    size+=len(line);chunk_bytes+=len(line)
                    if len(line)>65536 or chunk_bytes>UNIT_CAP or size>MAX_BATCHES*UNIT_CAP or time.monotonic()-started>120: raise ValueError('scope budget')
                    if line.startswith(b'@'):
                        output_bytes+=len(line)
                        if output_bytes>UNIT_CAP:raise ValueError('scoped output budget')
                        sink.write(line);continue
                    fields=line.rstrip(b'\n').split(b'\t')
                    if len(fields)<11: raise ValueError('SAM schema')
                    if fields[2].decode() in contigs:
                        output_bytes+=len(line)
                        if output_bytes>UNIT_CAP:raise ValueError('scoped output budget')
                        sink.write(line);kept+=1
                    else: excluded+=1
        chunks.append(dict(item,path=str(dest),sha256=sha(dest)))
        records.append(dict(source_sha256=item['sha256'],output_sha256=sha(dest),source_bytes=chunk_bytes,
                            start_pairs=item['start_pairs'],end_pairs=item['end_pairs']))
        pack_batches(records)
    if cursor!=c['total_pairs']: raise ValueError('source total')
    if sha(contract_path)!=expected_sha256 or any(sha(p)!=h for p,h in pins): raise ValueError('source drift')
    c['chunks']=chunks
    batches=pack_batches(records)
    (output/'batches.json').write_text(json.dumps(dict(chunks=records,batches=batches,source_contract_sha256=expected_sha256)))
    c['scope_derivation']={'source_contract_sha256':expected_sha256,'method':'marker-contig-bounded-batches-v2',
                           'batch_manifest_sha256':sha(output/'batches.json'),
                           'pair_ranges_describe_source':True}
    (output/'contract.json').write_text(json.dumps(c))
    summary=dict(kept_records=kept,excluded_off_contig_records=excluded,source_bytes=size,
                 scoped_bytes=output_bytes,batches=len(batches),batch_manifest_sha256=sha(output/'batches.json'),
                 chunks=len(chunks),source_contract_sha256=expected_sha256,
                 contract_sha256=sha(output/'contract.json'),script_sha256=sha(Path(__file__)),
                 cross_chunk_names_checked_only_within_selected_contig=True)
    (output/'receipt.json').write_text(json.dumps(summary))
    (output/'INCOMPLETE').unlink()
    return summary
