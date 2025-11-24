#ifndef UTILITY_H
#define UTILITY_H

#include <random>

int generateRandomNumber(int min, int max) {
  static std::random_device rd;
  static std::mt19937 rng(rd());
  std::uniform_int_distribution<int> uni(min, max);
  return uni(rng);
}

#endif
