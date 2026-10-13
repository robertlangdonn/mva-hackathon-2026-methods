import unittest
from scripts.local_lead_splice import parse_score, gene_score

class ScoreTests(unittest.TestCase):
    def test_overlapping_genes_preserved_but_target_selected(self):
        scores=[dict(gene='BUB1B',max_delta=0),dict(gene='PAK6',max_delta=.8)]
        self.assertEqual(gene_score(scores)['max_delta'],0)
        self.assertEqual(len(scores),2)
        with self.assertRaises(ValueError):gene_score(scores[1:])
        with self.assertRaises(ValueError):gene_score([scores[0],scores[0]])
    def test_exact_fields(self):
        r=parse_score('A|TOY|0.00|0.20|0.10|0.01|-1|2|3|4')
        self.assertEqual(r['max_delta'],0.2)
        self.assertEqual(r['positions'],[-1,2,3,4])
    def test_bad(self):
        for value in ('A|TOY|0.2','A|TOY|nan|0|0|0|1|2|3|4','A|TOY|1.1|0|0|0|1|2|3|4'):
            with self.assertRaises(ValueError): parse_score(value)

if __name__=='__main__':unittest.main()
