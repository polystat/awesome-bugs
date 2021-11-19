class INClass
{
public:
    virtual ~INClass() {}
    virtual void n(int v) = 0;
};

class IMClass
{
public:
    virtual ~IMClass() {}
    virtual void m(int v) = 0;
};

class Base: public INClass, public IMClass {
public:
    int x;

    Base() {
        this->x = 0;
    }

    virtual void n(int v) override {
        this->x = v;
    }

    virtual void m(int v) override {
        this->n(v);
    }

    virtual ~Base() {}
};

class Derived : public Base {
public:
    virtual void n(int v) override {
        this->m(v);
    }
};

int main() {
    Base *derivedInstance = new Derived();
    derivedInstance->m(10);
    delete derivedInstance;

    return 0;
}
