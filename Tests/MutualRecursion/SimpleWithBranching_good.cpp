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

    int getX() { return x; }
    void setX(int v) { x = v; }
};

class Derived : public Base {

public:
    virtual void n(int v) override {
        if (false) {
            this->m(v);
        }
        else {
            this->x++;
        }
    }
};

int main() {
    Base *derivedInstance = new Derived();
    derivedInstance->m(10);

    return 0;
}
