#include <iostream>

class NumericToBoolean {
public:
    static void implicitBoolConversions() {
        int a = 0.23;

        while (!a) {
            std::cout << a;
        }

        int b = -1;

        while (b) {
            std::cout << b;
        }

    }

};

int main() {
    NumericToBoolean::implicitBoolConversions();
    return 0;
}