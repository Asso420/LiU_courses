// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program
#include <iostream>
#include <iomanip>
#include <cctype>
#include <cstdio>
#include <cmath>

using namespace std;

int main() {
    // ########################Del_1#######################
    // del1 
    int start_value, last_value;
    double kelvin{}, fahrenheit{}, reaumur{};
    // del2
    char ch;
    int caps{}, alphas{}, numbers{};
    // del3
    string buff{}, text{}, longest_word{}, shortest_word{};
    int words{}, chars{};
    double average_char_count{};

    cout << "Del 1: Temperaturtabell" << '\n';
    cout << "Ange startvärde: ";
    cin >> start_value;

    while (start_value < -273) {
        cout << "Felaktigt startvärde!" << '\n';
        cout << "Ange startvärde: ";
        cin >> start_value;
    }

    cout << "Ange slutvärde: ";
    cin >> last_value;

    while (last_value < start_value) {
        cout << "Felaktigt slutvärde!" << '\n';
        cout << "Ange slutvärde: ";
        cin >> last_value;
    }

    cout << "Celsius   Kelvin   Fahrenheit   Reaumur" << '\n';
    cout << "---------------------------------------" << '\n';

    for (start_value; start_value <= last_value; start_value++) {
        kelvin = start_value + 273.15;
        fahrenheit = start_value * 1.8 + 32;
        reaumur = start_value * 0.8;
        cout << setw(7) << fixed << setprecision(0) << start_value;
        cout << setw(9) << fixed << setprecision(2) << kelvin;
        cout << setw(13) << fahrenheit;
        cout << setw(10) << reaumur << endl;
    }

    cout << "---------------------------------------" << "\n";
    cin.ignore(1000, '\n');

    // ########################Del2#####################################

    cout << "\nDel 2: Teckenhantering" << '\n';

    for (char i{0}; i < 10; i++) {
        cin.get(ch);
        if (isalpha(ch)) {
            alphas++;
        } else if (isspace(ch)) {
            caps++;
        } else if (isdigit(ch)) {
            numbers++;
        }
    }
    cin.ignore(1000, '\n');
    cout << "Texten innehöll:";
    cout << "\nAlfabetiska tecken:" << alphas << endl;
    cout << "Siffertecken......:" << numbers << endl;
    cout << "Vita tecken.......:" << caps << endl;

    // ########################Del_3####################

    cout << "\nDel 3: Ordhantering\n";
    cout << "Mata in en text:\n";

    while (cin >> buff) {
        chars += buff.size();

        if (shortest_word.empty()) {
            shortest_word = buff;
        } else if (buff.size() < shortest_word.size()) {
            shortest_word = buff;
        }

        if (buff.size() > longest_word.size()) {
            longest_word = buff;
        }

        words++;
    }

    if (words == 0) {
        cout << "\nInga ord matades in." << endl;
    } else {
        average_char_count = double(chars) / double(words);
        cout << "\n";
        cout << "Texten innehöll " << words << " ord." << endl;
        cout << "Det kortaste ordet var \"" << shortest_word << "\" med " << shortest_word.size() << " tecken." << endl;
        cout << "Det längsta ordet var \"" << longest_word << "\" med " << longest_word.size() << " tecken." << endl;
        cout << "Medelordlängden var " << setprecision(1) << average_char_count << " tecken." << endl;
    }
    cin.ignore(1000);
    return 0;
}
