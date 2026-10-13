import unittest
from scripts.portable_splice_replay import compare_predictions


class SpliceComparisonTests(unittest.TestCase):
    def test_exact(self):self.assertTrue(compare_predictions([{'scores':[0,.03]}],[{'scores':[0,.03]}]))
    def test_changed_score(self):self.assertFalse(compare_predictions([{'scores':[0,.03]}],[{'scores':[0,.04]}]))
    def test_missing_row(self):self.assertFalse(compare_predictions([{}],[]))
    def test_positions_matter(self):self.assertFalse(compare_predictions([{'position':1}],[{'position':2}]))
