from unittest import TestCase
from datetime import date

from ageutil import age, date_of_birth as dob


class TestAgeCalc(TestCase):

    def test_dob_age(self):
        self.assertEqual(dob(1995, 11, 27).on(2000, 1, 1).age(), 4)

    def test_dob_age_ymd(self):
        self.assertEqual(
            dob(2000, 1, 1).on(2020, 12, 31).age_ymd(),
            (21, 11, 30))

    def test_dob_range_for(self):
        self.assertEqual(
            dob(2000, 5, 1).range_for(age(1).to(2)),
            (date(2001, 5, 1), date(2003, 4, 30)))

        self.assertEqual(
            dob(2000, 5, 1).range_for(age(1).to(2, 6)),
            (date(2001, 5, 1), date(2002, 11, 30)))

        self.assertEqual(
            dob(2000, 5, 1).range_for(age(1, months=1, days=1).to(2, 6, 15)),
            (date(2001, 6, 2), date(2002, 11, 16)))

    def test_dob_range_for_unlimited(self):
        self.assertEqual(
            dob(2000, 5, 1).range_for(age(1).or_older()),
            (date(2001, 5, 1), None))
        self.assertEqual(
            dob(2000, 5, 1).range_for(age(1).or_younger()),
            (None, date(2002, 4, 30)))

        self.assertEqual(
            dob(2000, 5, 1).range_for(age(None).to(None)),
            (None, None))
