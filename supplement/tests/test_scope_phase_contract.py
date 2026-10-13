import gzip
import json
from pathlib import Path
import tempfile
import unittest
from scripts.scope_phase_contract import run, pack_batches, UNIT_CAP
from scripts.portable_phase_snapshot import sha


class ScopeTests(unittest.TestCase):
    def test_two_batches_exact_once(self):
        result=pack_batches([{'source_bytes':UNIT_CAP-1},{'source_bytes':2},{'source_bytes':3}])
        self.assertEqual([b['indices'] for b in result],[[0],[1,2]])

    def test_oversized_chunk_and_third_batch(self):
        for sizes in ([UNIT_CAP+1],[UNIT_CAP,UNIT_CAP,1],[-1]):
            with self.assertRaises(ValueError):pack_batches([{'source_bytes':n} for n in sizes])

    def test_scope_and_source_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);sam=root/'input.gz'
            line=lambda chrom: f'toy\t0\t{chrom}\t1\t60\t1M\t*\t0\t0\tA\tI\n'.encode()
            sam.write_bytes(gzip.compress(line('selected')+line('other')))
            pin=sha(sam);contract=root/'contract.json'
            contract.write_text(json.dumps(dict(schema='phase-multichunk-v1',complete=True,total_pairs=2,
                markers=[dict(key=['selected',1,'A','C'])],chunks=[dict(path=str(sam),sha256=pin,start_pairs=0,end_pairs=2)])))
            result=run(contract,sha(contract),root/'out')
            self.assertEqual((result['kept_records'],result['excluded_off_contig_records']),(1,1))
            self.assertEqual(sha(sam),pin)
            self.assertEqual(gzip.decompress((root/'out/chunk-000000.sam.gz').read_bytes()),line('selected'))
            with self.assertRaises(ValueError):run(contract,sha(contract),root/'out')
            with self.assertRaises(ValueError):run(contract,'0'*64,root/'bad')
