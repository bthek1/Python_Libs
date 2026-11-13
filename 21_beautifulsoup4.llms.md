# BeautifulSoup4

BeautifulSoup4 (bs4) is a Python library for parsing HTML and XML documents, commonly used for web scraping.

Author

Benedict Thekkel

## Installation

``` bash
pip install beautifulsoup4
pip install lxml  # recommended parser
```

------------------------------------------------------------------------

## Parsers

| Parser             | Install                | Speed  | Leniency     |
|--------------------|------------------------|--------|--------------|
| `html.parser`      | built-in               | medium | lenient      |
| `lxml`             | `pip install lxml`     | fast   | lenient      |
| `lxml-xml` / `xml` | `pip install lxml`     | fast   | strict       |
| `html5lib`         | `pip install html5lib` | slow   | most lenient |

``` python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "lxml")        # recommended
soup = BeautifulSoup(html, "html.parser") # no deps
soup = BeautifulSoup(xml, "lxml-xml")     # for XML
```

------------------------------------------------------------------------

## Core Objects

| Type              | Description                                |
|-------------------|--------------------------------------------|
| `BeautifulSoup`   | Root document object, subclass of `Tag`    |
| `Tag`             | An HTML/XML tag and its contents           |
| `NavigableString` | Text inside a tag                          |
| `Comment`         | HTML comment (subclass of NavigableString) |

------------------------------------------------------------------------

## Finding Elements

**Primary methods** — work on both `BeautifulSoup` and `Tag` objects:

``` python
# find — returns first match or None
soup.find("div")
soup.find("a", class_="link")
soup.find("input", {"type": "text"})

# find_all — returns list (alias: findAll)
soup.find_all("p")
soup.find_all(["h1", "h2", "h3"])
soup.find_all("a", limit=5)
soup.find_all(True)  # all tags

# CSS selectors
soup.select("div.container > p")
soup.select_one("a[href]")
soup.select("ul li:nth-of-type(2)")

# By attribute
soup.find_all(id="main")
soup.find_all(class_="active")          # class_ avoids keyword clash
soup.find_all(attrs={"data-id": "42"})
```

**Regex and functions as filters:**

``` python
import re
soup.find_all("a", href=re.compile(r"^https"))
soup.find_all(re.compile(r"^h[1-6]$"))  # all headings

# Function filter
soup.find_all(lambda tag: tag.has_attr("data-custom") and tag.name == "div")
```

------------------------------------------------------------------------

## Navigating the Tree

``` python
tag = soup.find("div")

# Children / descendants
tag.children        # direct children (iterator)
tag.descendants     # all nested (iterator)
tag.contents        # direct children (list)
list(tag.strings)   # all text strings, nested
list(tag.stripped_strings)  # stripped, no empty strings

# Parents
tag.parent
list(tag.parents)   # all ancestors up to document

# Siblings
tag.next_sibling
tag.previous_sibling
list(tag.next_siblings)
list(tag.previous_siblings)

# Parsed tree order
tag.next_element
tag.previous_element
```

------------------------------------------------------------------------

## Accessing Attributes & Text

``` python
tag = soup.find("a")

# Attributes
tag["href"]               # KeyError if missing
tag.get("href")           # None if missing
tag.get("class", [])      # class is always a list
tag.attrs                 # dict of all attributes
tag.has_attr("id")

# Text content
tag.string      # NavigableString if single text node, else None
tag.get_text()  # all text concatenated
tag.get_text(separator=" ", strip=True)
```

------------------------------------------------------------------------

## Modifying the Tree

``` python
tag["class"] = "new-class"
tag["data-x"] = "value"
del tag["id"]

tag.string.replace_with("new text")
tag.append(new_tag)
tag.insert(0, new_tag)
tag.insert_before(sibling)
tag.insert_after(sibling)

tag.decompose()       # remove tag + contents from tree, destroys it
tag.extract()         # remove and return tag (reusable)
tag.replace_with(other_tag)

# Create new tags
new_tag = soup.new_tag("a", href="https://example.com")
new_tag.string = "Click here"
soup.body.append(new_tag)

new_string = soup.new_string("some text")
```

