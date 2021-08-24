package mutualrec.false_positive_type_check;

/*
+package sandbox
+alias stdout org.eolang.io.stdout
+alias sprintf org.eolang.txt.sprintf

[] > base
  memory > x
  [self v] > n
    x.write v > @
  [self v] > m
    self.n self v > @

[] > obj
  [self v] > m
    true > @
  [self v] > g
    false > @

[] > derived
  base > @
  [self v] > n
    self.g self v > a
    self.m self v > b
 */

public class FalsePositiveTypeCheck {

}