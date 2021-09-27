package derived_again.java;

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

[] > derived
  base > @
  [self v] > n
    self.m self v > @

[] > derived_again
  derived > @
*/

class Base {
    public int x;

    public void n(int v) {
        this.x = v;
    }

    public void m(int v) {
        this.n(v);
    }
}

class Derived extends Base {
    @Override
    public void n(int v) {
        this.m(v);
    }
}

class DerivedAgain extends Derived {

}


public class DerivedAgainExample {
    public static void main(String[] args) {
        DerivedAgain derivedAgainInstance = new DerivedAgain();
        derivedAgainInstance.n(12);
    }
}
