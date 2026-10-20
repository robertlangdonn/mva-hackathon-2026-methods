import unittest
from scripts.public_niacin_sensitivity import sensitivity, read_table


class SensitivityTests(unittest.TestCase):
    def test_constant_doubling(self):
        r = sensitivity([2,4,8], [4,8,16], 0)
        self.assertEqual(r['median_log2_change'],1)
        self.assertEqual(r['loo_median_range'],[1,1])

    def test_influential_pair(self):
        r = sensitivity([1,1,1], [0.5,0.5,16], 0)
        self.assertEqual(r['positive_pairs'],1)
        self.assertEqual(r['loo_median_range'],[-1,1.5])

    def test_zeros(self):
        self.assertEqual(sensitivity([0,1],[1,1],0)['status'],'undefined_zero_count')
        self.assertEqual(sensitivity([0,0],[0,0],1)['median_log2_change'],0)

    def test_bad_pairs(self):
        for a,b in [([],[]),([1],[2]),([1,2],[3]),([1,-1],[1,2]),([1,float('nan')],[1,2])]:
            with self.assertRaises(ValueError): sensitivity(a,b,1)

    def test_matrix_validation(self):
        for value in ['id,gene,s\nx,A,-1\n', 'id,gene,s\nx,A,1\nx,A,2\n', 'id,gene,s\nx,A,nan\n', 'id,gene,s\nx,A\n']:
            with self.assertRaises(ValueError): read_table(value,',')

    def test_valid_table(self):
        cols,data=read_table('id,gene,s\nx,A,2\n',',')
        self.assertEqual(cols,['s']); self.assertEqual(data['x'],('A',[2.0]))
