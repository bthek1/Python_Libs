# Python Multiprocessing

[Multiprocessing doc](https://docs.python.org/3/library/multiprocessing.html)

Author

Benedict Thekkel

## Pool

``` python
from multiprocessing import Pool
```

``` python
Pool??
```

    Signature: Pool(processes=None, initializer=None, initargs=(), maxtasksperchild=None)
    Source:   
        def Pool(self, processes=None, initializer=None, initargs=(),
                 maxtasksperchild=None):
            '''Returns a process pool object'''
            from .pool import Pool
            return Pool(processes, initializer, initargs, maxtasksperchild,
                        context=self.get_context())
    File:      ~/mambaforge/envs/cfast/lib/python3.11/multiprocessing/context.py
    Type:      method

``` python
def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
```

    [1, 4, 9]

## Process

``` python
from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

    main line
    module name: __main__
    parent process: 2121
    process id: 50591
    function f
    module name: __main__
    parent process: 50591
    process id: 50750
    hello bob

## Queues

``` python
from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
```

    [42, None, 'hello']

## Pipes

``` python
from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```

    [42, None, 'hello']

## Lock

``` python
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

    hello world
     0hello world 1
    hello world2 
     hello world3
    hello world 4
    hello world 5
    hello world 6
    hello world 7
    hello world 8
    hello world 9

## Shared memory

``` python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

    3.1415927
    [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]

## Server process

``` python
from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)
```

    {1: '1', '2': 2, 0.25: None}
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

Back to top
