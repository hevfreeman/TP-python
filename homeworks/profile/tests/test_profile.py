
from unittest import TestCase
import time
from profile import profile


class ProfileTest(TestCase):
    def test_profile_base(self):
        @profile
        def foo():
            pass
        foo()

    def test_profile_class(self):
        @profile
        class Bar:
            def __init__(self):
                pass
        Bar()

    def test_profile_args(self):
        @profile
        def pri(x, y):
            print(x, y)
            time.sleep(1)
            print(y, x)
        pri(1, 2)

    def test_profile_with_return(self):
        @profile
        def sq(x):
            time.sleep(0.5)
            return x**2
        self.assertEqual(9, sq(3))
