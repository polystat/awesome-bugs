# 2 derived classes become recursive independently

```
# Name        : Derived classes override the base methods in such a way
                that they become mutually recursive, independently of each other
# FailureType : StackOverflowError
# ErrorType   : Programming error
# Source      : https://github.com/Sitiritis/eo-static-analyzer/blob/demo/sandbox/src/main/resources/mutual_rec_non_term_2_derived.eo
# CodeType    : Artificial
# Lines       : (45, 50), (57, 62)
```
