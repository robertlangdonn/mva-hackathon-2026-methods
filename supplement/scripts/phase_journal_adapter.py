"""Read-only completed-journal adapter. Inputs and outputs are controlled material.

The caller supplies an independently recorded specification hash. This proves
consistency with that anchor, not authenticity or a fresh raw-read census.
"""
import argparse
import json
from pathlib import Path
import re
import time
from scripts.portable_phase_snapshot import sha
from scripts.portable_phase_multichunk import targets


def run(spec_path, expected_sha256, output):
    if output.exists():
        raise ValueError('output already exists')
    pins = {}
    size = 0
    started = time.monotonic()

    def checked(path, expected=None, cap=8_000_000):
        nonlocal size
        path = Path(path)
        if not path.is_absolute() or any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
            raise ValueError('unsafe input path')
        n = path.stat().st_size
        if path not in pins:
            size += n
        if n > cap or size > 250_000_000 or time.monotonic()-started > 120:
            raise ValueError('input budget exceeded')
        digest = sha(path)
        if expected is not None and digest != expected:
            raise ValueError('input hash mismatch')
        if path in pins and pins[path] != digest:
            raise ValueError('input drift')
        pins[path] = digest
        return path

    def read(path, expected=None):
        return json.loads(checked(path, expected).read_text())

    spec = read(spec_path, expected_sha256)
    if spec.get('schema') != 'corrected-journal-adapter-v1':
        raise ValueError('specification schema')
    def named(name):
        item = spec[name]
        return read(item['path'], item['sha256'])
    plan, scope, done = (named(n) for n in ('plan', 'scope', 'complete'))
    journal = read(spec['journal'], done['journal_sha256'])
    census = read(spec['census_receipt'], plan['census_receipt'])
    checkpoint = read(spec['census_checkpoint'], census['checkpoint_sha256'])
    download = read(spec['download_receipt'], plan['download_receipt'])
    read(spec['download_plan'], download['plan_sha256'])
    read(spec['download_checkpoint'], download['download_checkpoint_sha256'])
    if checkpoint['counts'].get('complete') is not True or checkpoint['counts']['pairs'] != census['pairs'] or checkpoint['provenance']['download_receipt'] != plan['download_receipt']:
        raise ValueError('census lineage mismatch')
    total = plan['total_pairs']
    if type(total) is not int or total <= 0 or total != census['pairs'] or total != done['total_pairs']:
        raise ValueError('total mismatch')
    if type(plan['chunk_pairs']) is not int or plan['chunk_pairs'] <= 0:
        raise ValueError('chunk size')
    focus = read(spec['focus'], plan['focus'])
    focus_keys = {tuple(k) for row in focus for k in row['packet']['members']}
    required = {tuple(k) for k in scope['required_sites']}
    if len(required) != 2 or scope.get('import_old_progress') is not False or scope.get('independent_evidence') is not False or not required <= focus_keys:
        raise ValueError('corrected scope mismatch')
    source_root = Path(spec['source_root'])
    if not plan['sources']:
        raise ValueError('missing source pins')
    for name, digest in plan['sources'].items():
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError('source traversal')
        checked(source_root/name, digest)
    checked(source_root/'corrected_pair_alignment.py', scope['wrapper_sha256'])
    markers = named('markers')
    parsed = targets(markers['markers'])
    ends = markers['endpoints']
    if not isinstance(ends, list) or len(ends) != 2 or len(set(ends)) != 2 or any(type(i) is not int or not 0 <= i < len(parsed) for i in ends):
        raise ValueError('endpoint schema')
    if {tuple(parsed[i][0]) for i in ends} != required:
        raise ValueError('lead endpoints mismatch')
    for key, _, _ in parsed:
        if not any(chrom == key[0] and lo <= key[1] <= hi for chrom, lo, hi in plan['windows']):
            raise ValueError('marker outside retained scope')
    if not isinstance(journal, list) or not 1 <= len(journal) <= 256 or len(journal) != done['chunks']:
        raise ValueError('journal count')
    cursor = 0
    chunks = []
    identities = set()
    for receipt in journal:
        name = receipt['folder']
        if not re.fullmatch(r'chunk-\d{6}-\d+', name):
            raise ValueError('folder traversal')
        folder = Path(spec['data_root'])/name
        manifest = read(folder/'manifest.json', receipt['manifest_sha256'])
        if set(manifest['artifacts']) != {'selected.sam.gz', 'result.json', 'alignment.log'}:
            raise ValueError('artifact set')
        for artifact, digest in manifest['artifacts'].items():
            checked(folder/artifact, digest, 64*1024*1024)
        result = read(folder/'result.json', manifest['artifacts']['result.json'])
        if any(result[k] != receipt[k] for k in ('start_pairs', 'end_pairs', 'offsets')) or result['plan_sha256'] != spec['plan']['sha256']:
            raise ValueError('chunk receipt mismatch')
        end = min(cursor+plan['chunk_pairs'], total)
        if receipt['start_pairs'] != cursor or receipt['end_pairs'] != end or end <= cursor:
            raise ValueError('journal range mismatch')
        sam = folder/'selected.sam.gz'
        stat = sam.stat(); identity = (stat.st_dev, stat.st_ino)
        if identity in identities:
            raise ValueError('duplicate artifact')
        identities.add(identity)
        chunks.append(dict(path=str(sam), sha256=manifest['artifacts']['selected.sam.gz'], start_pairs=cursor, end_pairs=end))
        cursor = end
    if cursor != total:
        raise ValueError('incomplete journal')
    for path, digest in pins.items():
        checked(path, digest, 64*1024*1024)
    contract = dict(schema='phase-multichunk-v1', complete=True, total_pairs=total,
                    chunks=chunks, markers=markers['markers'], endpoints=ends)
    output.mkdir(mode=0o700, parents=True)
    (output/'INCOMPLETE').touch()
    (output/'contract.json').write_text(json.dumps(contract, sort_keys=True))
    (output/'receipt.json').write_text(json.dumps(dict(specification_sha256=expected_sha256,
        contract_sha256=sha(output/'contract.json'), chunks=len(chunks), journal_chain_verified=True,
        raw_census_recomputed=False, reference_context_authenticated=False,
        patient_result_reproduced=False, phase_established=False), sort_keys=True))
    (output/'INCOMPLETE').unlink()
    return contract


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.spec, args.sha256, args.output)
    print('Journal contract verified; no read replay performed.')
