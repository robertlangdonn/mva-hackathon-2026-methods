"""Conservative pure-function prototype. No file IO or patient-data runner.

Only non-shiftable, anchored simple indels <=50 bases are supported.
Five reference-matching flank bases per side, including the left anchor,
are required. REF/ALT labels describe a local read observation, not a call.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Target:
    chrom: str
    low: int
    high: int
    reference: str
    alternate: str
    expected_event: tuple


def prepare(chrom, position, ref, alt, context, context_start=1):
    """Return (target, reason); mismatch is an error, unsupported is explicit."""
    if not 1 <= len(context) <= 10000 or context_start < 1:
        raise ValueError('invalid bounded reference context')
    i = position-context_start
    if i < 0 or i+len(ref) > len(context):
        return None, 'INSUFFICIENT_CONTEXT'
    if context[i:i+len(ref)] != ref:
        raise ValueError('REF mismatch')
    if not ref or not alt or any(b not in 'ACGT' for b in ref+alt):
        return None, 'UNSUPPORTED_ALLELE'
    insertion = len(ref) == 1 and len(alt) > 1 and alt.startswith(ref)
    deletion = len(alt) == 1 and len(ref) > 1 and ref.startswith(alt)
    if not (insertion or deletion) or abs(len(ref)-len(alt)) > 50:
        return None, 'UNSUPPORTED_ALLELE'
    lo, hi = i-4, i+len(ref)+5  # inclusive anchor among five left flank bases
    if lo < 0 or hi > len(context):
        return None, 'INSUFFICIENT_FLANK_CONTEXT'
    if any(b not in 'ACGT' for b in context[lo:hi]):
        return None, 'AMBIGUOUS_REFERENCE'
    event = alt[1:] if insertion else ref[1:]
    # A one-base shift is possible iff a boundary matches the appropriate
    # event end. Reject the whole repeat case instead of choosing a placement.
    if event[-1] == ref[0] or event[0] == context[i+len(ref)]:
        return None, 'REPEAT_SHIFT_AMBIGUITY'
    return Target(chrom, context_start+lo, context_start+hi-1,
                  context[lo:hi], context[lo:i]+alt+context[i+len(ref):hi],
                  ('I',position+1,event) if insertion else
                  ('D',position+1,len(event))), 'READY'


def assess(fields, target):
    """SAM SEQ is alignment-oriented. All emitted bases require BQ >=20."""
    if len(fields) < 11:
        raise ValueError('truncated SAM')
    flag, mq = int(fields[1]), int(fields[4])
    if flag & 3844 or fields[2] != target.chrom or not 20 <= mq < 255:
        return 'UNINFORMATIVE_FILTER'
    seq, qual = fields[9:11]
    if seq == '*' or qual == '*':
        return 'UNINFORMATIVE_QUALITY'
    if len(seq) > 10000 or len(seq) != len(qual):
        raise ValueError('invalid query length')
    tokens = re.findall(r'(\d+)([MIDNSHP=X])', fields[5])
    if not tokens or ''.join(n+op for n,op in tokens) != fields[5] or any(int(n)<1 for n,_ in tokens):
        raise ValueError('invalid CIGAR')
    if sum(int(n) for n,op in tokens if op in 'MIS=X') != len(seq):
        raise ValueError('CIGAR query length mismatch')
    r, q = int(fields[3]), 0
    indices = []
    boundaries = set()
    skipped = False
    boundary_event = False
    boundary_quality_indices = []
    events = []
    for size, op in tokens:
        n = int(size)
        if op in 'M=X':
            start, stop = max(r,target.low), min(r+n,target.high+1)
            if start < stop:
                indices.extend(range(q+start-r, q+stop-r))
                for b in (target.low,target.high):
                    if r <= b < r+n:
                        boundaries.add(b)
        elif op == 'I':
            if target.low <= r-1 < target.high:
                indices.extend(range(q,q+n))
                events.append(('I',r,seq[q:q+n].upper()))
            if r-1 in (target.low-1,target.high):
                boundary_event = True
                boundary_quality_indices.extend(range(q,q+n))
        elif op == 'N' and r <= target.high and r+n > target.low:
            skipped = True
        elif op == 'D' and r <= target.high and r+n > target.low:
            events.append(('D',r,n))
        if op in 'MDN=X':
            r += n
        if op in 'MIS=X':
            q += n
    if skipped or boundaries != {target.low,target.high}:
        return 'UNINFORMATIVE_SPAN'
    # Boundary insertions are outside the projected haplotype, but their
    # qualities must pass before their ambiguity can affect a fragment.
    qualities = [ord(qual[j])-33 for j in indices + boundary_quality_indices]
    if any(not 0 <= b <= 93 for b in qualities):
        raise ValueError('invalid base quality')
    if any(b < 20 for b in qualities):
        return 'UNINFORMATIVE_QUALITY'
    if boundary_event:
        return 'AMBIGUOUS_LOCAL_EVENT'
    observed = ''.join(seq[j].upper() for j in indices)
    if observed == target.reference and not events:
        return 'REF'
    if observed == target.alternate and events == [target.expected_event]:
        return 'ALT'
    return 'AMBIGUOUS_LOCAL_EVENT'


def summarize(lines, target):
    """Bounded name grouping; not PCR/optical duplicate discovery or phase."""
    names = defaultdict(set)
    counts = Counter()
    for n, line in enumerate(lines):
        if n >= 50000:
            raise RuntimeError('synthetic/prototype observation cap')
        if line.startswith('@'):
            continue
        fields = line.rstrip('\n').split('\t')
        result = assess(fields,target)
        counts[result] += 1
        if result in ('REF','ALT','AMBIGUOUS_LOCAL_EVENT'):
            names[fields[0]].add(result)
            if len(names) > 10000:
                raise RuntimeError('fragment-name cap')
    fragments = Counter()
    for labels in names.values():
        label = ('AMBIGUOUS' if 'AMBIGUOUS_LOCAL_EVENT' in labels else
                 'CONFLICT' if len(labels)>1 else next(iter(labels)))
        fragments[label] += 1
    return {'read_observations': dict(counts), 'fragment_name_counts': dict(fragments)}
