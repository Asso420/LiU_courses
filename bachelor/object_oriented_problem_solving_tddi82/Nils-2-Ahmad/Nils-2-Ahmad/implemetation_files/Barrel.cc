#include "../decleration_files/Barrel.h"
#include "../decleration_files/Bomb.h"
#include "Manager.cc"

Barrel::Barrel(sf::Vector2f const &pos)
    : Object{pos, Manager<sf::Texture>::load("resources/Barrel.png")}
{
    sprite.setScale(0.5, 0.5);
}
void Barrel::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Explossion*>(&obj_2) != nullptr)
    {
        existing = false;
    }
}