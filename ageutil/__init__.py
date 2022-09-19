import datetime
from typing import Optional, Union
from calendar import monthrange


def month_diff(a: datetime.date, b: datetime.date):
    diff = b - a
    days = abs(diff.days)
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

    return months * sign, days


def month_add(d: datetime.date, months: int):
    for i in range(months):
        days_in_month = monthrange(d.year, d.month)[1]
        d += datetime.timedelta(days=days_in_month)
    return d


class AgePredicate:
    def __init__(self, years, months, days):
        self.lower = (years or 0,
                      months if months is not None else 0,
                      days if days is not None else 0)
        self.upper = (years + 1 if (years is not None and months is None) else (years or 0),
                      months + 1 if (months is not None and days is None) else (months or 0),
                      days if days is not None else -1)

        self._on = datetime.date.today()

    def __call__(self, date):
        return self.check(date)

    def check(self, date):
        upper, lower = self.range()
        return (upper is None or date >= upper) and (lower is None or date <= lower)

    def on(self, on: Union[datetime.date, int], month: Optional[int] = None, day: Optional[int] = None):
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
            lower = datetime.date(self._on.year - self.lower[0],
                                  (self._on.month - 1 - self.lower[1]) % 12 + 1,
                                  self._on.day) - datetime.timedelta(self.lower[2])

        if self.upper is not None:
            upper = datetime.date(self._on.year - self.upper[0],
                                  (self._on.month - 1 - self.upper[1]) % 12 + 1,
                                  self._on.day) - datetime.timedelta(self.upper[2])
        return (upper, lower)

    def to(self, years: Optional[int] = None, months: Optional[int] = None,
           days: Optional[int] = None):
        self.upper = (years + 1 if (years is not None and months is None) else (years or 0),
                      months + 1 if (months is not None and days is None) else (months or 0),
                      days if days is not None else -1)
        return self

    def or_older(self):
        self.upper = None
        return self

    def or_younger(self):
        self.lower = None
        return self


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

    def on(self, on: Union[datetime.date, int], month: Optional[int] = None, day: Optional[int] = None):
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
        lower = self.dob + datetime.timedelta(days=(pred.lower[0] * 365 + pred.lower[2]))
        lower = month_add(lower, pred.lower[1])
        upper = self.dob + datetime.timedelta(days=(pred.upper[0] * 365 + pred.upper[2]))
        upper = month_add(upper, pred.upper[1])
        return (lower, upper)


def age(years: Optional[int] = None, *, months: Optional[int] = None,
        days: Optional[int] = None) -> AgePredicate:
    return AgePredicate(years, months, days)


def dob(year: Union[datetime.date, int], month: Optional[int] = None, day: Optional[int] = None):
    return AgeCalc(year, month, day)
