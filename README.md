# ageutil
Python library for age and birthday related calculations

Intended to match how humans think about age.

## Examples

### Birthday ranges

```python
from ageutil import age
```

What's the range of possible birthdays for people who are 18 years old today?

```python
age(18).range()
```

What's the range of possible birthdays for people who are 18-21 years old today?

```python
age(18).to(21).range()
```

Same question but for 2 to 3 month old babies?

```python
age(months=2).to(months=3).range()
```

What's the range of possible birthdays for people who were younger than 12 when the Berlin wall was torn down?

```python
age(12).or_younger().on(1989, 11, 9).range()
```


### Age calculation

```python
from ageutil import date_of_birth
```

What's the exact age (years, months, days) of someone born on the first day of 2000?

```python
date_of_birth(2000, 1, 1).age_ymd()
```

During what date range was that person between 3 to 6 years old?

```python
date_of_birth(2000, 1, 1).range_for(age(3).to(6))
```


### Testing age

There are several options for checking whether a person's age falls within a certain range:

```python
from datetime import date
from ageutil import age
age_pred = age(2).to(3).on(2021, 1, 1)

age_pred(date(2019, 1, 1))  # True
age_pred.check(date(2019, 1, 1))  # True
date(2019, 1, 1) in age_pred  # True
```