------------------------------------------------------------------------

## Output

``` python
str(soup)           # full HTML string
soup.prettify()     # indented, unicode output
soup.encode("utf-8")

tag.decode()        # tag as string
tag.encode()        # tag as bytes
```

------------------------------------------------------------------------

## Common Patterns

**Scraping links:**

``` python
for a in soup.find_all("a", href=True):
    print(a["href"], a.get_text(strip=True))
```

**Scraping a table:**

``` python
rows = soup.select("table tbody tr")
data = [[td.get_text(strip=True) for td in row.find_all("td")] for row in rows]
```

**From a URL (with requests):**

``` python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://example.com", headers={"User-Agent": "Mozilla/5.0"})
r.raise_for_status()
soup = BeautifulSoup(r.text, "lxml")
```

**From a file:**

``` python
with open("page.html", "rb") as f:
    soup = BeautifulSoup(f, "lxml")
```

------------------------------------------------------------------------

## Gotchas

- **`class_`** not `class` — Python keyword conflict.
- **`tag.string` is `None`** if a tag has multiple children — use `get_text()` instead.
- **`class` is a list** — `tag["class"]` returns `["foo", "bar"]`, not `"foo bar"`. Use `tag.get("class", [])` and check membership or join to compare.
- **Whitespace siblings** — `tag.next_sibling` is often a `NavigableString` of whitespace (`"\n"`). Filter with `tag.find_next_sibling("div")` instead.
- **Parser differences** — `html.parser` and `lxml` can produce different trees for malformed HTML. Pick one and stick to it.
- **`find_all` is not lazy** — it walks the whole tree. For large docs, use `limit=` or `select_one` where possible.
- **`SoupStrainer`** — parse only a subset of the document for performance:

``` python
from bs4 import SoupStrainer

only_links = SoupStrainer("a")
soup = BeautifulSoup(html, "lxml", parse_only=only_links)
```

------------------------------------------------------------------------

``` python
import subprocess
import sys

# Install beautifulsoup4 and lxml if needed
try:
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "lxml", "-q"])
    from bs4 import BeautifulSoup

print("BeautifulSoup4 imported successfully")
```

    ✓ BeautifulSoup4 imported successfully

``` python
# Example 1: Basic HTML Parsing
html_string = """
<html>
    <body>
        <div class="container">
            <h1>Welcome to BeautifulSoup</h1>
            <p class="intro">This is an introduction paragraph.</p>
            <ul>
                <li><a href="https://example.com">Example Link</a></li>
                <li><a href="https://python.org">Python</a></li>
                <li><a href="https://github.com">GitHub</a></li>
            </ul>
        </div>
    </body>
</html>
"""

soup = BeautifulSoup(html_string, "lxml")
print("Parsed HTML document:")
print(soup.prettify()[:300] + "...\n")
```

    Parsed HTML document:
    <html>
     <body>
      <div class="container">
       <h1>
        Welcome to BeautifulSoup
       </h1>
       <p class="intro">
        This is an introduction paragraph.
       </p>
       <ul>
        <li>
         <a href="https://example.com">
          Example Link
         </a>
        </li>
        <li>
         <a href="https://python.org">
          Pyt...

``` python
# Example 2: Finding Elements
print("=== Finding Elements ===\n")

# find() - returns first match
h1 = soup.find("h1")
print(f"First h1: {h1}")

# find_all() - returns list
links = soup.find_all("a")
print(f"All links found: {len(links)}")
for link in links:
    print(f"  - {link.get_text()}: {link.get('href')}")

# CSS selectors
container = soup.select_one("div.container")
print(f"Container found: {container.name if container else 'None'}")

# By attribute
paragraphs = soup.find_all("p", class_="intro")
print(f"Paragraphs with class 'intro': {len(paragraphs)}")
```

    === Finding Elements ===

    First h1: <h1>Welcome to BeautifulSoup</h1>
    All links found: 3
      - Example Link: https://example.com
      - Python: https://python.org
      - GitHub: https://github.com
    Container found: div
    Paragraphs with class 'intro': 1

