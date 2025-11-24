// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program
#include "hero_handling.h"
#include "register_handling.h"
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>

using namespace std;
bool read(ifstream &file_h, Hero_Type &hero) {
    int int_array{};
    string line;

    if (!(file_h >> hero.name)) {
        return false;
    } else {
        file_h >> hero.birth >> hero.weight >> hero.hair;
        getline(file_h, line);
        stringstream ss(line);

        while (ss >> int_array) {
            hero.interests.push_back(int_array);
        }
        return true;
    }
}


