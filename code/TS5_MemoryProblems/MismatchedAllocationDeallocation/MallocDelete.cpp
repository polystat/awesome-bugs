#include <malloc.h>

int main() {
    char* s = (char*)malloc(5);
    delete s;
    
    return 0;
}