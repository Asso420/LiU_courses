#include <klee/klee.h>
#include <assert.h>
#include <stdio.h>


int getClientDetuctible (int clientAge, int yearOfLicence, int numberOfAccident, int isGoldMember){
    int base = 8000;
    if (clientAge > 30 || yearOfLicence > 5) {
        base = 5000;
    }

    int inc;

    if (isGoldMember){
        if (numberOfAccident <= 2) inc = 0;
        else if (numberOfAccident == 3) inc = 4000;
        else inc = 10000;
    }   else {
        if (numberOfAccident <= 0) inc = 0;
        else if (numberOfAccident == 1) inc = 1000;
        else if (numberOfAccident == 2) inc = 2500;
        else if (numberOfAccident == 3) inc = 4000;
        else inc = 10000;

    }

    return base + inc;

}


int main() {
    int clientAge, yearOfLicence, numberOfAccident, isGoldMember;

    klee_make_symbolic(&clientAge, sizeof(clientAge), "clientAge");
    klee_make_symbolic(&numberOfAccident, sizeof(numberOfAccident), "numberOfAccident");
    klee_make_symbolic(&yearOfLicence, sizeof(yearOfLicence), "yearOfLincence");
    klee_make_symbolic(&isGoldMember, sizeof(isGoldMember), "isGoldMember");

    int d = getClientDetuctible(clientAge, yearOfLicence, numberOfAccident, isGoldMember);
    // printf("%d\n", clientAge);
    // printf("%d\n", yearOfLicence);
    // printf("%d\n", numberOfAccident);
    // printf("%d\n", isGoldMember);
    // printf("%d\n", d);

    assert(d > 5000 || d < 18000 );                                                                 // should pass

    if ( (clientAge > 30 || yearOfLicence > 5) && numberOfAccident == 2 && isGoldMember == 0 ) {    // should pass
        assert(d == 7500);
    }

    assert (clientAge >= 18);

    if ( (clientAge > 30 || yearOfLicence > 5) && numberOfAccident == 2 && isGoldMember == 0 ) {    // should fail
    assert(d == 6500);
    }
}