# Pivot Tables js

Pivot Tables js

Author

Benedict Thekkel

``` python
import pandas as pd
from pivottablejs import pivot_ui
import ipypivot as pt

df = pd.read_csv('Data/salaries.csv')
df.head()
```

|     | company | job                 | degree    | salary_more_then_100k |
|-----|---------|---------------------|-----------|-----------------------|
| 0   | google  | sales executive     | bachelors | 0                     |
| 1   | google  | sales executive     | masters   | 0                     |
| 2   | google  | business manager    | bachelors | 1                     |
| 3   | google  | business manager    | masters   | 1                     |
| 4   | google  | computer programmer | bachelors | 0                     |

``` python
pivot_ui(df)
```

Back to top
