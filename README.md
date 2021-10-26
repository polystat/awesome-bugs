This is a taxonomy of software defects with examples.

We take into account the following classifications:

  * [MISRA C/C++](..)
  * ...

We are not trying to make an exhaustive list of defects, but mostly focus
on defects related to object-oriented structure of code. We classify by 
OO features being used in a defective program:

```
defects/
  classes/
  objects/
  inheritance/
  assertions/
  concurrency/
  null/
  operators/
    division/
      div-by-zero-when-reading-file.yml
      div-by-zero-in-simple-method.yml
    increment/
  loops/
  polymorphism/
  arrays/
  numbers/
  contracts/
  annotations/
  monads/
  traits/
  overloading/
  encapsulation/
  reflection/
  strings/
  pointers/
```

Each defect is presented in YAML format, similar to this one
(in a file `div-by-zero-in-simple-method.yml`):

```
title: A division without checking for zero may lead to division by zero
features: operator numbers/float
language: java
code: |
  class Foo {
    int f(int x) {
      return 42 / x;
    }
  }
```

To be continued...
