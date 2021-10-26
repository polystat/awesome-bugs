int main() {
    const int size = 10;
    int a[size];
    // Bug_here
    a[size] = 1;

    return 0;
}