# A long chain of mutually recursive methods. 
```
# Name        : Method M from Base calls a method N from Base. Derived class extends Base
                and adds a method O which calls method M. A class DerivedAgain overrides 
                the method N in such a way that it calls O. The resulting call chain becomes:
                N calls O, which calls M, which calls N.
# FailureType : StackOverflowError
# ErrorType   : Programming error
# Source      : https://github.com/Sitiritis/eo-static-analyzer/blob/demo/sandbox/src/main/resources/mutual_rec_non_term_long_chain.eo
# CodeType    : Artificial
# Lines       : 34, 41, 48
```

## *NOTE*: the groups of numbers in parentheses indicate the lines containing mutually recursive calls.
