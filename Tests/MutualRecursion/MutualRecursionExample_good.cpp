class Base {
public:
    int x;

    Base() {
        this->x = 0;
    }

    void f(int v) {
        this->x = v;
    }

    void g(int v) {
        this->f(v);
    }
};

class Derived : public Base {

public:
    void f(int v) {
        this->g(v);
    }
};

//int main() {
//    Base *derivedInstance = new Derived();
//    derivedInstance->g(10);
//    return 0;
//}
