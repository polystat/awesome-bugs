int main() {
    const int size = 3;
    int a[size] {1,2,3};

    for (int i = 0; i < 5; i++)
    {
        //Bug_here
        a[i] ++;
    }

    return 0;
}