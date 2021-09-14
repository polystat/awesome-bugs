package mutualrec.non_term.factory;

/*
+package sandbox
+alias stdout org.eolang.io.stdout
+alias sprintf org.eolang.txt.sprintf

[] > base_factory
  [] > get_base
    memory > x
    [self v] > n
      x.write v > @
    [self v] > m
      self.n self v > @

[] > derived
  base_factory.get_base > @
  [self v] > n
    self.m self v > @
 */

class BaseFactory {
    static class GetBase {
        public int x;

        public void n(int v) {
            this.x = v;
        }

        public void m(int v) {
            this.n(v);
        }
    }
}

class Derived extends BaseFactory.GetBase {
    @Override
    public void n(int v) {
        this.m(v);
    }
}

public class Factory {
    public static void main(String[] args) {
        Derived derivedInstance = new Derived();
        derivedInstance.m(12);
    }
}
