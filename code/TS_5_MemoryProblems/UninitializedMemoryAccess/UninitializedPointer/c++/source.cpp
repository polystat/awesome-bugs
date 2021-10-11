#include <malloc.h>

int main() {
    char* pStr = (char*)malloc(256);
    char c = pStr[0];

    return 0;
}