
def equivalent_range(sequence,index,ref,alt):
    if sequence[index:index+len(ref)]!=ref:raise ValueError('reference mismatch')
    if not ((len(ref)==1 and alt.startswith(ref)) or (len(alt)==1 and ref.startswith(alt))) or len(ref)==len(alt):
        raise ValueError('simple anchored indel required')
    edited=sequence[:index]+alt+sequence[index+len(ref):]
    positions=[]
    for j in range(len(sequence)-len(ref)+1):
        alternative=sequence[j] if len(alt)==1 else sequence[j]+edited[j+1:j+len(alt)]
        if sequence[:j]+alternative+sequence[j+len(ref):]==edited:positions.append(j)
    if not positions or index not in positions:raise ValueError('equivalence failure')
    return min(positions),max(positions)+len(ref)-1,min(positions)==0 or max(positions)==len(sequence)-len(ref)
