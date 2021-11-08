
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

[] > derived_again
  derived > @
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

    void m(int v) {
        this->n(v);
    }
};

class Derived : public Base {

};

class DerivedAgain : public Derived {
public:

    virtual void n(int v) override {
        this->m(v);
    }
};

//int main() {
//    Base *derivedAgainInstance = new DerivedAgain();
//    derivedAgainInstance->m(12);
//}
