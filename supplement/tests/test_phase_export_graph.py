from collections import defaultdict
import unittest
from scripts.paired_marker_graph import mates,add_links,connected

class PhaseGraphExportTests(unittest.TestCase):
    def test_reciprocal_mates(self):
        a=['toy','99','mock','10','60','5M','=','30','25']
        b=['toy','147','mock','30','60','5M','=','10','-25']
        self.assertTrue(mates(a,b));b[7]='11';self.assertFalse(mates(a,b))
    def test_strict_bridge_and_disconnection(self):
        e=defaultdict(lambda:defaultdict(set))
        for n in ('a','b'):add_links([{0:0,1:1}],n,e)
        for n in ('c','d'):add_links([{1:0,2:1}],n,e)
        self.assertTrue(connected(e,0,2,True));self.assertFalse(connected(e,0,3))
    def test_deduplication_and_opposing_support(self):
        e=defaultdict(lambda:defaultdict(set))
        for _ in range(3):add_links([{0:0,1:1}],'a',e)
        self.assertTrue(connected(e,0,1));self.assertFalse(connected(e,0,1,True))
        add_links([{0:0,1:1}],'b',e);self.assertTrue(connected(e,0,1,True))
        add_links([{0:0,1:0}],'c',e);self.assertFalse(connected(e,0,1,True))
    def test_conflicting_observations_removed(self):
        e=defaultdict(lambda:defaultdict(set))
        add_links([{0:0,1:0},{0:1,2:None}],'a',e)
        self.assertEqual(dict(e),{})
