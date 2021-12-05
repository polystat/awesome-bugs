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
description: An error can occur when divided by the value received as an argument to the method
features: 
  - operators/division
  - loops
language: java
bad:
  foo.java: |
    class Foo {
      int f(int x) {
        return 42 / x;
      }
    }
  foo.eo: |
    [] > Foo
      [] > new
        [x] > f
          42.div x > @
good:
  foo.java: |
    class Foo {
      int f(int x) {
        if(x!=0) {
          return 42 / x;
        }
       }
    }
  foo.eo: |
    [] > Foo
      [] > new
        [x] > f
          if. > @
            x.neq 0
            42.div x
            TRUE
```

Temporarily (until we have powerful enough Java/C++/Python to EO translators) we
keep EO code snippets in the YAML files too.

Both `bad` and `good` sections are mandatory. Intuitively, the `bad` section
contains a program with a bug, while the `good` one has a similar program
but without a bug.

