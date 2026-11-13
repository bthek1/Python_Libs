# Requests and Httpx

Both `requests` and `httpx` are powerful HTTP clients in Python. `requests` is widely used, while `httpx` is an advanced alternative that supports **asynchronous requests** and **HTTP/2**.

Author

Benedict Thekkel

## **1. Installing `requests` and `httpx`**

``` bash
pip install requests httpx
```

------------------------------------------------------------------------

## **2. Basic Usage: GET and POST Requests**

### **Using `requests`**

``` python
import requests

# GET Request
response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
print(response.json())  # Convert response to JSON

# POST Request
data = {"title": "New Task", "completed": False}
response = requests.post("https://jsonplaceholder.typicode.com/todos", json=data)
print(response.status_code, response.json())
```

### **Using `httpx` (Sync)**

``` python
import httpx

# GET Request
response = httpx.get("https://jsonplaceholder.typicode.com/todos/1")
print(response.json())

# POST Request
response = httpx.post("https://jsonplaceholder.typicode.com/todos", json=data)
print(response.status_code, response.json())
```

### **Using `httpx` (Async)**

``` python
import httpx
import asyncio

async def fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        print(response.json())

asyncio.run(fetch())
```

------------------------------------------------------------------------

## **3. Key Differences Between `requests` and `httpx`**

| Feature                | `requests` | `httpx`                |
|------------------------|------------|------------------------|
| **Sync Support**       | ✅ Yes     | ✅ Yes                 |
| **Async Support**      | ❌ No      | ✅ Yes (`AsyncClient`) |
| **HTTP/2 Support**     | ❌ No      | ✅ Yes                 |
| **Connection Pooling** | ❌ No      | ✅ Yes                 |
| **Timeouts**           | ✅ Yes     | ✅ Yes                 |
| **Streaming Support**  | ✅ Yes     | ✅ Yes                 |
| **Cookies & Sessions** | ✅ Yes     | ✅ Yes                 |

------------------------------------------------------------------------

## **4. Handling Headers, Parameters, and Cookies**

``` python
headers = {"Authorization": "Bearer mytoken"}
params = {"search": "python"}

# With requests
response = requests.get("https://api.example.com/data", headers=headers, params=params)
print(response.json())

# With httpx
response = httpx.get("https://api.example.com/data", headers=headers, params=params)
print(response.json())
```

### **Cookies Example**

``` python
# With requests
session = requests.Session()
session.cookies.set("session_id", "abc123")

# With httpx
client = httpx.Client()
client.cookies.set("session_id", "abc123")
```

------------------------------------------------------------------------

## **5. File Uploads**

``` python
files = {"file": open("example.txt", "rb")}

# Using requests
response = requests.post("https://api.example.com/upload", files=files)
print(response.json())

# Using httpx
response = httpx.post("https://api.example.com/upload", files=files)
print(response.json())
```

------------------------------------------------------------------------

## **6. Handling Timeouts and Retries**

``` python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

try:
    response = session.get("https://api.example.com/data", timeout=5)
    print(response.json())
except requests.exceptions.Timeout:
    print("Request timed out!")
```

``` python
import httpx

client = httpx.Client(timeout=httpx.Timeout(10.0))

try:
    response = client.get("https://api.example.com/data")
    print(response.json())
except httpx.TimeoutException:
    print("Request timed out!")
```

------------------------------------------------------------------------

## **7. Authentication (Basic, Token, OAuth)**

### **Basic Authentication**

``` python
from requests.auth import HTTPBasicAuth
import requests

response = requests.get("https://api.example.com/protected", auth=HTTPBasicAuth("user", "pass"))
print(response.status_code)
```

``` python
import httpx

response = httpx.get("https://api.example.com/protected", auth=("user", "pass"))
print(response.status_code)
```

### **Bearer Token Authentication**

``` python
headers = {"Authorization": "Bearer my_token"}
response = requests.get("https://api.example.com/data", headers=headers)
print(response.json())

response = httpx.get("https://api.example.com/data", headers=headers)
print(response.json())
```

------------------------------------------------------------------------

## **8. Handling JSON Responses & Errors**

``` python
try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()  # Raises error if status code is 4xx or 5xx
    data = response.json()
except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")
```

``` python
try:
    response = httpx.get("https://api.example.com/data")
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as err:
    print(f"HTTP Error: {err}")
```

------------------------------------------------------------------------

## **9. Streaming Large Responses**

``` python
# With requests
with requests.get("https://api.example.com/largefile", stream=True) as r:
    for chunk in r.iter_content(chunk_size=1024):
        print(chunk)

# With httpx
with httpx.stream("GET", "https://api.example.com/largefile") as response:
    for chunk in response.iter_bytes():
        print(chunk)
```

------------------------------------------------------------------------

## **10. Using Proxy Servers**

``` python
proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "https://proxy.example.com:8080"
}

# Using requests
response = requests.get("https://api.example.com/data", proxies=proxies)

# Using httpx
response = httpx.get("https://api.example.com/data", proxies=proxies)
```

------------------------------------------------------------------------

## **11. HTTP/2 and Connection Pooling (`httpx` Only)**

``` python
import httpx

# Enable HTTP/2
client = httpx.Client(http2=True)
response = client.get("https://api.example.com/data")
print(response.http_version)  # Should return 'HTTP/2'
```

------------------------------------------------------------------------

## **12. Benchmarking: Speed Comparison**

\`\`\`python import time import requests import httpx

url = “https://jsonplaceholder.typicode.com/todos/1”

# Using requests

start = time.time() requests.get(url) print(“requests:”, time.time() - start)

# Using httpx (sync)

start = time.time() httpx.get(url

------------------------------------------------------------------------

Back to top
