# Datetime

The `datetime` module is Python’s built-in library for handling **dates, times, time zones, and formatting**. It provides powerful features for manipulating and working with dates efficiently.

Author

Benedict Thekkel

## **1. Importing the `datetime` Module**

``` python
import datetime
```

This gives access to various date and time classes:\
- `datetime.date` → Handles **only** dates.\
- `datetime.time` → Handles **only** times.\
- `datetime.datetime` → Handles **both date and time**.\
- `datetime.timedelta` → Represents **time differences**.\
- `datetime.timezone` → Handles **time zones** (replacement for `pytz`).

------------------------------------------------------------------------

## **2. Working with Dates**

The `date` class handles **year, month, and day**.

### **A) Get Today’s Date**

``` python
today = datetime.date.today()
print(today)  # e.g., 2025-01-31
```

### **B) Create a Specific Date**

``` python
d = datetime.date(2025, 1, 31)
print(d)  # 2025-01-31
```

### **C) Extracting Date Components**

``` python
print(d.year)   # 2025
print(d.month)  # 1
print(d.day)    # 31
```

### **D) Formatting a Date**

``` python
formatted_date = d.strftime("%B %d, %Y")
print(formatted_date)  # January 31, 2025
```

> **Common Date Formats:** - `%Y-%m-%d` → `2025-01-31` - `%B %d, %Y` → `January 31, 2025` - `%d/%m/%Y` → `31/01/2025`

------------------------------------------------------------------------

## **3. Working with Time**

The `time` class handles **hours, minutes, seconds, and microseconds**.

### **A) Create a Specific Time**

``` python
t = datetime.time(14, 30, 45)  # 14:30:45
print(t)  # 14:30:45
```

### **B) Extracting Time Components**

``` python
print(t.hour)   # 14
print(tDatetime.minute) # 30
print(t.second) # 45
```

### **C) Formatting Time**

``` python
formatted_time = t.strftime("%I:%M %p")  
print(formatted_time)  # 02:30 PM (12-hour format)
```

------------------------------------------------------------------------

## **4. Working with Date and Time Together**

The `datetime` class represents both **date and time**.

### **A) Get the Current Date & Time**

``` python
now = datetime.datetime.now()
print(now)  # 2025-01-31 14:30:45.123456
```

### **B) Create a Specific Date & Time**

``` python
dt = datetime.datetime(2025, 1, 31, 14, 30, 45)
print(dt)  # 2025-01-31 14:30:45
```

### **C) Extract Components**

``` python
print(dt.year)    # 2025
print(dt.month)   # 1
print(dt.day)     # 31
print(dt.hour)    # 14
print(dt.minute)  # 30
print(dt.second)  # 45
```

### **D) Formatting Date & Time**

``` python
formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_dt)  # 2025-01-31 14:30:45
```

------------------------------------------------------------------------

## **5. Time Differences with `timedelta`**

A `timedelta` represents a duration between two datetime objects.

### **A) Create a `timedelta`**

``` python
delta = datetime.timedelta(days=5, hours=3, minutes=30)
print(delta)  # 5 days, 3:30:00
```

### **B) Add/Subtract a `timedelta`**

``` python
future_date = today + delta
print(future_date)  # 2025-02-05

past_date = today - delta
print(past_date)  # 2025-01-26
```

### **C) Difference Between Two Dates**

``` python
date1 = datetime.date(2025, 2, 10)
date2 = datetime.date(2025, 1, 31)

difference = date1 - date2
print(difference.days)  # 10
```

------------------------------------------------------------------------

## **6. Handling Time Zones (`datetime.timezone`)**

Instead of using `pytz`, Python has **built-in timezone support** using `datetime.timezone`.

### **A) Get UTC Time**

``` python
utc_now = datetime.datetime.now(datetime.timezone.utc)
print(utc_now)  # 2025-01-31 12:00:00+00:00
```

### **B) Define a Fixed Offset Time Zone**

To create a timezone with a fixed UTC offset:

``` python
offset = datetime.timedelta(hours=5, minutes=30)  # UTC+5:30
ist = datetime.timezone(offset, name="IST")

dt = datetime.datetime(2025, 1, 31, 14, 30, tzinfo=ist)
print(dt)  # 2025-01-31 14:30:00+05:30
```

### **C) Convert Between Time Zones**

``` python
utc_now = datetime.datetime.now(datetime.timezone.utc)
ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))  # UTC+5:30

ist_now = utc_now.astimezone(ist)
print(ist_now)  # Converts to IST timezone
```

------------------------------------------------------------------------

## **7. Parsing Strings into `datetime` (`strptime`)**

Convert a string into a `datetime` object:

``` python
date_string = "31-01-2025 14:30"
dt = datetime.datetime.strptime(date_string, "%d-%m-%Y %H:%M")
print(dt)  # 2025-01-31 14:30:00
```

------------------------------------------------------------------------

## **8. Comparing Dates & Times**

``` python
d1 = datetime.date(2025, 1, 31)
d2 = datetime.date(2025, 2, 1)

print(d1 < d2)  # True
print(d1 == d2)  # False
```

For datetime objects:

``` python
dt1 = datetime.datetime(2025, 1, 31, 12, 0)
dt2 = datetime.datetime(2025, 1, 31, 14, 0)

print(dt1 < dt2)  # True
```

------------------------------------------------------------------------

## **9. Generating Timestamps**

### **A) Get the Current Unix Timestamp**

``` python
timestamp = datetime.datetime.now().timestamp()
print(timestamp)  # e.g., 1738293600.123456
```

### **B) Convert Timestamp to `datetime`**

``` python
dt_from_timestamp = datetime.datetime.fromtimestamp(1738293600)
print(dt_from_timestamp)
```

------------------------------------------------------------------------

## **10. Using `datetime` in JSON Serialization**

Python’s `datetime` is **not JSON serializable** by default:

``` python
import json

now = datetime.datetime.now()
json.dumps({"timestamp": now})  # TypeError: Object of type datetime is not JSON serializable
```

### **Solution: Convert to String**

``` python
json.dumps({"timestamp": now.isoformat()})
```

### **Solution: Convert to Unix Timestamp**

``` python
json.dumps({"timestamp": now.timestamp()})
```

------------------------------------------------------------------------

## **Summary**

| Feature                | Code Example                                   |
|------------------------|------------------------------------------------|
| Get Today’s Date       | `datetime.date.today()`                        |
| Get Current Time       | `datetime.datetime.now().time()`               |
| Create a Date          | `datetime.date(2025, 1, 31)`                   |
| Create a Time          | `datetime.time(14, 30, 45)`                    |
| Get Date & Time        | `datetime.datetime.now()`                      |
| Format Date            | `.strftime("%Y-%m-%d")`                        |
| Convert String to Date | `.strptime("31-01-2025", "%d-%m-%Y")`          |
| Add 5 Days             | `date + timedelta(days=5)`                     |
| Get UTC Time           | `datetime.datetime.now(datetime.timezone.utc)` |
| Convert Time Zones     | `.astimezone(new_timezone)`                    |

------------------------------------------------------------------------

## **Conclusion**

- `datetime` is Python’s **built-in solution** for working with dates and times.
- `datetime.timezone` (not `pytz`) provides **native timezone handling**.
- `timedelta` helps **add/subtract time**.
- **String parsing (`strptime`) and formatting (`strftime`)** are essential for conversions.
- **Always consider time zones when working with global applications**.

This guide covers everything you need to master `datetime`! 🚀

------------------------------------------------------------------------

Back to top
