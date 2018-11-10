from unittest import TestCase

from whenthen import whenthen


class ProfileTest(TestCase):

    def test_whenthen_base(self):
        @whenthen
        def fract(x):
            return x * fract(x - 1)

        @fract.when
        def fract_when_eq_0(x):
            return x == 0

        @fract.then
        def fract_then_eq_0(x):
            return 1

        @fract.when
        def fract_when_higher_5(x):
            return x > 5

        @fract.then
        def fract_then_higher_5(x):
            return fract(5)

        print(fract)
        self.assertEqual(1, fract(0))
        self.assertEqual(1, fract(1))
        self.assertEqual(fract(5), fract(10))
