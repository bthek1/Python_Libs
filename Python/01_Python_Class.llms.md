# Python Class

Python class

Author

Benedict Thekkel

## Scopes and Namespaces Example

``` python
def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)
```

    After local assignment: test spam
    After nonlocal assignment: nonlocal spam
    After global assignment: nonlocal spam
    In global scope: global spam

## Class Syntax

``` python
class ClassName:
    <statement-1>
    .
    .
    .
    <statement-N>
```

## The self Parameter

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)

p1 = Person("John", 36)
p1.myfunc()
```

    Hello my name is John

``` python
class Person:
    def __init__(mysillyobject, name, age):
        mysillyobject.name = name
        mysillyobject.age = age

    def myfunc(abc):
        print("Hello my name is " + abc.name)

p1 = Person("John", 36)
p1.myfunc()
```

    Hello my name is John

### The pass Statement

class definitions cannot be empty, but if you for some reason have a class definition with no content, put in the pass statement to avoid getting an error.

``` python
class Person:
    pass
```

## `__init__`

The instantiation operation (“calling” a class object) creates an empty object. Many classes like to create objects with instances customized to a specific initial state. Therefore a class may define a special method named **init**(), like this:

``` python
def __init__(self):
    self.data = []
```

``` python
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

x = Complex(3.0, -4.5)

x.r, x.i
```

    (3.0, -4.5)

## `__new__`

When you create a new object by calling the class, Python calls the **new**() method to create the object first and then calls the **init**() method to initialize the object’s attributes.

``` python
class Person:
    def __new__(cls, name):
        print(f'Creating a new {cls.__name__} object...')
        obj = object.__new__(cls)
        return obj

    def __init__(self, name):
        print(f'Initializing the person object...')
        self.name = name


person = Person('John')
```

    Creating a new Person object...
    Initializing the person object...

``` python
x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
del x.counter
```

    16

``` python
class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
d.tricks                # unexpectedly shared by all dogs
```

    ['roll over', 'play dead']

``` python
class Dog:

    def __init__(self, name):
        self.name = name
        self.tricks = []    # creates a new empty list for each dog

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
d.tricks
```

    ['roll over']

``` python
e.tricks
```

    ['play dead']

Methods may call other methods by using method attributes of the self argument:

``` python
class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)
```

## `__iter__` & `__next__`

``` python
class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index = len(self.data)
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
```

``` python
rev = Reverse('spam')

iter(rev)
```

    <__main__.Reverse>

``` python
for char in rev:
    print(char)
```

    m
    a
    p
    s

``` python
s = 'abc'

it = iter(s)

it
```

    <str_ascii_iterator>

``` python
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
        

for char in reverse('golf'):
    print(char)
```

    f
    l
    o
    g

Anything that can be done with generators can also be done with class-based iterators as described in the previous section. What makes generators so compact is that the **iter**() and **next**() methods are created automatically.

## `__str__`

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("John", 36)

print(p1)
```

    <__main__.Person object>

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}({self.age})"

p1 = Person("John", 36)

print(p1)
```

    John(36)

## `__repr__`

``` python
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
```

``` python
person = Person('John', 'Doe', 25)
print(repr(person))
```

    <__main__.Person object>

``` python
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        
    def __str__(self):
        return f'str: {self.first_name}","{self.last_name}",{self.age}'

    def __repr__(self):
        return f'repr: ("{self.first_name}","{self.last_name}",{self.age})'
    
    def __call__(self):
        return f"call: {self.__dict__}"
```

``` python
person = Person("John", "Doe", 25)
print(person)
```

    str: John","Doe",25

``` python
print(repr(person))
```

    repr: ("John","Doe",25)

``` python
person
```

    repr: ("John","Doe",25)

``` python
person()
```

    "call: {'first_name': 'John', 'last_name': 'Doe', 'age': 25}"

#### **str** vs **repr**

The main difference between **str** and **repr** method is intended audiences.

The **str** method returns a string representation of an object that is human-readable while the **repr** method returns a string representation of an object that is machine-readable.

#### Summary

- Implement the **repr** method to customize the string representation of an object when repr() is called on it.
- The **str** calls **repr** internally by default.

## `__call__`

``` python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def __call__(self):
        self.increment()
        return self.count
