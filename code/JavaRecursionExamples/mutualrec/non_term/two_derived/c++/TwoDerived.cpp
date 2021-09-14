
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
public:
    int x;

    Base() {
        this->x = 0;
    }

    virtual void n(int v) {
        this->x = v;
    }

    virtual void m(int v) {
        this->n(v);
    }
};

class Derived1 : public Base {

public:
    void m(int v) override {
        this->n(v);
    }

    void n(int v) override {
        this->m(v);
    }
};

class Derived2 : public Base {

public:
    void m(int v) override {
        this->n(v);
    }

    void n(int v) override {
        this->m(v);
    }
};


int main() {
    auto *derived1Instance = new Derived1();
    auto *derived2Instance = new Derived2();
    derived1Instance->m(12);
    derived2Instance->m(12);
    return 0;
}
