#ifndef Abilities_h
#define Abilities_h
#include "Object.h"
#include "Player.h"

class Ability : public Object
{
public:
  Ability(sf::Vector2f const &pos, sf::Texture &texture);
};

class Inc_Bomb_Amount : public Ability
{
public:
  Inc_Bomb_Amount(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

class Inc_Life : public Ability
{
public:
  Inc_Life(sf::Vector2f const &pos);
  void inc_life(Player &p);
  void handle_collision(Object &obj_2) override;
};

class Inc_Bomb_Size : public Ability
{
public:
  Inc_Bomb_Size(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

class Inc_Move_Speed : public Ability
{
public:
  Inc_Move_Speed(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

class Give_Shield : public Ability
{
public:
  Give_Shield(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

class Give_Knife : public Ability
{
public:
  Give_Knife(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

class Give_Kick_Bomb : public Ability
{
public:
  Give_Kick_Bomb(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

class Give_Ghost_Ability : public Ability
{
public:
  Give_Ghost_Ability(sf::Vector2f const &pos);
  void handle_collision(Object &obj_2) override;
};

#endif
