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
age(18, 21).range()
```

Same question but for 2 to 3 month old babies?

```python
age(months=2).to(months=3).range()
```

What's the range of possible birthdays for people who were younger than 12 when the Berlin wall torn down?

```python
age(12).or_younger().on(1989, 11, 9).range()
```


### Age calculation

```python
from ageutil import dob
```

What's the exact age (years, months, days) of someone born on the first day of 2000?

```python
dob(2000, 1, 1).age_ymd()
```

During what date range was that person between 3 to 6 years old?

```python
dob(2000, 1, 1).range_for(age(3).to(6))
```