``` python
# Example 3: Navigating the Tree
print("\n=== Navigating the Tree ===\n")

# Get the first link
first_link = soup.find("a")
print(f"First link: {first_link.get_text()}")

# Parent navigation
parent = first_link.parent
print(f"Parent tag: {parent.name}")  # li

# Siblings navigation
next_sibling = first_link.next_sibling
print(f"Next sibling (text): {repr(next_sibling)}")

next_tag_sibling = first_link.find_next_sibling("a")
print(f"Next <a> sibling: {next_tag_sibling.get_text() if next_tag_sibling else 'None'}")

# Descendants
container = soup.find("div", class_="container")
all_text = list(container.stripped_strings)
print(f"All text in container: {all_text[:5]}...")
```

    === Navigating the Tree ===

    First link: Example Link
    Parent tag: li
    Next sibling (text): None
    Next <a> sibling: None
    All text in container: ['Welcome to BeautifulSoup', 'This is an introduction paragraph.', 'Example Link', 'Python', 'GitHub']...

``` python
# Example 4: Accessing Attributes & Text
print("\n=== Accessing Attributes & Text ===\n")

link = soup.find("a")
print(f"href attribute: {link['href']}")
print(f"href (safe get): {link.get('href')}")
print(f"data-custom (missing): {link.get('data-custom', 'N/A')}")
print(f"All attributes: {link.attrs}")
print(f"Has 'href'?: {link.has_attr('href')}")

# Text content
h1 = soup.find("h1")
print(f"Text content: {h1.get_text()}")
print(f"Text with strip: {h1.get_text(strip=True)}")
```

    === Accessing Attributes & Text ===

    href attribute: https://example.com
    href (safe get): https://example.com
    data-custom (missing): N/A
    All attributes: {'href': 'https://example.com'}
    Has 'href'?: True
    Text content: Welcome to BeautifulSoup
    Text with strip: Welcome to BeautifulSoup

``` python
# Example 5: Modifying the Tree
print("\n=== Modifying the Tree ===\n")

# Create a copy to modify
soup_copy = BeautifulSoup(str(soup), "lxml")

# Modify attributes
link = soup_copy.find("a")
link["data-modified"] = "true"
link["class"] = "external-link"
print(f"Modified link: {link}")

# Create and append new tags
new_tag = soup_copy.new_tag("p", attrs={"class": "note"})
new_tag.string = "This is a new paragraph!"
container = soup_copy.find("div", class_="container")
container.append(new_tag)

print(f"New paragraph added: {new_tag}")

# Extract specific tag
extracted = soup_copy.find("h1").extract()
print(f"Extracted h1 from tree: {extracted}")
```

    === Modifying the Tree ===

    Modified link: <a class="external-link" data-modified="true" href="https://example.com">Example Link</a>
    New paragraph added: <p class="note">This is a new paragraph!</p>
    Extracted h1 from tree: <h1>Welcome to BeautifulSoup</h1>

``` python
# Example 6: Scraping a Table
print("\n=== Scraping a Table ===\n")

table_html = """
<table>
    <thead>
        <tr><th>Name</th><th>Age</th><th>City</th></tr>
    </thead>
    <tbody>
        <tr><td>Alice</td><td>28</td><td>New York</td></tr>
        <tr><td>Bob</td><td>35</td><td>San Francisco</td></tr>
        <tr><td>Charlie</td><td>31</td><td>Boston</td></tr>
    </tbody>
</table>
"""

table_soup = BeautifulSoup(table_html, "lxml")

# Extract header
headers = [th.get_text(strip=True) for th in table_soup.find_all("th")]
print(f"Headers: {headers}")

# Extract rows
rows = table_soup.find_all("tr")[1:]  # Skip header row
data = []
for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all("td")]
    data.append(cols)
    print(f"  {cols}")

print(f"\nTotal rows scraped: {len(data)}")
```

    === Scraping a Table ===

    Headers: ['Name', 'Age', 'City']
      ['Alice', '28', 'New York']
      ['Bob', '35', 'San Francisco']
      ['Charlie', '31', 'Boston']

    Total rows scraped: 3

Back to top
