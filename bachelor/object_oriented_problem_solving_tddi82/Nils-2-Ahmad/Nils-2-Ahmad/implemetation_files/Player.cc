#include "../decleration_files/Player.h"
#include "../decleration_files/Abilities.h"
#include "../decleration_files/Wall.h"
#include "../decleration_files/Barrel.h"
#include "../decleration_files/Bomb.h"
#include "Manager.cc"

#include <string>
#include <SFML/Graphics.hpp>
#include <iostream>

Player::Player(sf::Vector2f const &pos)
    : Moving_Object{pos,
                    Manager<sf::Texture>::load("resources/charart.png")},
      shield{false}, knife{false}, ghost_ability{false}, kick_bomb{false},
      life{3}, move_speed{4}, bomb_amount{2}, bomb_size{1}
{
  sprite.setScale(1.5, 1.5);
  old_pos = sprite.getPosition();
}

void Player::handle_collision(Player &killing_time)
{
  if (killing_time.knife && !killing_time.shield && !killing_time.invincible)
  {
    --life;
    killing_time.knife = false;
  }

  if (knife && !shield && !invincible)
  {
    killing_time.life--;
    knife = false;
  }

  if (killing_time.knife && killing_time.shield && killing_time.invincible)
  {
    killing_time.knife = false;
  }

  if (knife && shield && invincible)
  {
    knife = false;
  }
}

void Player::handle_collision(Object &obj_2)
{
  if ( (dynamic_cast<Wall*>(&obj_2) != nullptr) ||
      ((dynamic_cast<Barrel*>(&obj_2) != nullptr) && barrel_coll_on) ||
      ((dynamic_cast<Bomb*>(&obj_2) != nullptr) && bomb_coll_on))
  {
    sprite.setPosition(old_pos);
  }
  else if (dynamic_cast<Inc_Bomb_Amount*>(&obj_2) != nullptr)
  {
    bomb_amount++;
  }
  else if (dynamic_cast<Inc_Life*>(&obj_2) != nullptr)
  {
    ++life;
  }
  else if (dynamic_cast<Inc_Move_Speed*>(&obj_2) != nullptr)
  {
    move_speed += 2;
  }
  else if (dynamic_cast<Give_Shield*>(&obj_2) != nullptr)
  {
    shield = true;
    shield_timer.restart();
  }
  else if (dynamic_cast<Give_Knife*>(&obj_2) != nullptr)
  {
    knife = true;
    knife_timer.restart();
  }
  else if (dynamic_cast<Give_Kick_Bomb*>(&obj_2) != nullptr)
  {
    kick_bomb = true;
    kick_timer.restart();
  }
  else if (dynamic_cast<Give_Ghost_Ability*>(&obj_2) != nullptr)
  {
    ghost_ability = true;
    barrel_coll_on = false;
    ghost_timer.restart();
  }
  else if (dynamic_cast<Explossion*>(&obj_2) != nullptr && !shield && !invincible)
  {
    --life;
    invincible = true;
    bomb_timer.restart();
  }
  else if (dynamic_cast<Inc_Bomb_Size*>(&obj_2) != nullptr)
  {
    bomb_size++;
  }
}

void Player::place_bomb(std::vector<std::unique_ptr<Object>>& v, char const P_id) //auto är object vectorn 
{

  sf::Vector2f pos{sprite.getPosition()};
  if (P_id == '1')
  {
    v.push_back(std::make_unique<Bomb>(bomb_size, pos, true));
    bomb_place_timer.restart();
  }
  else
  {
    v.push_back(std::make_unique<Bomb>(bomb_size, pos, false));
    bomb_place_timer.restart();
  }

  --bomb_amount;
  bomb_timer.restart();
}

void Player::inc_bomb_amount()
{
  ++bomb_amount;
}

int Player::get_bomb_amount() const
{
  return bomb_amount;
}

int Player::get_move_speed() const
{
  return move_speed;
}

void Player::decrement_life()
{
  --life;
}

int Player::get_life_amount() const
{
  return life;
}

void Player::check_if_invincible()
{
  if (shield_timer.getElapsedTime().asSeconds() >= 15)
  {
    shield = false;
  }

  if (bomb_timer.getElapsedTime().asSeconds() >= 1)
  {
    invincible = false;
  }

  if (knife_timer.getElapsedTime().asSeconds() >= 15)
  {
    knife = false;
  }

  if (kick_timer.getElapsedTime().asSeconds() >= 10)
  {
    kick_bomb = false;
  }

  if (ghost_timer.getElapsedTime().asSeconds() >= 15)
  {
    ghost_ability = false;
  }
}
bool Player::check_if_bomb_coll() const
{
  return bomb_coll_on;
}

void Player::change_bomb_coll(bool b)
{
  bomb_coll_on = b;
}
void Player::change_barrel_coll(bool b)
{
  barrel_coll_on = b;
}
bool Player::check_if_barrel_coll() const
{
  return barrel_coll_on;
}

bool Player::check_shield() const
{
  return shield;
}

bool Player::check_kick() const
{
  return kick_bomb;
}

sf::Clock Player::get_bomb_place_timer() const
{
  return bomb_place_timer;
}

sf::Clock Player::get_bomb_timer() const
{
  return bomb_timer;
}

sf::Clock Player::get_ghost_timer() const
{
  return ghost_timer;
}

sf::Clock Player::get_place_timer() const
{
  return bomb_place_timer;
}
void Player::reset_place_clock()
{
  bomb_place_timer.restart();
}

bool Player::pick_knife() const
{
  return knife;
}
