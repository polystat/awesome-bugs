
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
public:
    int x;

    Base() {
        this->x = 0;
    }

    virtual void f(int v) {
        this->x = v;
    }

    void g(int v) {
        this->f(v);
    }
};

class Derived : public Base {

public:
    void f(int v) override {
        this->g(v);
    }

};

int main() {
    auto *derivedInstance = new Derived();
    derivedInstance->g(10);
}
