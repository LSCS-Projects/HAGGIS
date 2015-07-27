import unittest
import numpy as np
from app_models import m_spatial

class Test_spatial(unittest.TestCase):
    def test_calculate_point_density(self):
        points = np.array([(1, 2), (3, 4), (4, 5), (100,100)])
        ids = ['p1','p2','p3','p4']
        res_density = [50.0,
                       75.0,
                       50.0,
                       25.0]
        model = m_spatial.SpatialTools()
        result = model.calculate_point_density(points,ids, 3.0)
        gold = zip(ids, res_density)
        self.assertEqual(result, gold)

if __name__ == '__main__':
    unittest.main()
