
class FloatToInt {
public:
    static int returnedValue(int a) {
        return 5 / a;
    }

    static int unsignedToSigned(unsigned short a) {
        return 5 / a;
    }

};

int main() {
    FloatToInt::returnedValue(0.55);
    FloatToInt::unsignedToSigned(1 << 16);
    return 0;
}