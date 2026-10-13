import unittest
from scripts.phase_marker_provenance import build


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.keys = [['toy', 10, 'A', 'C'], ['toy', 20, 'A', 'G']]
        self.kinds = {tuple(k): 'snv' for k in self.keys}

    def test_reference_checked(self):
        got = build(self.keys, self.kinds, self.keys, [['toy',1,30]], lambda c,a,b: 'A'*(b-a+1))
        self.assertEqual(got['endpoints'], [0,1])

    def test_wrong_reference(self):
        with self.assertRaises(ValueError):
            build(self.keys, self.kinds, self.keys, [['toy',1,30]], lambda *args: 'T')

    def test_missing_retention(self):
        with self.assertRaises(ValueError):
            build(self.keys, self.kinds, self.keys, [['toy',1,15]], lambda *args: 'A')

    def test_truncated_indel_context(self):
        key = ['toy',15,'A','AT']; keys = self.keys+[key]
        kinds = dict(self.kinds); kinds[tuple(key)] = 'simple_indel'
        with self.assertRaises(ValueError):
            build(keys, kinds, self.keys, [['toy',1,3000]], lambda *args: 'A')
