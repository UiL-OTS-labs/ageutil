from unittest import TestCase
from datetime import date

from ageutil import age


class TestAgePredicate(TestCase):

    def test_years_range(self):
        self.assertEqual(age(5).on(1972, 6, 16).range(), (date(1966, 6, 17), date(1967, 6, 16)))

    def test_years_exact_range(self):
        self.assertEqual(age(5, months=0, days=0).on(1972, 6, 16).range(), (date(1967, 6, 16), date(1967, 6, 16)))

    def test_year_to_year_range(self):
        self.assertEqual(age(21).to(22).on(1969, 8, 5).range(),
                         (date(1946, 8, 6), date(1948, 8, 5)))

    def test_months_range(self):
        self.assertEqual(age(0, months=1).on(2000, 6, 1).range(), (date(2000, 4, 2), date(2000, 5, 1)))
