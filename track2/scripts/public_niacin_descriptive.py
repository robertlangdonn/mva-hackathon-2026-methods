"""Prespecified paired descriptive analysis; no efficacy or DE claims."""
import collections
import csv
import hashlib
import io
import json
import math
import statistics as st
from scripts.public_niacin_intake import DEST, unpack

PANEL = ('BUB1B', 'SIRT2', 'NAPRT', 'NAMPT', 'NMRK1', 'NMNAT1', 'NMNAT2', 'NMNAT3', 'CD38')


def paired_effect(before, after):
    if len(before) != len(after) or not before:
        raise ValueError('nonempty matched pairs required')
    effects = [math.log2((b+1)/(a+1)) for a, b in zip(before, after)]
    return dict(pairs=len(effects), median_log2_change=round(st.median(effects), 4),
                positive_pairs=sum(x > 0 for x in effects),
                baseline_median=round(st.median(before), 3),
                post_median=round(st.median(after), 3))


def main():
    receipt = json.loads((DEST/'receipt.json').read_text())
    contents = {}
    for row in receipt['files']:
        blob = (DEST/row['name']).read_bytes()
        if hashlib.sha256(blob).hexdigest() != row['sha256']:
            raise ValueError('source drift')
        contents[row['name']] = unpack(blob)
    rows = list(csv.reader(io.StringIO(contents['GSE129811_AWVM29samples.HTSeq.counts.tsv.gz']), delimiter='\t'))
    header = rows[0]
    assert header[:2] == ['GeneID', 'GeneName']
    columns = header[2:]
    assert len(set(columns)) == len(columns)
    samples = {}
    for block in contents['GSE129811_family.soft.gz'].split('^SAMPLE = ')[1:]:
        fields = collections.defaultdict(list)
        for line in block.splitlines():
            if ' = ' in line:
                k, v = line.split(' = ', 1)
                fields[k].append(v)
        matches = set(fields['!Sample_description']) & set(columns)
        assert len(matches) == 1
        sample = matches.pop()
        assert sample not in samples
        characteristics = dict(x.split(': ', 1) for x in fields['!Sample_characteristics_ch1'])
        samples[sample] = characteristics
    assert set(samples) == set(columns)
    visits = collections.defaultdict(dict)
    cohorts = {}
    for i, name in enumerate(columns):
        s = samples[name]
        who, month = s['individual'], int(s['time'].split()[0])
        assert month not in visits[who]
        visits[who][month] = i
        group = s['disease state (study group)']
        assert who not in cohorts or cohorts[who] == group
        cohorts[who] = group
    ratios = [[] for _ in columns]
    panel = {}
    seen = set()
    norm_genes = 0
    for row in rows[1:]:
        assert len(row) == len(header) and row[0] not in seen
        seen.add(row[0])
        counts = [int(x) for x in row[2:]]
        assert all(x >= 0 for x in counts)
        if row[0].startswith('ENSG') and min(counts) > 0:
            meanlog = st.mean(math.log(x) for x in counts)
            for bucket, x in zip(ratios, counts):
                bucket.append(math.exp(math.log(x)-meanlog))
            norm_genes += 1
        if row[1] in PANEL:
            assert row[1] not in panel
            panel[row[1]] = counts
    factors = [st.median(x) for x in ratios]
    assert all(math.isfinite(x) and x > 0 for x in factors)
    results = []
    for gene in PANEL:
        if gene not in panel:
            results.append(dict(gene=gene, status='not_uniquely_available'))
            continue
        counts = panel[gene]
        normalized = [x/f for x, f in zip(counts, factors)]
        for group in sorted(set(cohorts.values())):
            for month in (4, 10):
                pairs = [v for who, v in visits.items() if cohorts[who] == group and 0 in v and month in v]
                if not pairs:
                    continue
                effect = paired_effect([normalized[v[0]] for v in pairs], [normalized[v[month]] for v in pairs])
                results.append(dict(gene=gene, group=group, month=month,
                    low_raw_count_any_sample=min(counts) < 10, **effect))
    summary = dict(samples=len(samples), participants=len(visits),
        visits=dict(collections.Counter(f'{cohorts[w]}:month{m}' for w, vs in visits.items() for m in vs)),
        normalization_genes=norm_genes, size_factor_range=[min(factors),max(factors)],
        interpretation='Exploratory paired RNA changes, not treatment efficacy or protein function',
        results=results)
    (DEST/'descriptive-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
