"""Public-data paired sensitivity summaries; never emits a full matrix."""
import collections
import csv
import hashlib
import io
import json
import math
import statistics as st
from scripts.public_niacin_intake import DEST, unpack
from scripts.public_niacin_descriptive import PANEL


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pinned(receipt):
    blob = (DEST / receipt['name']).read_bytes()
    require(hashlib.sha256(blob).hexdigest() == receipt['sha256'], 'source hash drift')
    return unpack(blob)


def sensitivity(before, after, pseudocount):
    require(len(before) == len(after) and len(before) >= 2, 'need at least two complete pairs')
    require(all(math.isfinite(x) and x >= 0 for x in before + after), 'invalid counts')
    require(pseudocount >= 0, 'negative pseudocount')
    if pseudocount == 0 and min(before + after) == 0:
        return dict(status='undefined_zero_count', pairs=len(before))
    changes = [math.log2((b+pseudocount)/(a+pseudocount)) for a,b in zip(before,after)]
    loo = [st.median(changes[:i]+changes[i+1:]) for i in range(len(changes))]
    return dict(status='computed', pairs=len(changes), median_log2_change=st.median(changes),
                positive_pairs=sum(x>0 for x in changes),
                loo_median_range=[min(loo),max(loo)])


def read_table(text, delimiter):
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    header = next(reader)
    require(len(header) == len(set(header)), 'duplicate columns')
    data = {}
    for row in reader:
        require(len(row) == len(header) and row[0] not in data, 'row width or duplicate ID')
        values = [float(x) for x in row[2:]]
        require(all(math.isfinite(x) and x >= 0 for x in values), 'invalid matrix value')
        data[row[0]] = (row[1], values)
    return header[2:], data


def main():
    receipts = json.loads((DEST/'receipt.json').read_text())['files']
    sources = {r['name']: pinned(r) for r in receipts}
    author_receipt = json.loads((DEST/'author-receipt.json').read_text())
    acols, author = read_table(pinned(author_receipt), ',')
    cols, raw = read_table(sources['GSE129811_AWVM29samples.HTSeq.counts.tsv.gz'], '\t')
    require(cols == acols and set(author).issubset(raw), 'matrix ID/sample mismatch')
    require(all(raw[k][0] == author[k][0] for k in author), 'symbol mismatch')
    require(all(x.is_integer() for _, v in raw.values() for x in v), 'noninteger raw counts')
    ratios = [[] for _ in cols]
    for gene, (_, values) in raw.items():
        if gene.startswith('ENSG') and min(values) > 0:
            gm = st.mean(math.log(x) for x in values)
            for bucket,x in zip(ratios,values):
                bucket.append(math.exp(math.log(x)-gm))
    factors = [st.median(x) for x in ratios]
    max_relative = 0.0
    mismatches = 0
    for gene in author:
        values = raw[gene][1]
        for x,f,y in zip(values,factors,author[gene][1]):
            expected = x/f
            max_relative = max(max_relative,abs(expected-y)/max(1,abs(y)))
            mismatches += not math.isclose(expected,y,rel_tol=1e-9,abs_tol=1e-9)
    visits = collections.defaultdict(dict)
    cohorts = {}
    mapped = set()
    for block in sources['GSE129811_family.soft.gz'].split('^SAMPLE = ')[1:]:
        fields = collections.defaultdict(list)
        for line in block.splitlines():
            if ' = ' in line:
                k,v = line.split(' = ',1); fields[k].append(v)
        matches = set(fields['!Sample_description']) & set(cols)
        require(len(matches)==1, 'ambiguous sample')
        name = matches.pop()
        require(name not in mapped, 'repeated sample')
        mapped.add(name)
        pairs = [x.split(': ',1) for x in fields['!Sample_characteristics_ch1']]
        c = dict(pairs)
        require(len(c)==len(pairs), 'duplicate characteristic')
        who,month = c['individual'], int(c['time'].split()[0])
        group = c['disease state (study group)']
        require(who not in cohorts or cohorts[who]==group, 'cohort drift')
        require(month not in visits[who], 'duplicate visit')
        cohorts[who]=group; visits[who][month]=cols.index(name)
    require(mapped==set(cols), 'unmapped samples')
    results = []
    for symbol in PANEL:
        ids = [k for k in raw if raw[k][0]==symbol]
        require(len(ids)==1, 'ambiguous panel symbol')
        gene = ids[0]
        require(gene in author, 'panel gene absent from author table')
        methods = dict(local=[x/f for x,f in zip(raw[gene][1],factors)], author=author[gene][1])
        for method, values in methods.items():
            for group in sorted(set(cohorts.values())):
                for month in (4,10):
                    pairs = [v for who,v in visits.items() if cohorts[who]==group and 0 in v and month in v]
                    if not pairs:
                        continue
                    for pc in (0,0.5,1):
                        results.append(dict(gene=symbol, method=method, group=group, month=month,
                            pseudocount=pc, **sensitivity([values[v[0]] for v in pairs],[values[v[month]] for v in pairs],pc)))
    report = dict(source_hashes=[r['sha256'] for r in receipts+[author_receipt]],
        raw_rows=len(raw), author_rows=len(author), omitted_raw_rows=len(raw)-len(author),
        samples=len(cols), compared_values=len(author)*len(cols),
        mismatch_values_at_1e_minus9=mismatches, max_scaled_absolute_difference=max_relative,
        caveat='Post-observation sensitivity; same biological samples; fixed-factor leave-one-pair-out', results=results)
    (DEST/'sensitivity-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
    for r in results:
        if r['method']=='author' and r['pseudocount']==1:
            print(json.dumps(r))


if __name__ == '__main__':
    main()