```

``` python
count = Counter()
```

``` python
count()
```

    1

``` python
count.__dict__
```

    {'count': 1}

## `__setattr__` & `__getattr__`

``` python
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.set_age(age)
        
    def __str__(self):
        return f'str: {self.first_name}","{self.last_name}",{self.age}'

    def __repr__(self):
        return f'repr: ("{self.first_name}","{self.last_name}",{self.age})'
    
    def __call__(self):
        return f"call: {self.__dict__}"
    
    def __getattr__(self, attr):
        print("getting attr")
        try:
            return self.__dict__[attr] 
        except KeyError:
            print(f"Attribute doesn't exist")
    
    
    def __setattr__(self, attr, value):
        print(f"setting attr: class.{attr} = {value}")
        self.__dict__[attr] = value
        
    def set_age(self, age):
        if age <= 0:
            #raise ValueError('The age must be positive')
            print('The age must be positive')
            return
        self._age = age

    def get_age(self):
        return self._age
```

``` python
john = Person('John', 'Doe', 23)
john.set_age(12)
```

    setting attr: class.first_name = John
    setting attr: class.last_name = Doe
    setting attr: class._age = 23
    setting attr: class._age = 12

``` python
john.a = 1
```

    setting attr: class.a = 1

``` python
john.b
```

    getting attr
    Attribute doesn't exist

``` python
john.__dict__
```

    {'first_name': 'John', 'last_name': 'Doe', '_age': 12, 'a': 1}

``` python
getattr(john, 'b')
```

    getting attr
    Attribute doesn't exist

## `__setitem__` & `__getitem__`

``` python
# Code to demonstrate use 
# of __getitem__() in python 
class Test(object): 
      
    # This function prints the type 
    # of the object passed as well  
    # as the object item 
    def __getitem__(self, items): 
        print (type(items), items) 
  
    # Driver code 
test = Test() 
test[5] 
test[5:65:5] 
test['GeeksforGeeks'] 
test[1, 'x', 10.0] 
test['a':'z':2] 
test[object()]
```

    <class 'int'> 5
    <class 'slice'> slice(5, 65, 5)
    <class 'str'> GeeksforGeeks
    <class 'tuple'> (1, 'x', 10.0)
    <class 'slice'> slice('a', 'z', 2)
    <class 'object'> <object object>

``` python
class Building(object):
    def __init__(self, floors):
        self._floors = [None]*floors
    def __setitem__(self, floor_number, data):
        self._floors[floor_number] = data
    def __getitem__(self, floor_number):
        return self._floors[floor_number]

building1 = Building(4) # Construct a building with 4 floors
building1[0] = 'Reception'
building1[1] = 'ABC Corp'
building1[2] = 'DEF Inc'
print(building1[1])
```

    ABC Corp

``` python
class PDFreader:
    ''' Function for reading and displaying pdf files
        ex. path = './Data/<file>.pdf' 
            pdf = PDFreader(path, size = (10, 8))
            pdf[0:5]
    '''
    def __init__(self, path, size = (6, 4)):
        self.filepath = path
        self.images = self.display_pdf_slides()
        self.index = 0
        self.size = size   
        
        
    def __str__(self):
        return f'--string--: path:"{self.filepath}"   index:{self.index}   size:{self.size}   len:{len(self.images)}'

    def __repr__(self):
        return f'--Representation-- \r\npath:"{self.filepath}" \r\nindex:{self.index} \r\nsize:{self.size} \r\nlen:{len(self.images)}'
    
    def __getitem__(self, slide):
        'get slides like indexing a array'
        if isinstance(slide, int):
            self.slides(slice(slide, slide + 1))   
        elif isinstance(slide, slice):
            self.slides(slide)  
            
    
    def slides(self, slide):
        'display the slide as plt.imshow(image)'
        import matplotlib.pyplot as plt

        for i, image in enumerate(self.images[slide]):
            plt.figure(figsize=self.size)
            plt.imshow(image)
            if slide.step == None:
                plt.title(f'Slide {slide.start + i}')
            else:
                plt.title(f'Slide {slide.start + slide.step}')
            plt.axis('off')
        plt.show()
