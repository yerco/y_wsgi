# Decorators
https://realpython.com/primer-on-python-decorators/

## First-Class Objects
In Python, functions are first-class objects. 
This means that functions can be passed around and used as arguments, 
just like any other object (string, int, float, list, and so on).

```python
def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we're the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")
```
```bash
>>> greet_bob(say_hello)
'Hello Bob'

>>> greet_bob(be_awesome)
'Yo Bob, together we're the awesomest!'
```

## Inner Functions
It’s possible to define functions inside other functions. Such functions are called inner functions.
```python
def parent():
    print("Printing from the parent() function")

    def first_child():
        return "Printing from the first_child() function"

    def second_child():
        return "Printing from the second_child() function"

    print(first_child())
    print(second_child())
```
```bash
>>> parent()
Printing from the parent() function
Printing from the first_child() function
Printing from the second_child() function
```

## Functions as Return Values
Functions can be passed as arguments to other functions and can also be returned by other functions.
```python
def parent(num):
    def first_child():
        return "Hi, I am Elias"

    def second_child():
        return "Call me Ester"

    if num == 1:
        return first_child
    else:
        return second_child
```
```bash
>>> first = parent(1)
>>> second = parent(2)

>>> first
<function parent.<locals>.first_child at 0x7f3f3b8f6d30>
>>> second
<function parent.<locals>.second_child at 0x7f3f3b8f6e18>
```

## Simple Decorators
```python
def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = decorator(say_whee)
```
```bash
>>> say_whee()
Something is happening before the function is called.
Whee!
Something is happening after the function is called.
```

**`say_whee = decorator(say_whee)`**

## Syntactic Sugar!
```python
def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@decorator
def say_whee():
    print("Whee!")
```
```bash
>>> say_whee()
Something is happening before the function is called.
Whee!
Something is happening after the function is called.
```
**`say_whee = decorator(say_whee)`**

## Reusing Decorators
```python
def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice
```
```bash
>>> @do_twice
... def say_whee():
...     print("Whee!")
...
>>> say_whee()
Whee!
Whee!
```

## Decorating Functions With Arguments
```python
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice
```
```bash
>>> @do_twice
... def greet(name):
...     print(f"Hello {name}")
...
>>> greet("World")
Hello World
Hello World
```

## Returning Values From Decorated Functions
```python
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"
```
```bash
>>> return_greeting("Adam")
Creating greeting
Creating greeting
Hi Adam
```

## Who Are You, Really?
To solve the issue of the identity of the decorated functions:
```python
import functools

def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice
```



