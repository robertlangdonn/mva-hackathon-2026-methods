"""Bounded local SNV snapshot replay; connectivity is not phase or causality."""
from collections import defaultdict
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from scripts.paired_marker_graph import mates,add_links,connected
from scripts.interim_read_support import base_at

CAP=64*1024*1024

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest()

def run(contract_path,output):
    if output.exists():raise ValueError('output already exists')
    if contract_path.is_symlink() or contract_path.stat().st_size>1_000_000:raise ValueError('contract limit')
    contract_hash=sha(contract_path); c=json.loads(contract_path.read_text())
    if c.get('schema')!='snv-phase-snapshot-v1':raise ValueError('unsupported schema')
    p=Path(c['sam_gz'])
    if not p.is_absolute() or p.is_symlink() or not p.is_file() or p.stat().st_size>CAP:raise ValueError('input path/size')
    expected=c['sam_sha256']
    if sha(p)!=expected:raise ValueError('snapshot hash mismatch')
    keys=[tuple(k) for k in c['markers']]; endpoints=c['endpoints']
    if not 2<=len(keys)<=500 or len(set(keys))!=len(keys):raise ValueError('marker inventory')
    if len({k[:2] for k in keys})!=len(keys):raise ValueError('duplicate marker position')
    if any(len(k)!=4 or not isinstance(k[0],str) or type(k[1]) is not int or k[1]<1 or k[2] not in ('A','C','G','T') or k[3] not in ('A','C','G','T') or k[2]==k[3] for k in keys):raise ValueError('SNV schema')
    if len(endpoints)!=2 or endpoints[0]==endpoints[1] or any(type(i)is not int or not 0<=i<len(keys) for i in endpoints):raise ValueError('endpoint schema')
    groups=defaultdict(list);size=observations=0
    with gzip.open(p,'rb') as f:
        while line:=f.readline(65537):
            size+=len(line)
            if len(line)>65536 or size>CAP:raise ValueError('decompressed size limit')
            if line.startswith(b'@'):continue
            fields=line.decode().rstrip('\n').split('\t')
            if len(fields)<11:raise ValueError('SAM schema')
            if int(fields[1])&(4|256|512|1024|2048) or not 20<=int(fields[4])<255:continue
            obs={}
            for i,k in enumerate(keys):
                if fields[2]!=k[0]:continue
                v=base_at(fields,k[1])
                if v is not None and v[1]>=20:obs[i]=0 if v[0]==k[2] else 1 if v[0]==k[3] else None
            if obs:
                groups[fields[0]].append((fields[:9],obs));observations+=1
                if len(groups)>50000 or observations>100000:raise ValueError('observation cap')
    edges=defaultdict(lambda:defaultdict(set));accepted=0
    for name,records in groups.items():
        labels=defaultdict(set)
        for _,obs in records:
            for i,v in obs.items():labels[i].add(v)
        bad={i for i,v in labels.items() if len(v)!=1 or None in v}
        records=[(f,{i:v for i,v in obs.items() if i not in bad}) for f,obs in records]
        for _,obs in records:add_links([obs],name,edges)
        if len(records)==2 and mates(records[0][0],records[1][0]):
            add_links([r[1] for r in records],name,edges);accepted+=1
    if sha(p)!=expected or sha(contract_path)!=contract_hash:raise ValueError('input drift')
    summary=dict(markers=len(keys),relevant_names=len(groups),accepted_observed_pairs=accepted,
        edges=len(edges),optimistic_connected=connected(edges,*endpoints),
        strict_connected=connected(edges,*endpoints,strict=True),phase_established=False)
    output.mkdir(mode=0o700);(output/'INCOMPLETE').touch()
    result=dict(summary=summary,edges=[dict(markers=list(k),same=len(v.get(0,set())),opposite=len(v.get(1,set()))) for k,v in sorted(edges.items())])
    (output/'result.json').write_text(json.dumps(result,indent=2))
    (output/'manifest.json').write_text(json.dumps(dict(artifacts={'result.json':sha(output/'result.json')},contract_sha256=contract_hash,sam_sha256=expected,script_sha256=sha(Path(__file__))),indent=2))
    (output/'INCOMPLETE').unlink()
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(run(args.contract,args.output)))
