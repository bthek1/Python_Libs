# tqdm

Status bar for for loops

Author

Benedict Thekkel

``` python
!pip list | grep tqdm
```

    tqdm                      4.66.4

``` python
from tqdm import tqdm       # <-- yes
from time import sleep
from tqdm import trange
```

``` python
for i in tqdm(range(100)):  # <-- magic
    sleep(0.01)
```

    100%|██████████████████████████████| 100/100 [00:01<00:00, 96.61it/s]

``` python
for i in trange(100, desc="hello", unit="epoch"):
    sleep(0.01)
```

    hello: 100%|████████████████████| 100/100 [00:01<00:00, 95.96epoch/s]

``` python
with tqdm(total=100) as pbar:
    for i in range(10):
        sleep(0.1)
        pbar.update(10)
```

    100%|██████████████████████████████| 100/100 [00:01<00:00, 98.61it/s]

``` python
pbar = tqdm(total=100)
for i in range(10):
    sleep(0.1)
    pbar.update(10)
pbar.close()
```

    100%|██████████████████████████████| 100/100 [00:01<00:00, 98.64it/s]

## Using with map

``` python
from tqdm import tqdm
import time

def process_item(item):
    time.sleep(0.01)
    return item * 2

results = list(tqdm(map(process_item, range(100)), total=len(range(100))))
```

    100%|██████████████████████████████| 100/100 [00:01<00:00, 95.96it/s]

## Using with Nested Loops

``` python
from tqdm.notebook import tqdm
import time

for i in tqdm(range(5), desc='Outer loop'):
    for j in tqdm(range(100), desc='Inner loop', leave=False):
        time.sleep(0.01)  # Simulate some work being done
```

## Using with Mulitprocessing

``` python
from multiprocessing import Pool
from tqdm import tqdm
import time

def process_item(item):
    time.sleep(0.1)  # Simulate some work being done
    return item * 2

items = range(100)

# Create a Pool with progress bar
with Pool(processes=4) as pool:
    results = list(tqdm(pool.imap(process_item, items), total=len(items)))
```

    100%|██████████████████████████████| 100/100 [00:02<00:00, 39.69it/s]

## Using with Function

``` python
from tqdm.notebook import tqdm
import time

def callback(pbar):
    # Simulate work
    pbar.update(1)

def inner_loop(new_bar):
    for i in range(total):
        time.sleep(0.01)
        new_bar.update(1)
    new_bar.close()
        

total = 10
pbar = tqdm(total=total)


for i in range(total):
    new_bar = tqdm(total=total, leave=False)
    inner_loop(new_bar)
    callback(pbar)

pbar.close()
```

Back to top
