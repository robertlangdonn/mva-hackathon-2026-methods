import gzip
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import portable_phase_multichunk as module
from scripts.portable_phase_snapshot import sha

def sam(name,seq,cigar):
    return '\t'.join([name,'0','toy','1','60',cigar,'*','0','0',seq,'I'*len(seq)])+'\n'

class MultiChunkTests(unittest.TestCase):
    seq='GCTAGTCAAAAGTCGATCG'
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.contract=self.root/'contract.json';self.out=self.root/'out'
        self.rows=[sam('ref',self.seq,f'{len(self.seq)}M'),sam('alt','T'+self.seq[1:8]+self.seq[9:],f'8M1D{len(self.seq)-9}M')]
        self.markers=[dict(kind='snv',key=['toy',1,'G','T']),dict(kind='repeat_indel',key=['toy',7,'CA','C'],context=self.seq,context_start=1)]
        self.save()
    def save(self):
        chunks=[]
        for n,text in enumerate(self.rows):
            p=self.root/f'{n}.sam.gz';p.write_bytes(gzip.compress(text.encode(),mtime=0))
            chunks.append(dict(path=str(p),sha256=sha(p),start_pairs=n,end_pairs=n+1))
        self.c=dict(schema='phase-multichunk-v1',complete=True,total_pairs=len(chunks),chunks=chunks,markers=self.markers,endpoints=[0,1])
        self.write()
    def write(self):self.contract.write_text(json.dumps(self.c))
    def test_repeat_bridge_exact_counts(self):
        r=module.run(self.contract,self.out)
        self.assertTrue(r['strict_connected']);self.assertFalse(r['phase_established'])
        self.assertEqual(json.loads((self.out/'result.json').read_text())['edges'],[dict(markers=[0,1],same=2,opposite=0)])
    def test_simple_indel_bridge(self):
        ref='ACGTCAGTACGATCGT'
        self.markers=[dict(kind='simple_indel',key=['toy',5,'C','CTT'],context=ref,context_start=1),dict(kind='snv',key=['toy',16,'T','G'])]
        self.rows=[sam('ref',ref,'16M'),sam('alt','ACGTCTTAGTACGATCGG','5M2I11M')];self.save()
        self.assertTrue(module.run(self.contract,self.out)['strict_connected'])
    def test_opposing_support_not_strict(self):
        self.rows[1]=sam('alt','T'+self.seq[1:],f'{len(self.seq)}M');self.save()
        r=module.run(self.contract,self.out);self.assertTrue(r['optimistic_connected']);self.assertFalse(r['strict_connected'])
    def test_repeated_names_across_chunks_rejected(self):
        self.rows[1]=self.rows[1].replace('alt\t','ref\t');self.save()
        with self.assertRaisesRegex(ValueError,'crosses chunks'):module.run(self.contract,self.out)
        self.assertFalse(self.out.exists())
    def test_gap_overlap_missing_total_and_incomplete(self):
        for mode in ('gap','overlap','total','complete'):
            self.save()
            if mode=='gap':self.c['chunks'][1]['start_pairs']=2
            elif mode=='overlap':self.c['chunks'][1]['start_pairs']=0
            elif mode=='total':self.c['total_pairs']=3
            else:self.c['complete']=False
            self.write()
            with self.assertRaises(ValueError):module.run(self.contract,self.out)
            self.assertFalse(self.out.exists())
    def test_duplicate_file_and_corruption(self):
        self.c['chunks'][1]['path']=self.c['chunks'][0]['path'];self.write()
        with self.assertRaisesRegex(ValueError,'duplicate chunk'):module.run(self.contract,self.out)
        self.save();(self.root/'1.sam.gz').write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):module.run(self.contract,self.out)
    def test_source_change_during_scan(self):
        original=module.graph.add_links
        def drift(*args):
            self.contract.write_text(self.contract.read_text()+' ')
            return original(*args)
        with patch.object(module.graph,'add_links',side_effect=drift):
            with self.assertRaisesRegex(ValueError,'drift'):module.run(self.contract,self.out)
        self.assertFalse(self.out.exists())
    def test_bad_reference_and_method_selection(self):
        self.c['markers'][1]['context']='A'*len(self.seq);self.write()
        with self.assertRaisesRegex(ValueError,'REF mismatch'):module.run(self.contract,self.out)
        self.markers[1]['context']=self.seq
        self.save();self.c['markers'][1]['kind']='simple_indel';self.write()
        with self.assertRaisesRegex(ValueError,'eligibility'):module.run(self.contract,self.out)
    def test_low_quality_no_edges_and_no_overwrite(self):
        self.rows=[r.replace('I','!') for r in self.rows];self.save()
        self.assertEqual(module.run(self.contract,self.out)['edges'],0)
        with self.assertRaisesRegex(ValueError,'already exists'):module.run(self.contract,self.out)

if __name__=='__main__':unittest.main()
