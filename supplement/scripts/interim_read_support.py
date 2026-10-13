import re

def base_at(fields, target):
    """SAM SEQ is already alignment-oriented; never reverse-complement it again."""
    seq, qual = fields[9:11]
    if seq == '*' or qual == '*':
        return None
    if len(seq) != len(qual):
        raise ValueError('SAM sequence/quality length mismatch')
    tokens = re.findall(r'(\d+)([MIDNSHP=X])', fields[5])
    if not tokens or ''.join(n+op for n, op in tokens) != fields[5] or any(int(n) < 1 for n, _ in tokens):
        raise ValueError('invalid CIGAR')
    if sum(int(n) for n, op in tokens if op in 'MIS=X') != len(seq):
        raise ValueError('CIGAR query length mismatch')
    ref = int(fields[3]); query = 0; found = None
    for n, op in tokens:
        n = int(n)
        if op in 'M=X' and ref <= target < ref+n:
            offset = query+target-ref
            quality = ord(qual[offset])-33
            if not 0 <= quality <= 93:
                raise ValueError('invalid base quality')
            found = (seq[offset].upper(), quality, min(offset, len(seq)-1-offset))
        if op in 'MDN=X':
            ref += n
        if op in 'MIS=X':
            query += n
    return found
