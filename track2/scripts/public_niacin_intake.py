"""Bounded public GEO intake; prints metadata/schema aggregates, not matrices."""
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data/cache/public-niacin-GSE129811'
BASE = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE129nnn/GSE129811/'
FILES = {
    'GSE129811_family.soft.gz': BASE + 'soft/GSE129811_family.soft.gz',
    'GSE129811_AWVM29samples.HTSeq.counts.tsv.gz': BASE + 'suppl/GSE129811_AWVM29samples.HTSeq.counts.tsv.gz',
}
CAP = 10 * 1024 * 1024


def fetch(name, url):
    target = DEST / name
    if target.exists():
        payload = target.read_bytes()
        if len(payload) > CAP:
            raise ValueError('cached file exceeds cap')
    else:
        with urllib.request.urlopen(url, timeout=45) as response:
            payload = response.read(CAP + 1)
        if len(payload) > CAP:
            raise ValueError('download cap exceeded')
        # Validate compressed format and decompression cap before retaining.
        unpack(payload)
        partial = target.with_suffix('.partial')
        partial.write_bytes(payload)
        partial.replace(target)
    return payload


def unpack(payload):
    with gzip.GzipFile(fileobj=io.BytesIO(payload)) as handle:
        plain = handle.read(100 * 1024 * 1024 + 1)
    if len(plain) > 100 * 1024 * 1024:
        raise ValueError('expanded size cap exceeded')
    return plain.decode('utf-8-sig')


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    receipts = []
    contents = {}
    previous = DEST / 'receipt.json'
    old = {x['name']: x['sha256'] for x in json.loads(previous.read_text())['files']} if previous.exists() else {}
    for name, url in FILES.items():
        payload = fetch(name, url)
        digest = hashlib.sha256(payload).hexdigest()
        if name in old and old[name] != digest:
            raise ValueError('cached source hash drift')
        receipts.append(dict(name=name, url=url, bytes=len(payload), sha256=digest))
        contents[name] = unpack(payload)
    soft = contents['GSE129811_family.soft.gz']
    samples = []
    for block in soft.split('^SAMPLE = ')[1:]:
        fields = {}
        for line in block.splitlines()[1:]:
            if line.startswith('!Sample_') and ' = ' in line:
                key, value = line.split(' = ', 1)
                fields.setdefault(key, []).append(value)
        samples.append(fields)
    table = list(csv.reader(io.StringIO(contents['GSE129811_AWVM29samples.HTSeq.counts.tsv.gz']), delimiter='\t'))
    summary = dict(metadata_samples=len(samples), table_rows=len(table)-1,
                   header_columns=len(table[0]), first_row_columns=len(table[1]),
                   metadata_keys=sorted(set(k for sample in samples for k in sample)))
    receipt = dict(files=receipts, summary=summary)
    previous.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
