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

    virtual ~Base() {}
};

class Derived : public Base {
public:
    virtual void n(int v) override {
        if (this->x > this->y) {
            this->m(v);
        }
        else {
            this->x++;
        }
    }
};

int main() {
    Base* derivedInstance = new Derived();
    derivedInstance->n(10);
    derivedInstance->m(10);
    delete derivedInstance;

    return 0;
}
