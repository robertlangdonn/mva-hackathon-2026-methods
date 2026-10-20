"""One bounded additional public processed input, separate pinned receipt."""
import hashlib
import json
from scripts.public_niacin_intake import DEST, BASE, fetch

NAME = 'GSE129811_AWVM29samples.DESeq.normCounts.csv.gz'


def main():
    receipt = DEST / 'author-receipt.json'
    url = BASE + 'suppl/' + NAME
    blob = fetch(NAME, url)
    result = dict(name=NAME, url=url, bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest())
    if receipt.exists() and json.loads(receipt.read_text()) != result:
        raise ValueError('author normalized source drift')
    receipt.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
