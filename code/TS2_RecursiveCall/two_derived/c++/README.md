# 2 derived classes become recursive independently

```
# Name        : 2 derived classes override the 2 base methods in such a way
                that the derived methods become mutually recursive
# FailureType : StackOverflowError
# ErrorType   : Programming error
# Source      : https://github.com/Sitiritis/eo-static-analyzer/blob/demo/sandbox/src/main/resources/mutual_rec_non_term_2_derived.eo
# CodeType    : Artificial
# Lines       : (45, 50), (57, 62)
```

## *NOTE*: the groups of numbers in parentheses indicate the lines containing mutually recursive calls.
