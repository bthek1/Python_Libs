# Python args

[argparse](https://docs.python.org/3/library/argparse.html)

Author

Benedict Thekkel

``` python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print(f"the square of {args.square} equals {answer}")
else:
    print(answer)
```

``` bash
>> python prog.py
usage: prog.py [-h] [-v] square
prog.py: error: the following arguments are required: square

>> python prog.py 4
16

>> python prog.py 4 --verbose
the square of 4 equals 16

>> python prog.py --verbose 4
the square of 4 equals 16
```

``` python
!cat 9_argparse_example.py
```

    import argparse
    from datetime import datetime

    def reformat_date(date_string):
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        return date_object.strftime('%Y-%m-%dT%H:%M:%SZ')

    def main(start, end):
        if start != None:
            print("Argument 1:", reformat_date(start))
        if end != None:
            print("Argument 2:", reformat_date(end))

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="""Create models for users
        Ex. python test.py -s 19/03/2024 -e 19/07/2024""")
        parser.add_argument("-s", "--start_date", type=str, help="Start Date ex. '19/03/2024'")
        parser.add_argument("-e", "--end_date", type=str, help="End Date ex. '19/07/2024'")
        args = parser.parse_args()
        main(args.start_date, args.end_date)

``` python
!python 9_argparse_example.py -h
```

    usage: 9_argparse_example.py [-h] [-s START_DATE] [-e END_DATE]

    Create models for users Ex. python test.py -s 19/03/2024 -e 19/07/2024

    options:
      -h, --help            show this help message and exit
      -s START_DATE, --start_date START_DATE
                            Start Date ex. '19/03/2024'
      -e END_DATE, --end_date END_DATE
                            End Date ex. '19/07/2024'

``` python
!python 9_argparse_example.py -s 01/01/2023 -e 01/01/2024
```

    Argument 1: 2023-01-01T00:00:00Z
    Argument 2: 2024-01-01T00:00:00Z

``` python
!cat 9_sys_example.py
```

    import sys
     
    # total arguments
    n = len(sys.argv)
    print("Total arguments passed:", n)
     
    # Arguments passed
    print("\nName of Python script:", sys.argv[0])
     
    print("\nArguments passed:", end = " ")
    for i in range(1, n):
        print(sys.argv[i], end = " ")
         
    # Addition of numbers
    Sum = 0
    # Using argparse module
    for i in range(1, n):
        Sum += int(sys.argv[i])
         
    print("\n\nResult:", Sum)

``` python
!python 9_sys_example.py 1 2
```

    Total arguments passed: 3

    Name of Python script: 9_sys_example.py

    Arguments passed: 1 2 

    Result: 3

``` python
a = []
```

``` python
a[1] = 1
```

    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)
    Cell In[1], line 1
    ----> 1 a[1] = 1

    NameError: name 'a' is not defined

``` python
a
```

    [1, 1, 3]

Back to top
