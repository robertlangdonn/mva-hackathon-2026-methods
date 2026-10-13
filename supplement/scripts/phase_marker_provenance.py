"""Build marker contracts from pinned selections and reference-derived contexts."""
from scripts.portable_phase_multichunk import targets


def build(keys, kinds, leads, windows, fetch):
    if not 2 <= len(keys) <= 500 or len({tuple(k) for k in keys}) != len(keys):
        raise ValueError('marker scope')
    rows = []
    for key in keys:
        chrom, pos, ref, alt = key
        kind = kinds[tuple(key)]
        row = dict(key=list(key), kind=kind)
        if kind == 'snv':
            if fetch(chrom, pos, pos+len(ref)-1) != ref:
                raise ValueError('reference mismatch')
        else:
            pad = 1000 if kind == 'repeat_indel' else 64
            start = max(1, pos-pad); end = pos+len(ref)+pad
            seq = fetch(chrom, start, end)
            if len(seq) != end-start+1:
                raise ValueError('truncated context')
            row.update(context=seq, context_start=start)
        rows.append(row)
    parsed = targets(rows)
    for key, kind, target in parsed:
        chrom, pos, ref, alt = key
        low, high = pos, pos+len(ref)-1
        if kind == 'repeat_indel': low, high = target['low'], target['high']
        elif kind == 'simple_indel': low, high = target.low, target.high
        if not any(c == chrom and a <= low and high <= b for c,a,b in windows):
            raise ValueError('required flanks outside retention')
    endpoints = [keys.index(list(k)) for k in leads]
    if len(endpoints) != 2 or len(set(endpoints)) != 2:
        raise ValueError('lead endpoints')
    return dict(markers=rows, endpoints=endpoints)
