import copy
import unittest
from scripts.portable_phase_workflow import compare


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.markers=[dict(key=['toy',1,'A','C']),dict(key=['toy',2,'C','G'])]
        summary=dict(markers=2,relevant_names=2,accepted_observed_pairs=2,edges=1,
                     optimistic_connected=True,strict_connected=True,phase_established=False,chunks=2)
        self.old=dict(markers=[r['key'] for r in self.markers],summary=summary,
                      edges=[dict(markers=[0,1],same=2,opposite=0)])
        self.new=copy.deepcopy(self.old)

    def test_exact_match(self):
        self.assertTrue(compare(self.old,self.new,self.markers)['all_match'])

    def test_counts_not_only_topology(self):
        self.new['edges'][0]['same']=3
        self.assertFalse(compare(self.old,self.new,self.markers)['all_match'])

    def test_summary_drift(self):
        self.new['summary']['relevant_names']=3
        self.assertFalse(compare(self.old,self.new,self.markers)['all_match'])

    def test_marker_permutation(self):
        with self.assertRaises(ValueError):compare(self.old,self.new,self.markers[::-1])
