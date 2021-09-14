
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
public:
    int x;

    Base() {
        this->x = 0;
    }

    virtual void n(int v) {
        this->x = v;
    }

    void m(int v) {
        this->n(v);
    }
};

class Derived : public Base {
public:

    void n(int v) override {
        this->m(v);
    }

};

class DerivedAgain : public Derived {

};

int main() {
    auto *derivedAgainInstance = new DerivedAgain();
    derivedAgainInstance->n(12);
}
