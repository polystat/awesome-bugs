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
      div-by-zero-when-reading-file.cpp.yml
      div-by-zero-when-inherited.java.yml
        ---
        tags: divison operator numbers
        author: 
        severity:
        ---
        class Foo {
        }
      div-02/
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

