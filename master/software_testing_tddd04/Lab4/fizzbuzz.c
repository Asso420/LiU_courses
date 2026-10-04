//Simple fizzbuzz may or may not be correct
#include <stdio.h>

void fizz_buzz()
{
    for (int i = 1; i < 35; ++i) {
    //% is the modulo operator in C.
        if (i % 3 == 0 && i % 5 == 0) {
            printf("Fizz!Buzz!\n");
        } else if (i % 3 == 0){
            printf("Fizz\n");
        } else if (i % 5 == 0) {
            printf("Buzz\n");
        } else {
            printf("%d\n", i);
        }
    }
}
void main()
{
    fizz_buzz();
}