```

## `__enter__` & `__exit__`

``` python
class MySecretConnection:
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        print('entering:', self.url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit:', self.url)


with MySecretConnection('(test)') as finxter:
    # Called finxter.__enter__()
    pass
    # Called finxter.__exit__()
```

    entering: (test)
    exit: (test)

``` python
class Open_File():
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        print('file opened')
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        self.file.close()
        print('file closed')
        
with Open_File('Data/sample.txt', 'a') as f:
    f.write('Testing\n\r')
        
print(f.closed)
```

    file opened
    file closed
    True

``` python
from contextlib import contextmanager

@contextmanager
def open_file(file, mode):
    # __enter__ start
    f = open(file, mode)  
    print('file opened')
    # __enter__ end
    yield f
    # __exit__ start
    f.close()
    print('file closed')
    # __exit__ end
    
with open_file('Data/sample.txt', 'a') as f:
    f.write('test text\n\r')
    
print(f.closed)
```

    file opened
    file closed
    True

## `__eq__`

``` python
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
```

``` python
john = Person('John', 'Doe', 25)
jane = Person('Jane', 'Doe', 25)
```

``` python
print(john is jane); print(john == jane); john == jane # False
```

    False
    False

    False

``` python
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.age == other.age

        return False
```

``` python
john = Person('John', 'Doe', 25)
jane = Person('Jane', 'Doe', 25)
print(john is jane); print(john == jane); john == jane # False
```

    False
    True

    True

``` python
john = Person('John', 'Doe', 25)
mary = Person('Mary', 'Doe', 27)
print(john is mary); print(john == mary); john == mary # False
```

    False
    False

    False

``` python
john = Person('John', 'Doe', 25)
print(john == 20)
```

    False

## `__bool__`

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __bool__(self):
        if self.age < 18 or self.age > 65:
            return False
        return True



jane = Person('Jane', 19)
bool(jane)
```

    True

``` python
bool(jane) is True
```

    True

## `__len__`

``` python
a = 'aasd'
len(a)
```

    4

``` python
class Person:
    def __init__(self, name):
        self.name = name

    def __len__(self):
        print('len was called...')
        return len(self.name)


ben = Person('ben')
print(bool(ben))  # False

ben.name = ''
print(bool(ben))  # True
```

    len was called...
    True
    len was called...
    False

#### Summary

- All objects of custom classes return True by default.
- Implement the **bool** method to override the default. The **bool** method must return either True or False.
- If a class doesn’t implement the **bool** method, Python will use the result of the **len** method. If the class doesn’t implement both methods, the objects will be True by default.

## `__del__`

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __del__(self):
        print('__del__ was called')


person = Person('John Doe', 23)
del person
```

    __del__ was called

``` python
person = Person('John Doe', 23)
person = None
```

    __del__ was called

## `__dict__`

``` python
Person.__dict__
```

    mappingproxy({'__module__': '__main__',
                  '__init__': <function __main__.Person.__init__(self, name, age)>,
                  '__del__': <function __main__.Person.__del__(self)>,
                  '__dict__': <attribute '__dict__' of 'Person' objects>,
                  '__weakref__': <attribute '__weakref__' of 'Person' objects>,
                  '__doc__': None})

## Python Operator Overloading

``` python
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x},{self.y})'

    def __add__(self, point):
        if not isinstance(point, Point2D):
            raise ValueError('The other must be an instance of the Point2D')

        return Point2D(self.x + point.x, self.y + point.y)

    def __sub__(self, point):
        if not isinstance(point, Point2D):
            raise ValueError('The other must be an instance of the Point2D')

        return Point2D(self.x - point.x, self.y - point.y)
    def __mul__(self, point):
        if not isinstance(point, Point2D):
            raise ValueError('The other must be an instance of the Point2D')

        return Point2D(self.x * point.x, self.y * point.y)

    def __and__(self, point):
        return self.__add__(point)


a = Point2D(10, 20)
b = Point2D(15, 25)
c = b - a
b-a, b + a, b * a, b & a
```

    ((5,5), (25,45), (150,500), (25,45))

## Inheritance

``` python
class DerivedClassName(Base1, Base2, Base3):
    <statement-1>
    .
    .
    .
    <statement-N>
```

#### Example

``` python
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
        
    def __str__(self):
        return f"str:{self.lastname}, {self.firstname}"
    
    def __repr__(self):
        return f'Repr: {self.firstname},{self.lastname}'

    def printname(self):
        print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:
```

``` python
x = Person("John", "Doe")
print(x)
```

    str:Doe, John

``` python
x
```

    Repr: John,Doe

``` python
class Student(Person):
    pass 

x = Student("Mike", "Olsen")
x.printname()
```

    Mike Olsen

The child’s **init**() function overrides the inheritance of the parent’s **init**() function.

``` python
class Student(Person):
    def __init__(self, fname, lname):
        Person.__init__(self, fname, lname)
