#include "../decleration_files/Player.h"
#include "../decleration_files/Wall.h"
#include "Manager.cc"

#include <SFML/Graphics.hpp>

Wall::Wall(sf::Vector2f const &pos)
    : Object{pos,
             Manager<sf::Texture>::load("resources/Wall.png")}
{
    sprite.setScale(0.5, 0.5);
}
void Wall::handle_collision(Object &obj_2)
{
}
