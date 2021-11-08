#include <random>

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
        int randomNumber = rand();
        if (randomNumber % 3 == 10) {
            this->m(v);
        }
    }
};

int main() {
    Base* derivedInstance = new Derived();
    derivedInstance->m(10);

    return 0;
}
