
def donor_position(starts,ends,strand):
    if len(starts)!=len(ends) or len(starts)<2:raise ValueError('multi-exon model required')
    return (ends[0]+1,'G','A') if strand=='+' else (starts[-1]-1,'C','T')
