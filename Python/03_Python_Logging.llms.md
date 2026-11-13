# Python Logging

[Logging doc](https://docs.python.org/3/library/logging.html)

Author

Benedict Thekkel

``` python
import logging
```

``` python
logging.basicConfig(filename='my_logs.log',
                    format='%(asctime)s %(levelname)s [Line:%(lineno)d] [file: %(filename)s]'\
                    '[func: %(funcName)s] [process: %(process)d, %(processName)s]'\
                    '[thread: %(thread)d, %(threadName)s] %(message)s ',
                    filemode='w',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG)
```

``` python
logging.debug('DEBUG')
logging.info('INFO')
logging.warning('WARNING')
logging.error('ERROR')
logging.critical('CRITICAL')
```

``` python
a = 2
```

``` python
b = 55
```

``` python
print("asdfasf")
```

    asdfasf

``` python
x:int = 10 + 10
```

``` python
logging.info(f"The answer is {x}!")
```

``` python
logging.info(f"The answer is {x + a}!")
```

Back to top
