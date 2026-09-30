#include <stdio.h>

int add(int a, int b) {
    int c;
    c = a + b;
    return c;
}

int main()
{
    int x = add(3, 4);
    printf("Hello, world %d\n", x);
}
