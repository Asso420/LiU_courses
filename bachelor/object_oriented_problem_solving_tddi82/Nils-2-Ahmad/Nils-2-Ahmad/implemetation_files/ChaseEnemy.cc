#include "../decleration_files/ChaseEnemy.h"
#include "../decleration_files/Enemy.h"
#include "../decleration_files/Wall.h"
#include "../decleration_files/Barrel.h"
#include "Manager.cc"
#include <cmath>

#include <string>
#include <SFML/Graphics.hpp>
#include <iostream>

ChaseEnemy::ChaseEnemy(sf::Vector2f const &pos)
  : Enemy{pos}
  , chase_radius{200.0f}                      
  , reach_threshold{12.0f}         

{
    move_speed = 100;              
}

void ChaseEnemy::update(sf::Vector2f const &player_pos, float dt) {
    sf::Vector2f current = sprite.getPosition();

    sf::Vector2f dir = player_pos - current;
    float dist = std::sqrt(dir.x * dir.x + dir.y * dir.y);

    if (dist > chase_radius)
        return;

    if (dist < reach_threshold)
        return;

    dir /= dist;
    old_pos = current;

    float velocity = static_cast<float>(move_speed) * dt;

    sprite.move(dir * velocity);
}
