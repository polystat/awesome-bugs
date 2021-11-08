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

    virtual void n(int v) override {
        this->m(v);
    }

};
//
//int main() {
//    Base *derivedAgainInstance = new DerivedAgain();
//    derivedAgainInstance->m(12);

//    return 0;
//}
