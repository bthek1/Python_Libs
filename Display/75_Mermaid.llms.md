# Mermaid

Library for making Diagrams

Author

Benedict Thekkel

```` python
from IPython.display import display, Markdown

display(Markdown('''
```mermaid
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[Do something]
    B -->|No| D[Do something else]
    C --> E[End]
    D --> E[End]
```
'''))
````

``` mermaid
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[Do something]
    B -->|No| D[Do something else]
    C --> E[End]
    D --> E[End]
```

#### 2. Sequence Diagram

``` mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: I am good thanks!
    Alice->>Bob: Are you going to the party?
    Bob-->>Alice: Yes, see you there!
```

#### 3. Class Diagram

``` mermaid
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
      +String beakColor
      +swim()
      +quack()
    }
    class Fish{
      -int sizeInFeet
      -canEat()
    }
    class Zebra{
      +bool is_wild
      +run()
    }
```

#### 4. Gantt Chart

``` mermaid
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2024-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2024-01-12  , 12d
    another task     : 24d
```

## Running Mermaid Diagrams

Code

``` python
from IPython.display import display, HTML

mermaid_code = """
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[Do something]
    B -->|No| D[Do something else]
    C --> E[End]
    D --> E[End]
"""

display(HTML(f"""
<div class="mermaid">
  {mermaid_code}
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{ startOnLoad: true }});
</script>
"""))
```

graph TD A\[Start\] --\> B{Is it?} B --\>\|Yes\| C\[Do something\] B --\>\|No\| D\[Do something else\] C --\> E\[End\] D --\> E\[End\]

Back to top
