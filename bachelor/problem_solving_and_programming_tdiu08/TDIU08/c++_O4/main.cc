// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program
#include "hero_handling.h"
#include "register_handling.h"
#include <iostream>
#include <vector>
#include <iomanip>
#include <sstream>

using namespace std;

void add_hero(Register_Type &hero_list, string const &file_name)
{
    while (true)
    {
        cout << "Enter hero information:" << endl;

        if (not new_hero(hero_list, file_name))
        {
            cout << "Hero already in register. ";
        }
        else
        {
            break;
        }
    }
    cout << "The hero was added to the register on file " << file_name << endl;
}

void print_match(Register_Type const& hero_list, vector<int> const& interests) {
    Register_Type match;
    match = Searching(hero_list, interests);

    cout << "There are " << match.size() << " matching heroes." << endl;
    cout << "Hero name  Birth year  Weight  Hair color  Interests" << endl;
    cout << "====================================================" << endl;
    print_h(cout, match);
}

void hero_match(Register_Type &hero_list) {
    vector<int> interests;
    string input;
    int num;

    cout << "Enter your interests (at least one between 1 and 15): ";

    while (true) {
        getline(cin, input);
        stringstream ss(input);

        while (ss >> num) {
            if (num >= 1 && num <= 15) {
                interests.push_back(num);
            }
        }

        if (!interests.empty()) {
            break;
        }
    }
    print_match(hero_list, interests);
}

void menu(Register_Type &hero_list, string const &file_name) {
    int option;
    cout << "Welcome to Hero Matchmaker 3000!" << endl;
    while (true) {
        cout << "1) Add new hero to register file" << endl;
        cout << "2) Find matching heroes" << endl;
        cout << "3) Quit program" << endl;

        while (true) {
            cout << "Select: ";
            cin >> option;

            if ((option > 0) and (option <= 3)) {
                break;
            }
        }

        if (option == 1) {
            add_hero(hero_list, file_name);
        } else if (option == 2) {
            hero_match(hero_list);
        } else if (option == 3) {
            break;
        }
    }

    cout << "Terminating Hero Matchmaker 3000!" << endl;
}

int main(int argc, char *argv[])
{
    ifstream file_h;
    Register_Type hero_list;

    if (argc != 2)
    {
        cout << "Incorrect number of arguments!" << endl
             << "Usage: " << argv[0] << " REGISTERFILE";
    }
    else
    {
        file_h.open(argv[1]);
        hero_list = read_file(file_h);
        file_h.close();
        menu(hero_list, argv[1]);
    }
    return 0;
}
