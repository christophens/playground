import unittest
from calculator import main_c

class BasicArithmeticTests(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(main_c('3 + 4.7'), 7.7)
        self.assertEqual(main_c(' +3 + 4.7'), 7.7)
        self.assertEqual(main_c('3 + +4.7'), 7.7)
        self.assertEqual(main_c('3 + (4.7 )'), 7.7)
        self.assertEqual(main_c('3 + (+ 4.7)'), 7.7)
        self.assertEqual(main_c('7.999999999999+0.000000000001'), 8.0)
    
    def test_subtraction(self):
        self.assertEqual(main_c('3 - 4.2'), -1.2)
        self.assertEqual(main_c(' +3 - 4.7'), -1.7)
        self.assertEqual(main_c('3 - +4.7'), -1.7)
        self.assertEqual(main_c('3 - (4.7 )'), -1.7)
        self.assertEqual(main_c('3 - (+ 4.7)'), -1.7)
    
    


if __name__ == '__main__':
    unittest.main()