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

        # also test wrap around to previous year
        self.assertEqual(age(0, months=1).on(2000, 1, 1).range(), (date(1999, 11, 2), date(1999, 12, 1)))

    def test_months_more_than_12(self):
        self.assertTrue(
            age(months=24).on(2022, 1, 1).check(date(2020, 1, 1)))

    def test_age_contains_date(self):
        self.assertTrue(
            date(2000, 1, 1) in age(1, months=0, days=0).on(2001, 1, 1))
        self.assertFalse(
            date(2000, 1, 1) in age(2, months=0, days=0).on(2001, 1, 1))
