import gzip
import json
from pathlib import Path
import tempfile
import unittest
from scripts.portable_phase_snapshot import run,sha

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.sam=self.root/'toy.sam.gz';self.contract=self.root/'contract.json';self.out=self.root/'out'
        self.rows=['a\t0\ttoy\t1\t60\t4M\t*\t0\t0\tACGT\tIIII\n','b\t0\ttoy\t1\t60\t4M\t*\t0\t0\tACGT\tIIII\n']
        self.save()
    def save(self,**changes):
        self.sam.write_bytes(gzip.compress(''.join(self.rows).encode(),mtime=0))
        c=dict(schema='snv-phase-snapshot-v1',sam_gz=str(self.sam),sam_sha256=sha(self.sam),markers=[['toy',1,'A','T'],['toy',4,'T','A']],endpoints=[0,1]);c.update(changes)
        self.contract.write_text(json.dumps(c))
    def test_graph_and_no_overwrite(self):
        result=run(self.contract,self.out)
        self.assertTrue(result['strict_connected']);self.assertFalse(result['phase_established'])
        with self.assertRaises(ValueError):run(self.contract,self.out)
    def test_hash_drift_rejected_before_output(self):
        self.sam.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'hash'):run(self.contract,self.out)
        self.assertFalse(self.out.exists())
    def test_repeated_name_does_not_inflate_support(self):
        self.rows=[self.rows[0],self.rows[0]];self.save()
        result=run(self.contract,self.out)
        self.assertTrue(result['optimistic_connected']);self.assertFalse(result['strict_connected'])
    def test_conflicting_same_name_removed(self):
        self.rows=[self.rows[0],self.rows[0].replace('ACGT','TCGT')];self.save()
        self.assertEqual(run(self.contract,self.out)['edges'],0)
    def test_wrong_marker_shape_and_low_quality(self):
        self.save(markers=[['toy',1,'A','T'],['toy',1,'A','G']])
        with self.assertRaises(ValueError):run(self.contract,self.out)
        self.rows=[r.replace('IIII','!!!!') for r in self.rows];self.save()
        self.assertEqual(run(self.contract,self.out)['relevant_names'],0)
    def test_record_limit_and_symlink(self):
        self.rows=['x'*65537+'\n'];self.save()
        with self.assertRaisesRegex(ValueError,'size limit'):run(self.contract,self.out)
        self.rows=[];self.save();link=self.root/'link.gz';link.symlink_to(self.sam)
        self.save(sam_gz=str(link))
        with self.assertRaisesRegex(ValueError,'path/size'):run(self.contract,self.out)
