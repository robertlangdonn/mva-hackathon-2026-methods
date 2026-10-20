import gzip
import unittest
from scripts.public_niacin_intake import unpack, FILES
from scripts.public_niacin_descriptive import paired_effect


class PublicIntakeTests(unittest.TestCase):
    def test_small_gzip(self):
        self.assertEqual(unpack(gzip.compress(b'a\tb\n1\t2\n')), 'a\tb\n1\t2\n')

    def test_not_gzip_rejected(self):
        with self.assertRaises(gzip.BadGzipFile):
            unpack(b'<html>not a data file</html>')

    def test_only_public_processed_inputs(self):
        self.assertEqual(len(FILES), 2)
        self.assertTrue(all(url.startswith('https://ftp.ncbi.nlm.nih.gov/geo/series/GSE129nnn/GSE129811/') for url in FILES.values()))
        self.assertTrue(all('/soft/' in url or '/suppl/' in url for url in FILES.values()))

    def test_paired_effect(self):
        result = paired_effect([1, 3], [3, 7])
        self.assertEqual(result['median_log2_change'], 1)
        self.assertEqual(result['positive_pairs'], 2)

    def test_zeros_are_not_positive_evidence(self):
        result = paired_effect([0, 0], [0, 0])
        self.assertEqual(result['median_log2_change'], 0)
        self.assertEqual(result['positive_pairs'], 0)

    def test_pair_lengths(self):
        for a, b in [([], []), ([1], [1, 2])]:
            with self.assertRaises(ValueError):
                paired_effect(a, b)


if __name__ == '__main__':
    unittest.main()
