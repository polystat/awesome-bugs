int main() {
    char* str = new char[30];
    str = new char[60]; 
    delete[] str;

    return 0;
}