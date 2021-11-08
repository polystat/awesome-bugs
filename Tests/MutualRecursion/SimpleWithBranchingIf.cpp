class Base {
protected:
    int x;

public:
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
    virtual void n(int v) override {
        if (this->x == 0) {
            this->x++;
        }
        else {
            this->m(v);
        }
    }
};

int main() {
    Base *derivedInstance = new Derived();
    //derivedInstance->n(10);
    derivedInstance->m(10);

    return 0;
}
