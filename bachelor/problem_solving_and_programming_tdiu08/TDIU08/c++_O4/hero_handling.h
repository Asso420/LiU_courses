// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program
#ifndef HERO_HANDLING_H
#define HERO_HANDLING_H
#include <vector>
#include <string>
#include <fstream>

struct Hero_Type
{
  std::string name{};
  int birth{};
  double weight{};
  std::string hair{};
  std::vector <int> interests{};
};

bool read(std::ifstream  & file_h,
	        Hero_Type & hero);
#endif 