```

Now we have successfully added the **init**() function, and kept the inheritance of the parent class, and we are ready to add functionality in the **init**() function.

Python also has a super() function that will make the child class inherit all the methods and properties from its parent:

``` python
class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year

    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)
```

``` python
x = Student("Mike", "Olsen", 2019) 
x.welcome()
```

    Welcome Mike Olsen to the class of 2019

## Property

### Getter and setter

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.set_age(age)

    def set_age(self, age):
        if age <= 0:
            #raise ValueError('The age must be positive')
            print('The age must be positive')
            return
        self._age = age

    def get_age(self):
        return self._age

john = Person('John', 18)
```

``` python
john.set_age(-19)
print(john.get_age())
```

    The age must be positive
    18

``` python
john.__dict__
```

    {'name': 'John', '_age': 18}

``` python
Person.__dict__
```

    mappingproxy({'__module__': '__main__',
                  '__init__': <function __main__.Person.__init__(self, name, age)>,
                  'set_age': <function __main__.Person.set_age(self, age)>,
                  'get_age': <function __main__.Person.get_age(self)>,
                  '__dict__': <attribute '__dict__' of 'Person' objects>,
                  '__weakref__': <attribute '__weakref__' of 'Person' objects>,
                  '__doc__': None})

The property() has the following parameters:

- fget is a function to get the value of the attribute, or the getter method.
- fset is a function to set the value of the attribute, or the setter method.
- fdel is a function to delete the attribute.
- doc is a docstring i.e., a comment.

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.set_age(age)

    def set_age(self, age):
        if age <= 0:
            #raise ValueError('The age must be positive')
            print('The age must be positive')
            return
        self._age = age

    def get_age(self):
        return self._age
    
    age = property(fget=get_age, fset=set_age)

john = Person('John', 18)
```

``` python
john.age = -19
```

    The age must be positive

``` python
john.age
```

    18

### Property Decorator

Here’s the syntax of the property class:

``` python
class property(fget=None, fset=None, fdel=None, doc=None)
```

The property() accepts a callable (age) and returns a callable. Therefore, it is a decorator. Therefore, you can use the @property decorator to decorate the age() method as follows:

To assign the set_age to the fset of the age property object, you call the setter() method of the age property object like the following:

``` python
class Person:
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def set_age(self, value):
        if value <= 0:
            raise ValueError('The age must be positive')
        self._age = value
```

### Readonly Property

To define a readonly property, you need to create a property with only the getter. However, it is not truly read-only because you can always access the underlying attribute and change it.

``` python
import math


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2


c = Circle(10)
print(c.area)
```

    314.1592653589793

### Delete Property

``` python
from pprint import pprint


class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value.strip() == '':
            raise ValueError('name cannot be empty')
        self._name = value

    @name.deleter
    def name(self):
        del self._name
```

``` python
pprint(Person.__dict__)
```

    mappingproxy({'__dict__': <attribute '__dict__' of 'Person' objects>,
                  '__doc__': None,
                  '__init__': <function Person.__init__>,
                  '__module__': '__main__',
                  '__weakref__': <attribute '__weakref__' of 'Person' objects>,
                  'name': <property object>})

``` python
person = Person('John')
```

``` python
person.__class__.__name__
```

    'Person'

``` python
pprint(person.__dict__)
```

    {'_name': 'John'}

``` python
del person.name
```

``` python
pprint(person.__dict__)
```

    {}

## Decorators

### Passing the function as an argument

``` python
# can be passed as arguments to other functions 
def shout(text): 
    return text.upper() 
 
def whisper(text): 
    return text.lower() 
 
def greet(func): 
    # storing the function in a variable 
    greeting = func("""Hi, I am created by a function passed as an argument.""") 
    print (greeting)
```

``` python
greet(shout) 
greet(whisper)
```

    HI, I AM CREATED BY A FUNCTION PASSED AS AN ARGUMENT.
    hi, i am created by a function passed as an argument.

### Returning functions from another function.

``` python
def create_adder(x): 
    def adder(y): 
        return x+y 
 
    return adder 
 
add_15 = create_adder(15) 
 
print(add_15(10))
```

    25

As stated above the decorators are used to modify the behaviour of function or class. In Decorators, functions are taken as the argument into another function and then called inside the wrapper function.

``` python
@gfg_decorator
def hello_decorator():
    print("Gfg")

