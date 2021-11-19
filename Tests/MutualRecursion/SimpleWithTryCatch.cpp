#include <stdexcept>

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

    virtual ~Base() {}
};

class Derived : public Base {
public:
    virtual void n(int v) override {
        try
        {
            if (this->x == 0) {
                this->x--;
            }
            else {
                throw std::invalid_argument("received negative value");
            }
        }
        catch (const std::exception)
        {
            this->m(v);
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
