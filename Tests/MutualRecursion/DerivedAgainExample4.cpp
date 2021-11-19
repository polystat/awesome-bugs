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
public:
    void o(int v) {
        this->m(v);
    }
};

class DerivedAgain : public Derived {
public:
    void n(int v) override {
        this->o(v);
    }
};

int main() {
    Base *derivedAgainInstance = new DerivedAgain();
    derivedAgainInstance->m(12);
    delete derivedAgainInstance;

    return 0;
}