'''Above code is equivalent to '''

def hello_decorator():
    print("Gfg")
    
hello_decorator = gfg_decorator(hello_decorator)
```

### Decorator can modify the behaviour:

``` python
# importing libraries
import time
import math
 
# decorator to calculate duration
# taken by any function.
def calculate_time(func):
    print('inside')
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
 
        # storing time before function execution
        begin = time.time()
        print('before')
        a = func(*args, **kwargs)
        
        # storing time after function execution
        end = time.time()
        print("after: Total time taken in : ", func.__name__, end - begin)
        
        return a
 
    return inner1
 
 
 
# this can be added to any function present,
# in this case to calculate a factorial
#@calculate_time
def factorial(num):
 
    # sleep 2 seconds because it takes very less time
    # so that you can see the actual difference
    return math.factorial(num)
 
# calling the function.
factorial(10)
```

    3628800

``` python
calculate_time(factorial)(10)
```

    inside
    before
    Total time taken in :  factorial 3.361701965332031e-05

    3628800

``` python
factorial = calculate_time(factorial)
```

    inside

``` python
factorial(10)
```

    before
    Total time taken in :  factorial 0.00014400482177734375

    3628800

``` python
factorial(1)
```

    before
    Total time taken in :  factorial 0.000186920166015625

    1

``` python
@calculate_time
def factorial(num):
 
    # sleep 2 seconds because it takes very less time
    # so that you can see the actual difference

    return math.factorial(num)
```

    inside

``` python
# calling the function.
factorial(10)
```

    before
    Total time taken in :  factorial 0.0002372264862060547

    3628800

#### Example

``` python
def hello_decorator(func):
    def inner1(*args, **kwargs):
        
        print("before Execution")
        
        # getting the returned value
        returned_value = func(*args, **kwargs)
        print("after Execution")
        
        # returning the value to the original frame
        return returned_value
        
    return inner1


# adding decorator to the function
@hello_decorator
def sum_two_numbers(a, b):
    print("Inside the function")
    return a + b

a, b = 1, 2

# getting the value through return of the function
print("Sum =", sum_two_numbers(a, b))
```

    before Execution
    Inside the function
    after Execution
    Sum = 3

### Decorator Chaining

``` python
# code for testing decorator chaining 
def decor1(func):
    def inner():
        
        x = func()
        print(f'{x} * {x}')
        return x * x
    return inner 
def decor(func):
    def inner():
        x = func()
        print(f'2 * {x}')
        return 2 * x
    return inner
 


@decor1
@decor
def num(): 
    print(10)
    return 10

@decor
@decor1
def num2():
    print(10)
    return 10

print(num()) 
print(num2())
```

    10
    2 * 10
    20 * 20
    400
    10
    10 * 10
    2 * 100
    200

### Decorator with parameters

``` python
# Python code to illustrate 
# Decorators with parameters in Python 

def decorator_func(x, y):

    def Inner(func):

        def wrapper(*args, **kwargs):
            print("I like Geeksforgeeks")
            print("Summation of values - {}".format(x+y) )

            func(*args, **kwargs)
            
        return wrapper
    return Inner


# Not using decorator 
def my_fun(*args):
    for ele in args:
        print(ele)

# another way of using decorators
decorator_func(12, 15)(my_fun)('Geeks', 'for', 'Geeks')
```

    I like Geeksforgeeks
    Summation of values - 27
    Geeks
    for
    Geeks

``` python
@decorator_func(12,15)
def my_fun(*args):
    for ele in args:
        print(ele)

