import re
from scripts.retained_connectivity_bound import equivalent_range

def prepare(key,sequence,start):
    c,pos,ref,alt=key;i=pos-start
    lo,hi,censored=equivalent_range(sequence,i,ref,alt)
    if censored or lo<5 or hi+6>len(sequence):raise ValueError('repeat/context boundary unresolved')
    low=lo-5; high=hi+6
    reference=sequence[low:high]
    alternate=sequence[low:i]+alt+sequence[i+len(ref):high]
    if set(reference+alternate)-set('ACGT'):raise ValueError('ambiguous context')
    return dict(chrom=c,low=start+low,high=start+high-1,reference=reference,alternate=alternate)

def assess(fields,target):
    if len(fields)<11:raise ValueError('SAM schema')
    if fields[2]!=target['chrom'] or int(fields[1])&(4|256|512|1024|2048) or not 20<=int(fields[4])<255:return None
    seq,qual=fields[9:11]
    if seq=='*' or qual=='*':return None
    if len(seq)!=len(qual):raise ValueError('query quality lengths')
    parts=re.findall(r'(\d+)([MIDNSHP=X])',fields[5])
    if not parts or ''.join(n+op for n,op in parts)!=fields[5] or any(int(n)<1 for n,op in parts):raise ValueError('CIGAR syntax')
    if sum(int(n) for n,op in parts if op in 'MIS=X')!=len(seq):raise ValueError('query CIGAR length')
    r=int(fields[3]);q=0;indices=[];boundaries=set();low=target['low'];high=target['high']
    for size,op in parts:
        n=int(size)
        if op in 'M=X':
            a,b=max(low,r),min(high+1,r+n)
            if a<b:indices.extend(range(q+a-r,q+b-r))
            for endpoint in (low,high):
                if r<=endpoint<r+n:boundaries.add(endpoint)
        elif op=='I':
            if r-1 in (low-1,high):return None
            if low<=r-1<high:indices.extend(range(q,q+n))
        elif op=='N' and r<=high and r+n>low:return None
        if op in 'MDN=X':r+=n
        if op in 'MIS=X':q+=n
    if boundaries!={low,high} or any(not 20<=ord(qual[i])-33<=93 for i in indices):return None
    hap=''.join(seq[i].upper() for i in indices)
    if hap==target['reference']:return 0
    if hap==target['alternate']:return 1
    return None
