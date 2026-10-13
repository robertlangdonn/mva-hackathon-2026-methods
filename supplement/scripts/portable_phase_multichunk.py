"""Hash-pinned multi-chunk SNV/indel graph replay; not a phase caller."""
from collections import defaultdict
import argparse
import gzip
import json
from pathlib import Path
import time
from scripts import paired_marker_graph as graph
from scripts import interim_read_support as snv
from scripts import simple_indel_support as simple
from scripts import repeat_haplotype_support as repeat
from scripts import retained_connectivity_bound as equivalence
from scripts.portable_phase_snapshot import sha

CAP=64*1024*1024

def targets(rows):
    if not isinstance(rows,list) or not 2<=len(rows)<=500:raise ValueError('marker count')
    seen=set();out=[]
    for row in rows:
        k=row['key'];kind=row['kind']
        if not isinstance(k,list) or len(k)!=4 or not isinstance(k[0],str) or not k[0] or type(k[1])is not int or k[1]<1:
            raise ValueError('marker schema')
        if any(not isinstance(x,str) or not 1<=len(x)<=51 or set(x)-set('ACGT') for x in k[2:]) or k[2]==k[3]:raise ValueError('allele schema')
        if tuple(k[:2]) in seen:raise ValueError('duplicate marker position')
        seen.add(tuple(k[:2]));target=None
        if kind=='snv':
            if len(k[2])!=1 or len(k[3])!=1:raise ValueError('SNV allele length')
        elif kind in ('simple_indel','repeat_indel'):
            seq=row['context'];start=row['context_start']
            if not isinstance(seq,str) or not 1<=len(seq)<=10000 or set(seq)-set('ACGT') or type(start)is not int or start<1:raise ValueError('context schema')
            i=k[1]-start
            if i<0 or i+len(k[2])>len(seq) or seq[i:i+len(k[2])]!=k[2]:raise ValueError('context REF mismatch')
            if kind=='simple_indel':
                target,reason=simple.prepare(*k,seq,start)
                if reason!='READY':raise ValueError('simple-indel eligibility failed')
            else:target=repeat.prepare(tuple(k),seq,start)
        else:raise ValueError('unsupported marker type')
        out.append((k,kind,target))
    return out

