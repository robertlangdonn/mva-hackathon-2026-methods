import unittest
from scripts.repeat_haplotype_support import prepare,assess
class RepeatTests(unittest.TestCase):
    seq='GCTAGTCAAAAGTCGATCG'
    def sam(self,cigar,seq,qual=None):return ['r','0','1','1','60',cigar,'*','0','0',seq,qual or 'I'*len(seq)]
    def test_shifted_deletions(self):
        t=prepare(('1',7,'CA','C'),self.seq,1)
        for j in range(7,11):
            alt=self.seq[:j]+self.seq[j+1:]
            self.assertEqual(assess(self.sam(f'{j}M1D{len(self.seq)-j-1}M',alt),t),1)
        self.assertEqual(assess(self.sam(f'{len(self.seq)}M',self.seq),t),0)
    def test_shifted_insertions(self):
        t=prepare(('1',7,'C','CA'),self.seq,1)
        for j in range(7,12):
            alt=self.seq[:j]+'A'+self.seq[j:]
            self.assertEqual(assess(self.sam(f'{j}M1I{len(self.seq)-j}M',alt),t),1)
    def test_quality_and_mismatch(self):
        t=prepare(('1',7,'CA','C'),self.seq,1)
        self.assertIsNone(assess(self.sam(f'{len(self.seq)}M',self.seq,'!'*len(self.seq)),t))
        wrong=self.seq[:8]+'C'+self.seq[9:]
        self.assertIsNone(assess(self.sam(f'{len(wrong)}M',wrong),t))
    def test_partial_and_bad_cigar(self):
        t=prepare(('1',7,'CA','C'),self.seq,1)
        self.assertIsNone(assess(self.sam('5M',self.seq[:5]),t))
        with self.assertRaises(ValueError):assess(self.sam('1M',self.seq),t)
    def test_ambiguous_context(self):
        with self.assertRaises(ValueError):prepare(('1',1,'CA','C'),'CAAA',1)
if __name__=='__main__':unittest.main()
