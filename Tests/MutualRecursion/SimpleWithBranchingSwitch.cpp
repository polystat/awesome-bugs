class Base {
protected:
    int x;
    int y;

public:
    Base() {
        this->x = 0;
        this->y = 0;
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
    virtual void n(int v) override {
        switch (this->x) {
            case 0: { this->x++; break; }
            case 1: { this->x+=2; break; }
            case 2: { this->m(v); break; }
            default: { this->m(v); }
        }
    }
};

int main() {
    Base* derivedInstance = new Derived();
    //derivedInstance->n(10);
    //derivedInstance->n(10);
    derivedInstance->m(10);

    return 0;
}
