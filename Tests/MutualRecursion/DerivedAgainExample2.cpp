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

    virtual ~Base() {}
};

class Derived : public Base {

};

class DerivedAgain : public Derived {
public:
    virtual void n(int v) override {
        this->m(v);
    }
};

int main() {
    Base *derivedAgainInstance = new DerivedAgain();
    derivedAgainInstance->m(12);
    delete derivedAgainInstance;

    return 0;
}
