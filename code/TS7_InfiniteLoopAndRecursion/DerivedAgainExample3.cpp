class Base {
public:
    int x;

    Base() {
        this->x = 0;
    }

    virtual void n(int v) {
        this->x = v;
    }

};

class Derived : public Base {
public:

    void m(int v) {
        this->n(v);
    }

};

class DerivedAgain : public Derived {
public:

    void n(int v) override {
        this->m(v);
    }

};
//
//int main() {
//    auto *derivedAgainInstance = new DerivedAgain();
//    derivedAgainInstance->n(12);
//    return 0;
//}
