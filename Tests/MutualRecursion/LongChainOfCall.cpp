class Base {
public:
    int x;

    Base() {
        this->x = 0;
    }

    virtual void n(int v) {
        this->x = v;
    }

    void o(int v) {
        this->n(v);
    }

    void m(int v) {
        this->o(v);
    }
};

class Derived : public Base {
public:
    virtual void n(int v) override {
        this->m(v);
    }

    void l(int v) {
        this->m(v);
    }
};

int main() {
    Derived *derivedInstance = new Derived();
    derivedInstance->l(10);
    delete derivedInstance;

    return 0;
}