def run(contract_path,output):
    started=time.monotonic()
    def guard():
        if time.monotonic()-started>120:raise ValueError('time cap')
    if output.exists():raise ValueError('output already exists')
    if contract_path.is_symlink() or contract_path.stat().st_size>8_000_000:raise ValueError('contract size/path')
    contract_hash=sha(contract_path);c=json.loads(contract_path.read_text())
    if c.get('schema')!='phase-multichunk-v1' or c.get('complete')is not True:raise ValueError('incomplete snapshot')
    ts=targets(c['markers']);ends=c['endpoints']
    if not isinstance(ends,list) or len(ends)!=2 or ends[0]==ends[1] or any(type(i)is not int or not 0<=i<len(ts) for i in ends):raise ValueError('endpoint schema')
    chunks=c['chunks']
    if not isinstance(chunks,list) or not 1<=len(chunks)<=256:raise ValueError('chunk count')
    pins=[];paths=set();inodes=set();cursor=compressed=0
    for n,item in enumerate(chunks):
        p=Path(item['path']);lo=item['start_pairs'];hi=item['end_pairs']
        if type(lo)is not int or type(hi)is not int or lo!=cursor or hi<=lo:raise ValueError('chunk range gap/overlap')
        cursor=hi
        if not p.is_absolute() or p.is_symlink() or not p.is_file():raise ValueError('chunk path')
        stat=p.stat();identity=(stat.st_dev,stat.st_ino)
        if p.resolve() in paths or identity in inodes:raise ValueError('duplicate chunk file')
        paths.add(p.resolve());inodes.add(identity);compressed+=stat.st_size
        if compressed>CAP:raise ValueError('compressed cap')
        if sha(p)!=item['sha256']:raise ValueError('chunk hash mismatch')
        pins.append((p,item['sha256']));guard()
    if type(c['total_pairs'])is not int or cursor!=c['total_pairs']:raise ValueError('incomplete pair ranges')
    modules=(graph,snv,simple,repeat,equivalence)
    codepins={m.__name__:(Path(m.__file__),sha(Path(m.__file__))) for m in modules}
    groups=defaultdict(list);owners={};size=observations=0
    for chunk,(p,expected) in enumerate(pins):
        with gzip.open(p,'rb') as f:
            while line:=f.readline(65537):
                size+=len(line);guard()
                if len(line)>65536 or size>CAP:raise ValueError('decompressed cap')
                if line.startswith(b'@'):continue
                fields=line.decode().rstrip('\n').split('\t')
                if len(fields)<11:raise ValueError('SAM schema')
                name=fields[0]
                if name in owners and owners[name]!=chunk:raise ValueError('read name crosses chunks')
                owners[name]=chunk
                if len(owners)>50000:raise ValueError('name cap')
                if int(fields[1])&(4|256|512|1024|2048) or not 20<=int(fields[4])<255:continue
                obs={}
                for i,(k,kind,target) in enumerate(ts):
                    if fields[2]!=k[0]:continue
                    if kind=='snv':
                        value=snv.base_at(fields,k[1])
                        if value is not None and value[1]>=20:obs[i]=0 if value[0]==k[2] else 1 if value[0]==k[3] else None
                    elif kind=='simple_indel':
                        value=simple.assess(fields,target)
                        if value in ('REF','ALT'):obs[i]=int(value=='ALT')
                        elif value=='AMBIGUOUS_LOCAL_EVENT':obs[i]=None
                    else:
                        value=repeat.assess(fields,target)
                        if value is not None:obs[i]=value
                if obs:
                    groups[name].append((fields[:9],obs));observations+=1
                    if observations>100000:raise ValueError('observation cap')
    edges=defaultdict(lambda:defaultdict(set));accepted=0
    for name,records in groups.items():
        labels=defaultdict(set)
        for _,obs in records:
            for i,v in obs.items():labels[i].add(v)
        bad={i for i,v in labels.items() if len(v)!=1 or None in v}
        records=[(f,{i:v for i,v in obs.items() if i not in bad}) for f,obs in records]
        for _,obs in records:graph.add_links([obs],name,edges)
        if len(records)==2 and graph.mates(records[0][0],records[1][0]):
            graph.add_links([r[1] for r in records],name,edges);accepted+=1
    if sha(contract_path)!=contract_hash or any(sha(p)!=h for p,h in pins) or any(sha(p)!=h for p,h in codepins.values()):raise ValueError('input/source drift')
    guard()
    summary=dict(chunks=len(pins),declared_pairs=cursor,markers=len(ts),relevant_names=len(groups),
        accepted_observed_pairs=accepted,edges=len(edges),optimistic_connected=graph.connected(edges,*ends),
        strict_connected=graph.connected(edges,*ends,strict=True),phase_established=False)
    output.mkdir(mode=0o700);(output/'INCOMPLETE').touch()
    result=dict(summary=summary,edges=[dict(markers=list(k),same=len(v.get(0,set())),opposite=len(v.get(1,set()))) for k,v in sorted(edges.items())])
    (output/'result.json').write_text(json.dumps(result,indent=2))
    (output/'manifest.json').write_text(json.dumps(dict(artifacts={'result.json':sha(output/'result.json')},
        contract_sha256=contract_hash,chunks_sha256=[h for p,h in pins],source_sha256={n:h for n,(p,h) in codepins.items()},
        script_sha256=sha(Path(__file__)),raw_pair_census_recomputed=False),indent=2))
    (output/'INCOMPLETE').unlink();return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--contract',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(run(a.contract,a.output)))
