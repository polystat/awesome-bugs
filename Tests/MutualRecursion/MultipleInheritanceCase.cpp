class NClass {
private:
    int x;
public:
    virtual ~NClass() {}
    virtual void n(int v) {
        this->x = v;
    }
};

class MClass {
private:
    int y;
public:
    virtual ~MClass() {}
    virtual void m(int v) {
        this->y = v;
    }
};

class Base : public NClass, public MClass {
public:
    virtual void m(int v) override {
        this->n(v);
    }
};

class Derived : public Base {
public:
    virtual void n(int v) override {
        this->m(v);
    }
};

int main() {
    Base* derivedInstance = new Derived();
    derivedInstance->n(10);
    delete derivedInstance;

    return 0;
}
