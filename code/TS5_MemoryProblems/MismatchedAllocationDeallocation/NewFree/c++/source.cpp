#include <malloc.h>

int main() {
    char* s = new char[5];
    free(s);
    
    return 0;
}