#include "../decleration_files/ZigZagEnemy.h"
#include "../decleration_files/Enemy.h"
#include "../decleration_files/Wall.h"
#include "../decleration_files/Barrel.h"
#include "Manager.cc"

#include <string>
#include <SFML/Graphics.hpp>
#include <iostream>

ZigZagEnemy::ZigZagEnemy(sf::Vector2f const &pos)
  : Enemy{pos},
    dx{1}, dy{1}
{
    move_speed = 50;
    dx = (rand() % 2) ? 1 : -1;
    dy = (rand() % 2) ? 1 : -1;
}

void ZigZagEnemy::update(float dt) {
    float speed = static_cast<float>(get_move_speed());
    sf::Vector2f delta{ dx * speed * dt, dy * speed * dt };
    old_pos = sprite.getPosition();
    sprite.move(delta);
}

void ZigZagEnemy::handle_collision(Object &other) {
    sprite.setPosition(old_pos);

    if (dynamic_cast<Wall*>(&other) ||
        dynamic_cast<Barrel*>(&other) ||
        dynamic_cast<Bomb*>(&other))
    {
        int choice = rand() % 3;
        if (choice == 0)      dx = -dx;
        else if (choice == 1) dy = -dy;
        else { dx = -dx; dy = -dy; }
    }
}