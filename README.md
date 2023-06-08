# SQLStatementLength
Determine the length of a variable SQL statement.

**Language: Python**

**Start: 2023**

## Why
I found out that SQL statements for [SQLite](https://www.sqlite.org/limits.html) have a limit of 1,000,000,000 characters ([SQLITE_MAX_SQL_LENGTH](https://github.com/sqlite/sqlite/blob/master/src/sqliteLimit.h)). I had a query like this:

```sql
SELECT NAME, DESCRIPTION, V_0, V_1, ... V_100 FROM TABLE WHERE ID IN (3,9,54,200)
```

where the number of columns like _V\_0_ can change, but it is limited to a maximum of 100 while the number of _IDs_ has no real limit. I wanted to find out how many IDs it takes for the statement to reach the limit of _SQLITE_MAX_SQL_LENGTH_.

## Calculations
To determine the length (_L_) of the SQL statement based on the number of IDs (_n_), first we define:

$$f = length(fixed)$$

$$g = length(conj)$$

where the _fixed_ if the non-changing part of the SQL statement and _conj_ in this case is the comma. And now we can write L as:

$$L = f + \sum_{i=1}^n (g + \lfloor \log_{10} i \rfloor + 1) - g$$

where the floored _log_ + 1 represents the number of digits in the number and the subtraction of _g_ accounts for the comma after the last ID which should not be included. We can now write a simplified version of this formula to determine the upper bound L1:

$$L1 > L$$

$$L1 = f + \sum_{i=1}^n (g + \log_{10} i + 1) - g$$

$$L1 = f - g + \sum_{i=1}^n (g + 1) + \sum_{i=1}^n \log_{10} i$$

And since we know that:

$$\log a + \log b = \log (a + b)$$

We can finally write:

$$L1 = f - g + n \cdot (g + 1) + \log_{10} (n!)$$

## Implementations of L and L1
I implemented a few versions of this calculation with different level of precisions and calculation times. For _n_ equals to 100,000:

 Method     | Time (ms) | Result
------------|-----------|------------
LString     | 1253      | 589,435        
L           | 90        | 589,435
L1          | 219       | 657,113
L1Sterling  | 0         | 600,542
L1Ramanujan | 0         | 600,542

Where _LString_ calculates _L_ by composing the SQL string, _L_ and _L1_ apply the aforementioned calculations and _L1Sterling_ and _L1Ramanujan_ calculate _L1_ with approximations of the log factorial:

$$ \log_{10} (n!) \approx logSterling = n \cdot \log_{10} n - n + \frac{1}{2} \cdot \log_{10} (2 \cdot \pi \cdot n) + \frac{1}{12 \cdot n} - \frac{1}{360 \cdot n^3} $$

$$ \log_{10} (n!) \approx logRamanujan = n \cdot \log_{10} n - n + \frac{1}{6} \cdot \log_{10}(8 \cdot n^3 + 4 \cdot n^2 + n + 1/30) + \frac{1}{2} \cdot \log_{10} \pi $$

Both approximations are defined in the [Stirling's approximation Wikipedia page](https://en.wikipedia.org/wiki/Stirling%27s_approximation#Versions_suitable_for_calculators).

The calculation of some of these methods slows down drammatically as _n_ increases. Therefore, for _n_ equals to 115,000,000 I only calculated some of them:

 Method     | Time (ms) | Result
------------|-----------|---------------
L           | 66661     | 1,038,892,962
L1Sterling  | 0         | 1,041,984,320
L1Ramanujan | 0         | 1,041,984,320
