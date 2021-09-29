# A derived class overrides one of the methods of the inner class of Base in such a way that the other method becomes mutually recursive with the overridden method.

```
# Name        : A derived class overrides one of the methods of the inner class of Base
                in such a way that the other method becomes mutually recursive with the override method.
# FailureType : StackOverflowError
# ErrorType   : Programming error
# Source      : https://github.com/Sitiritis/eo-static-analyzer/blob/demo/sandbox/src/main/resources/mutual_rec_non_term_factory.eo
# CodeType    : Artificial
# Lines       : 31, 39
```

## *NOTE*: the pairs of numbers in parentheses indicate the lines containing mutually recursive calls.
