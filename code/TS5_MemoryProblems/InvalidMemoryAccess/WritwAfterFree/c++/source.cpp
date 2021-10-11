#include <malloc.h>
#include <cstring>

int main() {
    char* pStr = (char*)malloc(25);
    free(pStr);
    strcpy(pStr, "test string");

    return 0;
}