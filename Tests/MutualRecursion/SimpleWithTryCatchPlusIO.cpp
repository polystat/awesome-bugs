#include <stdexcept>
#include <iostream>

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
            std::cin.exceptions(std::istream::failbit | std::istream::badbit);
            std::cin >> this->x;
        }
        catch (const std::ios_base::failure& fail) {
            this->m(v);
        }
        catch (const std::exception)
        {
            this->m(v);
        }
    }
};

int main() {
    Base* derivedInstance = new Derived();
    derivedInstance->m(10);
    delete derivedInstance;

    return 0;
}
