# Python Unit Test Generator

Simple tool to auto-generate [unittest](https://docs.python.org/3/library/unittest.html) unit tests for python code.
Note that this only generates scaffolding code - it does not make actual tests, just the boilerplate.

This tool simply uses a regex to detect all functions in the code:
```regexp
((@.*\n)?\s*def (.*)\((.|\n)*?\)( -> .*?)?:(?=(.|\n)*?((@.*?)?\n(@.*\n)?\s*def)||(\s*\Z)))
```

> [!IMPORTANT]
> This tool only detects function names, not the classes they are in. So, if you have a function with the same name in multiple classes (such as `__init__`), the program will differentiate by adding a numerical suffix to duplicates in the generated test cases - for example, `__init__`, `__init__2`, `__init__3`, etc. The same will be true for functions that are defined multiple times (even though only one function is really being defined). In short, **this tool works best on code with only one class / no function redefinitions, so duplicate function names can be avoided.**

# Usage

```shell
python_unit_test_generator <file_path> <output_path>
```
`output_path` defaults to `output.py` in the current working directory.

### Example:

my_script.py:
```py
# Taken fromhttps://www.w3schools.com/python/python_classes.asp

class Person:
  def __init__(mysillyobject, name, age):
    mysillyobject.name = name
    mysillyobject.age = age

  def myfunc(abc):
    print("Hello my name is " + abc.name)

p1 = Person("John", 36)
p1.myfunc()
```

<br>

```shell
python_unit_test_generator my_script.py
```

output.py:
```py
import unittest


class GeneratedTests(unittest.TestCase):
    def test___init__(self) -> None:
        ...

    def test_myfunc(self) -> None:
        ...


```
