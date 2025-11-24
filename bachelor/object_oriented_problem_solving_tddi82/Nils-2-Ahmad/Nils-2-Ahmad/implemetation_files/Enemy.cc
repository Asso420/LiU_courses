#include "../decleration_files/Enemy.h"
#include "../decleration_files/Wall.h"
#include "../decleration_files/Barrel.h"
#include "Manager.cc"

#include <string>
#include <SFML/Graphics.hpp>
#include <iostream>

Enemy::Enemy(sf::Vector2f const &pos)
    : Moving_Object{pos,
                    Manager<sf::Texture>::load("resources/pixel3.png")},
      move_speed{4}
{
  sprite.setScale(1.5, 1.5);
  old_pos = sprite.getPosition();
}

void Enemy::handle_collision(Object &obj_2)
{
  if ((dynamic_cast<Wall*>(&obj_2) != nullptr) ||
      ((dynamic_cast<Barrel*>(&obj_2) != nullptr)) ||
      ((dynamic_cast<Bomb*>(&obj_2) != nullptr)))
  {
    sprite.setPosition(old_pos);
  }
}

int Enemy::get_move_speed() const
{
  return move_speed;
}
