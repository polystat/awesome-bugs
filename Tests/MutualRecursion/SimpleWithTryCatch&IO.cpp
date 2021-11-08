#include <stdexcept>
#include <ios>

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

        try
        {
            try {

                сin >> this->x;
            }
            catch (const std::ios_base::failure& fail) {
                this->m(v);
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
    derivedInstance->m(10);

    return 0;
}