# another way of using decorators
my_fun('Geeks', 'for', 'Geeks')
```

    I like Geeksforgeeks
    Summation of values - 27
    Geeks
    for
    Geeks

## Partials

Partial functions support both positional and keyword arguments to be used as fixed arguments.

input a function with inputs variables to be set\
output new function with the variabes set

``` python
from functools import partial
```

``` python
partial??
```

    Init signature: partial(self, /, *args, **kwargs)
    Docstring:     
    partial(func, *args, **keywords) - new function with partial application
    of the given arguments and keywords.
    Source:        
    class partial:
        """New function with partial application of the given arguments
        and keywords.
        """
        __slots__ = "func", "args", "keywords", "__dict__", "__weakref__"
        def __new__(cls, func, /, *args, **keywords):
            if not callable(func):
                raise TypeError("the first argument must be callable")
            if hasattr(func, "func"):
                args = func.args + args
                keywords = {**func.keywords, **keywords}
                func = func.func
            self = super(partial, cls).__new__(cls)
            self.func = func
            self.args = args
            self.keywords = keywords
            return self
        def __call__(self, /, *args, **keywords):
            keywords = {**self.keywords, **keywords}
            return self.func(*self.args, *args, **keywords)
        @recursive_repr()
        def __repr__(self):
            qualname = type(self).__qualname__
            args = [repr(self.func)]
            args.extend(repr(x) for x in self.args)
            args.extend(f"{k}={v!r}" for (k, v) in self.keywords.items())
            if type(self).__module__ == "functools":
                return f"functools.{qualname}({', '.join(args)})"
            return f"{qualname}({', '.join(args)})"
        def __reduce__(self):
            return type(self), (self.func,), (self.func, self.args,
                   self.keywords or None, self.__dict__ or None)
        def __setstate__(self, state):
            if not isinstance(state, tuple):
                raise TypeError("argument to __setstate__ must be a tuple")
            if len(state) != 4:
                raise TypeError(f"expected 4 items in state, got {len(state)}")
            func, args, kwds, namespace = state
            if (not callable(func) or not isinstance(args, tuple) or
               (kwds is not None and not isinstance(kwds, dict)) or
               (namespace is not None and not isinstance(namespace, dict))):
                raise TypeError("invalid partial state")
            args = tuple(args) # just in case it's a subclass
            if kwds is None:
                kwds = {}
            elif type(kwds) is not dict: # XXX does it need to be *exactly* dict?
                kwds = dict(kwds)
            if namespace is None:
                namespace = {}
            self.__dict__ = namespace
            self.func = func
            self.args = args
            self.keywords = kwds
    File:           ~/mambaforge/envs/cfast/lib/python3.11/functools.py
    Type:           type
    Subclasses:     

``` python
# A normal function
def f(a, b, c, x):
    return 1000*a + 100*b + 10*c + x
 
# A partial function that calls f with
# a as 3, b as 1 and c as 4.
g = partial(f, 3, 1, 4)
 
# Calling g()
print(g(5))
```

    3145

``` python
from functools import *
 
# A normal function
def add(a, b, c):
    print(f'a:{a}, b:{b}, c:{c}')
    return 100 * a + 10 * b + c
 
# A partial function with b = 1 and c = 2
add_part = partial(add, c = 2, b = 1)
 
# Calling partial function
print(add_part(3))
```

    a:3, b:1, c:2
    312

``` python
def greater_than(a, b):
    return a < b

greater_than(5,10)

def make_comparator(n):
    def inner(a):
        return a < n

    return inner


def partial(*args):
    def inner(a):
        return args[0](args[1],a)
    return inner
```

``` python
greater_than_20 = make_comparator(20)
```

``` python
greater_than_20(40)
```

    False

``` python
greater_than_2 = partial(greater_than,2)
```

``` python
greater_than_2(2)
```

    False

## \*args and \*\*kwargs in Python

### `*args`

``` python
def myFun(*argv):
    for arg in argv:
        print(arg)
 
 
myFun('Hello', 'Welcome', 'to', 'GeeksforGeeks')
```

    Hello
    Welcome
    to
    GeeksforGeeks

``` python
def myFun(arg1, *argv):
    print("First argument :", arg1)
    for arg in argv:
        print("Next argument through *argv :", arg)
 
 
myFun('Hello', 'Welcome', 'to', 'GeeksforGeeks')
```

    First argument : Hello
    Next argument through *argv : Welcome
    Next argument through *argv : to
    Next argument through *argv : GeeksforGeeks

### `**kwargs`

``` python
def myFun(**kwargs):
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))
 
 
# Driver code
myFun(first='Geeks', mid='for', last='Geeks')
```

    first == Geeks
    mid == for
    last == Geeks

``` python
def myFun(arg1, **kwargs):
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))
 
 
# Driver code
myFun("Hi",  first='Geeks', mid='for', last='Geeks')
```

    first == Geeks
    mid == for
    last == Geeks

``` python
def myFun(arg1, arg2, arg3):
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)
 
 
# Now we can use *args or **kwargs to
# pass arguments to this function :
args = ("Geeks", "for", "Geeks")
myFun(*args)
 
