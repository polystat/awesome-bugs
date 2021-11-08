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
};

class Derived : public Base {

public:
    void n(int const &v) {
        this->m(v);
    }
};

int main() {
    Base *derivedInstance = new Derived();
    derivedInstance->m(10);

    return 0;
}
