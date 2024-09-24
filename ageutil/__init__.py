import datetime
from collections import namedtuple
from typing import Optional, Union, Tuple
from calendar import monthrange


MonthSpan = namedtuple('MonthSpan', 'months, days')
DateSpan = namedtuple('DateSpan', 'years, months, days')


def month_diff(a: datetime.date, b: datetime.date) -> MonthSpan:
    diff = b - a
    days = abs(diff.days)
    if diff.days == 0:
        return MonthSpan(0, 0)

    sign = days // diff.days
    month = (min(a, b)).month
    year = (min(a, b)).year
    months = 0

    while True:
        days_in_month = monthrange(year, month)[1]
        if days < days_in_month:
            # no whole months left
            break

        days -= days_in_month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        months += 1

    return MonthSpan(months * sign, days)


def month_add(d: datetime.date, months: int) -> datetime.date:
    """returns date that is `months` months in the future/past"""
    if months == 0:
        return d

    backwards = months < 0
    months = abs(months)

    for i in range(months):
        if backwards:
            days_in_month = monthrange(d.year, 1 + (d.month - 2) % 12)[1]
            d += datetime.timedelta(days=-days_in_month)
        else:
            days_in_month = monthrange(d.year, d.month)[1]
            d += datetime.timedelta(days=days_in_month)
    return d


class AgePredicate:
    lower: Optional[DateSpan]
    upper: Optional[DateSpan]

    def __init__(self, years: Optional[int], months: Optional[int], days: Optional[int]):
        self.lower, self.upper = None, None

        if years is not None or months is not None or days is not None:
            self.lower = DateSpan(years or 0,
                                  months if months is not None else 0,
                                  days if days is not None else 0)
            self.upper = DateSpan(
                years + 1 if (years is not None and months is None) else (years or 0),
                months + 1 if (months is not None and days is None) else (months or 0),
                days if days is not None else -1)

        self._on = datetime.date.today()

    def __call__(self, date: datetime.date) -> bool:
        return self.check(date)

    def check(self, date: datetime.date):
        if date is None:
            raise TypeError('date cannot be None')
        upper, lower = self.range()
        return (upper is None or date >= upper) and (lower is None or date <= lower)

    def on(self, on: Union[datetime.date, int], month: Optional[int] = None,
           day: Optional[int] = None):
        if isinstance(on, int):
            if month is None or day is None:
                raise TypeError()
            self._on = datetime.date(on, month, day)
        else:
            if not isinstance(on, datetime.date):
                raise TypeError()
            self._on = on
        return self

    def range(self):
        upper, lower = None, None
        if self.lower is not None:
            lower = datetime.date(self._on.year - self.lower.years,
                                  self._on.month,
                                  self._on.day) - datetime.timedelta(self.lower.days)
            lower = month_add(lower, -self.lower.months)

        if self.upper is not None:
            upper = datetime.date(self._on.year - self.upper.years,
                                  self._on.month,
                                  self._on.day) - datetime.timedelta(self.upper.days)
            upper = month_add(upper, -self.upper.months)
        return (upper, lower)

    def to(self, years: Optional[int] = None, months: Optional[int] = None,
           days: Optional[int] = None):
        if years is None and months is None and days is None:
            return self.or_older()

        self.upper = DateSpan(years + 1 if (years is not None and months is None) else (years or 0),
                              months + 1 if (months is not None and days is None) else (months or 0),
                              days if days is not None else -1)
        return self

    def or_older(self):
        self.upper = None
        return self

    def or_younger(self):
        self.lower = None
        return self

    def __contains__(self, date: datetime.date):
        return self.check(date)


class AgeCalc:
    def __init__(self, year: Union[datetime.date, int], month: Optional[int] = None,
                 day: Optional[int] = None):
        if isinstance(year, datetime.date):
            self.dob = year
        else:
            if month is None or day is None:
                raise TypeError()
            self.dob = datetime.date(year, month, day)

        self._on = datetime.date.today()

    def on(self, on: Union[datetime.date, int], month: Optional[int] = None,
           day: Optional[int] = None):
        if isinstance(on, int):
            if month is None or day is None:
                raise TypeError()
            self._on = datetime.date(on, month, day)
        else:
            if not isinstance(on, datetime.date):
                raise TypeError()
            self._on = on
        return self

    def _age_full(self):
        diff = month_diff(self.dob, self._on)
        return ((self._on - self.dob).days // 365, diff[0] % 12, diff[1])

    def age(self):
        return self._age_full()[0]

    def age_ym(self):
        return self._age_full()[:2]

    def age_ymd(self):
        return self._age_full()

    def range_for(self, pred: AgePredicate):
        upper, lower = None, None
        if pred.lower is not None:
            lower = self.dob
            lower = month_add(lower, pred.lower.months + pred.lower.years * 12)
            lower += datetime.timedelta(days=pred.lower.days)

        if pred.upper is not None:
            upper = self.dob
            upper = month_add(upper, pred.upper.months + pred.upper.years * 12)
            upper += datetime.timedelta(days=pred.upper.days)

        return (lower, upper)


def age(years: Optional[int] = None, *, months: Optional[int] = None,
        days: Optional[int] = None) -> AgePredicate:
    return AgePredicate(years, months, days)


def date_of_birth(year: Union[datetime.date, int], month: Optional[int] = None,
                  day: Optional[int] = None) -> AgeCalc:
    return AgeCalc(year, month, day)