kwargs = {"arg1": "Geeks", "arg2": "for", "arg3": "Geeks"}
myFun(**kwargs)
```

    arg1: Geeks
    arg2: for
    arg3: Geeks
    arg1: Geeks
    arg2: for
    arg3: Geeks

``` python
def myFun(*args, **kwargs):
    print("args: ", args)
    print("kwargs: ", kwargs)
 
 
# Now we can use both *args ,**kwargs
# to pass arguments to this function :
myFun('geeks', 'for', 'geeks', first="Geeks", mid="for", last="Geeks")
```

    args:  ('geeks', 'for', 'geeks')
    kwargs:  {'first': 'Geeks', 'mid': 'for', 'last': 'Geeks'}

``` python
# defining car class
class car():
    # args receives unlimited no. of arguments as an array
    def __init__(self, *args):
        # access args index like array does
        self.speed = args[0]
        self.color = args[1]
 
 
# creating objects of car class
audi = car(200, 'red')
bmw = car(250, 'black')
mb = car(190, 'white')
 
# printing the color and speed of the cars
print(audi.color)
print(bmw.speed)
```

    red
    250

``` python
# defining car class
class car():
    # args receives unlimited no. of arguments as an array
    def __init__(self, **kwargs):
        # access args index like array does
        self.speed = kwargs['s']
        self.color = kwargs['c']
 
 
# creating objects of car class
audi = car(s=200, c='red')
bmw = car(s=250, c='black')
mb = car(s=190, c='white')
 
# printing the color and speed of cars
print(audi.color)
print(bmw.speed)
```

    red
    250

## Yield

``` python
def simpleGeneratorFun():
    yield 1
    yield 2
    yield 3
 
 
# Driver code to check above generator function
for value in simpleGeneratorFun():
    print(value)
```

    1
    2
    3

``` python
def nextSquare():
    i = 1
 
    # An Infinite loop to generate squares
    while True:
        yield i*i
        i += 1  # Next execution resumes
        # from this point
 
 
# Driver code to test above generator
# function
for num in nextSquare():
    if num > 100:
        break
    print(num)
```

    1
    4
    9
    16
    25
    36
    49
    64
    81
    100

## Generators

``` python
# A generator function 
def simpleGeneratorFun(): 
    yield 1
    yield 2
    yield 3
    
    
    
# x is a generator object 
x = simpleGeneratorFun() 
  
# Iterating over the generator object using next 
  
# In Python 3, __next__() 
print(next(x)) 
print(next(x)) 
print(next(x))
```

    1
    2
    3

``` python
# generator expression 
generator_exp = (i for i in range(5)) 

for i in generator_exp: 
    print(i)
```

    0
    1
    2
    3
    4

``` python
# generator expression 
generator_exp = (i * 5 for i in range(5) if i%2==0) 

for i in generator_exp: 
    print(i)
```

    0
    10
    20

## Lambda

``` python
calc = lambda num: "Even number" if num % 2 == 0 else "Odd number"
 
print(calc(20))
```

    Even number

``` python
def cube(y):
    print(f"Finding cube of number:{y}")
    return y * y * y
 
lambda_cube = lambda num: num ** 3
 
# invoking simple function
print("invoking function defined with def keyword:")
print(cube(30))
# invoking lambda function
print("invoking lambda function:", lambda_cube(30))
```

    invoking function defined with def keyword:
    Finding cube of number:30
    27000
    invoking lambda function: 27000

## PDB

``` python
import pdb; pdb.set_trace()
```

    --Call--
    > /home/benedict/mambaforge/envs/cfast/lib/python3.11/site-packages/IPython/core/displayhook.py(258)__call__()
        256         sys.stdout.flush()
        257 
    --> 258     def __call__(self, result=None):
        259         """Printing with history cache management.
        260 

    ipdb>  help

    Documented commands (type help <topic>):
    ========================================
    EOF    commands   enable    ll        pp       s                until 
    a      condition  exit      longlist  psource  skip_hidden      up    
    alias  cont       h         n         q        skip_predicates  w     
    args   context    help      next      quit     source           whatis
    b      continue   ignore    p         r        step             where 
    break  d          interact  pdef      restart  tbreak         
    bt     debug      j         pdoc      return   u              
    c      disable    jump      pfile     retval   unalias        
    cl     display    l         pinfo     run      undisplay      
    clear  down       list      pinfo2    rv       unt            

    Miscellaneous help topics:
    ==========================
    exec  pdb

    ipdb>  exit

Back to top
