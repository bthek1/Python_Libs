# Mito

Python Spreadsheet

Author

Benedict Thekkel

``` python
!pip list | grep mitosheet
```

    mitosheet                     0.1.530

``` python
import mitosheet
```

``` python
mitosheet.sheet(analysis_to_replay="id-qdjqkelpwx")
```

``` python
from mitosheet.public.v3 import *; # Analysis Name:id-qdjqkelpwx;
import pandas as pd

# Imported salaries.csv
salaries = pd.read_csv(r'/home/ben/BENEDICT_Only/Benedict_Projects/Benedict_ML/ML/nbs/Data/salaries.csv')

# sort the column company in ascending order
salaries.sort_values('company', ascending=True, inplace=True)
```

Back to top
