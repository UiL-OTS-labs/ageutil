from unittest import TestCase
from datetime import date

from ageutil import dob


class TestAgeCalc(TestCase):

    def test_dob_age(self):
        self.assertEqual(dob(1995, 11, 27).on(2000, 1, 1).age(), 4)
