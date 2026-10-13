import unittest
from scripts.splice_transcript_controls import donor_position
class DonorTests(unittest.TestCase):
    def test_plus(self):self.assertEqual(donor_position([10,30],[20,40],'+'),(21,'G','A'))
    def test_minus(self):self.assertEqual(donor_position([10,30],[20,40],'-'),(29,'C','T'))
    def test_single_exon(self):
        with self.assertRaises(ValueError):donor_position([10],[20],'+')
if __name__=='__main__':unittest.main()
