package mutualrec.non_term_2_derived;

/*
+package sandbox
+alias stdout org.eolang.io.stdout
+alias sprintf org.eolang.txt.sprintf

[] > base
  memory > x
  [self v] > n
    self.x.write v > @
  [self v] > m
    self.n self v > @

[] > derived1
  base > @
  [self v] > m
    self.n self v > @
  [self v] > n
    self.m self v > @

[] > derived2
  base > @
  [self v] > m
    self.n self v > @
  [self v] > n
    self.m self v > @
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

class Derived1 extends Base {
    @Override
    public void m(int v) {
        this.n(v);
    }

    @Override
    public void n(int v) {
        this.m(v);
    }
}

class Derived2 extends Base {
    @Override
    public void m(int v) {
        this.n(v);
    }

    @Override
    public void n(int v) {
        this.m(v);
    }
}

public class NonTerm2Derived {

    public static void main(String[] args) {
        Derived1 derived1Instance = new Derived1();
        Derived2 derived2Instance = new Derived2();
        derived1Instance.m(12);
        derived2Instance.m(12);
    }

}
