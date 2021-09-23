package mutualrec.non_term.example;

/*
 * EO code:
 * +package sandbox
 * +alias stdout org.eolang.io.stdout
 * +alias sprintf org.eolang.txt.sprintf
 *
 * [] > base
 *   memory > x
 *   [self v] > f
 *     x.write > @
 *       v
 *   [self v] > g
 *     self.f > @
 *       self
 *       v
 * [] > derived
 *   base > @
 *   [self v] > f
 *     self.g > @
 *       self
 *       v
 */

class Base {
    public int x;

    public void f(int v) {
        this.x = v;
    }

    public void g(int v) {
        this.f(v);
    }
}

class Derived extends Base {
    @Override
    public void f(int v) {
        this.g(v);
    }
}

public class MutualRecursionExample {
    public static void main(String[] args) {
        Derived derivedInstance = new Derived();
        derivedInstance.g(10);
    }
}
