import gzip
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts.phase_journal_adapter import run
from scripts.portable_phase_snapshot import sha


class JournalAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.spec = {'schema': 'corrected-journal-adapter-v1',
                     'source_root': str(self.root), 'data_root': str(self.root)}
        self.keys = [['toy', 100, 'A', 'C'], ['toy', 120, 'A', 'G']]
        self.put('download_plan', {})
        self.put('download_checkpoint', {})
        self.put('download_receipt', {'plan_sha256': sha(self.path('download_plan')),
                 'download_checkpoint_sha256': sha(self.path('download_checkpoint'))})
        self.put('census_checkpoint', {'counts': {'complete': True, 'pairs': 4},
                 'provenance': {'download_receipt': sha(self.path('download_receipt'))}})
        self.put('census_receipt', {'pairs': 4, 'checkpoint_sha256': sha(self.path('census_checkpoint'))})
        self.put('focus', [{'packet': {'members': self.keys}}])
        (self.root/'corrected_pair_alignment.py').write_text('# synthetic source\n')
        self.plan = {'total_pairs': 4, 'chunk_pairs': 2,
                     'census_receipt': sha(self.path('census_receipt')),
                     'download_receipt': sha(self.path('download_receipt')),
                     'focus': sha(self.path('focus')), 'windows': [['toy', 1, 200]],
                     'sources': {'corrected_pair_alignment.py': sha(self.root/'corrected_pair_alignment.py')}}
        self.put('plan', self.plan, True)
        self.put('scope', {'required_sites': self.keys, 'import_old_progress': False,
                 'independent_evidence': False,
                 'wrapper_sha256': sha(self.root/'corrected_pair_alignment.py')}, True)
        self.put('markers', {'markers': [{'kind': 'snv', 'key': k} for k in self.keys], 'endpoints': [0, 1]}, True)
        self.journal = []
        for i in range(2):
            folder = self.root/f'chunk-{i:06d}-1'; folder.mkdir()
            (folder/'selected.sam.gz').write_bytes(gzip.compress(b''))
            (folder/'alignment.log').write_text('synthetic\n')
            result = dict(start_pairs=2*i, end_pairs=2*i+2, offsets=[i, i], plan_sha256=sha(self.path('plan')))
            (folder/'result.json').write_text(json.dumps(result))
            (folder/'manifest.json').write_text(json.dumps({'artifacts': {n: sha(folder/n) for n in ('selected.sam.gz', 'alignment.log', 'result.json')}}))
            self.journal.append(dict(start_pairs=2*i, end_pairs=2*i+2, offsets=[i,i], folder=folder.name, manifest_sha256=sha(folder/'manifest.json')))
        self.seal_journal()

    def path(self, name):
        return self.root/(name+'.json')

    def put(self, name, value, pinned=False):
        p = self.path(name); p.write_text(json.dumps(value))
        self.spec[name] = {'path': str(p), 'sha256': sha(p)} if pinned else str(p)

    def seal_journal(self):
        self.put('journal', self.journal)
        self.put('complete', {'journal_sha256': sha(self.path('journal')), 'total_pairs': 4, 'chunks': len(self.journal)}, True)

    def execute(self):
        self.path('spec').write_text(json.dumps(self.spec))
        return run(self.path('spec'), sha(self.path('spec')), self.root/'output')

    def test_valid_and_no_overwrite(self):
        result = self.execute()
        self.assertEqual(len(result['chunks']), 2)
        receipt = json.loads((self.root/'output/receipt.json').read_text())
        self.assertFalse(receipt['raw_census_recomputed'])
        with self.assertRaises(ValueError): self.execute()

    def test_hash_anchor(self):
        self.path('spec').write_text(json.dumps(self.spec))
        with self.assertRaises(ValueError): run(self.path('spec'), '0'*64, self.root/'output')

    def test_source_drift(self):
        (self.root/'corrected_pair_alignment.py').write_text('changed')
        with self.assertRaises(ValueError): self.execute()

    def test_artifact_drift(self):
        (self.root/self.journal[0]['folder']/'alignment.log').write_text('changed')
        with self.assertRaises(ValueError): self.execute()

    def test_truncated_journal(self):
        self.journal.pop(); self.seal_journal()
        with self.assertRaises(ValueError): self.execute()

    def test_path_traversal(self):
        self.journal[0]['folder'] = '../escape'; self.seal_journal()
        with self.assertRaises(ValueError): self.execute()

    def test_lead_mismatch(self):
        self.put('scope', {'required_sites': [['toy',101,'A','C'], self.keys[1]],
            'import_old_progress': False, 'independent_evidence': False,
            'wrapper_sha256': sha(self.root/'corrected_pair_alignment.py')}, True)
        with self.assertRaises(ValueError): self.execute()

    def test_scope_and_census_drift(self):
        self.path('census_checkpoint').write_text('{}')
        with self.assertRaises(ValueError): self.execute()

    def test_symlink(self):
        original = self.path('focus'); moved = self.root/'other.json'
        original.rename(moved); original.symlink_to(moved)
        with self.assertRaises(ValueError): self.execute()

    def test_old_progress_refused(self):
        scope = json.loads(self.path('scope').read_text())
        scope['import_old_progress'] = True
        self.put('scope', scope, True)
        with self.assertRaises(ValueError): self.execute()

    def test_final_read_drift(self):
        calls = 0
        target = self.root/'corrected_pair_alignment.py'
        def changing_hash(path):
            nonlocal calls
            if Path(path) == target:
                calls += 1
                if calls == 3:
                    target.write_text('drift after verification')
            return sha(path)
        with patch('scripts.phase_journal_adapter.sha', side_effect=changing_hash):
            with self.assertRaises(ValueError): self.execute()
        self.assertFalse((self.root/'output').exists())


if __name__ == '__main__': unittest.main()
