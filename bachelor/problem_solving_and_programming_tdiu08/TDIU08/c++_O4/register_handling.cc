// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program
#include "register_handling.h"
#include "hero_handling.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <algorithm>
#include <sstream>

using namespace std;

bool operator<(Hero_Type const &lhs,
               Hero_Type const &rhs)
{
    return (lhs.name < rhs.name);
}

void sorting(Register_Type &heroes)
{
    for (Hero_Type &hero : heroes)
    {
        sort(begin(hero.interests), end(hero.interests));
    }
    sort(begin(heroes), end(heroes));
}

void print_h(ostream &file,
             Register_Type const &Heroes)
{
    file << fixed << setprecision(2);

    for (int i{}; i < Heroes.size(); i++)
    {
        file << setw(11) << left << Heroes.at(i).name;
        file << setw(12) << Heroes.at(i).birth;
        file << setw(8) << Heroes.at(i).weight;
        file << setw(12) << Heroes.at(i).hair;

        for (int k{}; k < Heroes.at(i).interests.size(); k++)
        {
            file << setw(3) << right << Heroes.at(i).interests.at(k);
        }

        file << endl;
    }
}

void write(Register_Type &Heroes,
           string const &file_name)
{
    ofstream hero_file(file_name, ios::out);

    print_h(hero_file, Heroes);
    hero_file.close();
}

vector<int> load_interest()
{
    vector<int> numb;
    int value;
    string s;

    getline(cin, s);
    stringstream ss(s);

    while (ss >> value)
    {
        numb.push_back(value);
    }
    return numb;
}

bool new_hero(Register_Type &Heroes,
              string const &file_name)
{
    Hero_Type temp;
    cin >> temp.name >> temp.birth >> temp.weight >> temp.hair;
    temp.interests = load_interest();

    for (const Hero_Type &hero : Heroes)
    {
        if (hero.name == temp.name)
        {
            return false;
        }
    }
    Heroes.push_back(temp);
    sorting(Heroes);
    write(Heroes, file_name);
    return true;
}

Register_Type read_file(ifstream &file_h)
{
    Hero_Type hero{};
    Register_Type heroes;

    while (read(file_h, hero))
    {
        heroes.push_back(hero);
        hero.interests.clear();
    }

    return heroes;
}

bool there_Is_one(const Register_Type &match,
                  const Hero_Type &hero)
{
    for (const Hero_Type &Hero : match)
    {
        if (Hero.name == hero.name)
        {
            return true;
        }
    }
    return false;
}

Register_Type Searching(const Register_Type &heroes, const vector<int> &numb)
{
    Register_Type match{};

    for (const Hero_Type &current_hero : heroes)
    {
        for (int interest : current_hero.interests)
        {
            if (find(numb.begin(), numb.end(), interest) != numb.end() &&
                not there_Is_one(match, current_hero))
            {
                match.push_back(current_hero);
                break;
            }
        }
    }

    sorting(match);
    return match;
}
