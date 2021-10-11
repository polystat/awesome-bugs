#include <malloc.h>

int main() {
    char* pStr = (char*)malloc(20);
    free(pStr);
    free(pStr);

    return 0;
}