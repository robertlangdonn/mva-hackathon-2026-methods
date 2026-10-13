from collections import defaultdict
from itertools import combinations

def mates(a, b):
    fa, fb = int(a[1]), int(b[1])
    return (all(f & 3 == 3 and not f & (4|8|256|512|1024|2048) for f in (fa,fb))
            and {fa & 192, fb & 192} == {64,128}
            and a[2] == b[2] and a[6] in ('=', b[2]) and b[6] in ('=', a[2])
            and int(a[7]) == int(b[3]) and int(b[7]) == int(a[3])
            and bool(fa & 32) == bool(fb & 16) and bool(fb & 32) == bool(fa & 16)
            and bool(fa & 16) != bool(fb & 16)
            and int(a[8]) != 0 and int(a[8]) == -int(b[8]))

def add_links(observations, name, edges):
    merged = defaultdict(set)
    for obs in observations:
        for marker, allele in obs.items(): merged[marker].add(allele)
    clean = {k:next(iter(v)) for k,v in merged.items() if len(v)==1 and None not in v}
    for (a,x),(b,y) in combinations(sorted(clean.items()),2):
        edges[(a,b)][x ^ y].add(name)

def connected(edges, start, end, strict=False):
    graph = defaultdict(set)
    for (a,b), support in edges.items():
        counts = [len(support.get(i,set())) for i in (0,1)]
        if strict and not (min(counts)==0 and max(counts)>=2): continue
        if not any(counts): continue
        graph[a].add(b); graph[b].add(a)
    seen={start}; stack=[start]
    while stack:
        for node in graph[stack.pop()] - seen: seen.add(node); stack.append(node)
    return end in seen
