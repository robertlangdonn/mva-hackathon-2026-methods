
def parse_score(value):
    fields=value.split('|')
    if len(fields)!=10: raise ValueError('score schema')
    scores=[float(v) for v in fields[2:6]]
    if any(not 0<=v<=1 for v in scores): raise ValueError('invalid scores')
    return dict(gene=fields[1],scores=scores,positions=[int(v) for v in fields[6:]],max_delta=max(scores))

def gene_score(scores, gene='BUB1B'):
    selected=[s for s in scores if s['gene']==gene]
    if len(selected)!=1: raise ValueError('target gene score missing or ambiguous')
    return selected[0]
