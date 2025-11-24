#include "../decleration_files/Abilities.h"
#include "Manager.cc"

Ability::Ability(sf::Vector2f const &pos, sf::Texture &texture)
    : Object{pos, texture}
{
}

Inc_Bomb_Amount::Inc_Bomb_Amount(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Bomb_Ability.png")}
{
    sprite.setScale(0.09, 0.09);
}

void Inc_Bomb_Amount::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Inc_Life::Inc_Life(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Life.png")}
{
    sprite.setScale(0.09, 0.09);
}

void Inc_Life::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Inc_Bomb_Size::Inc_Bomb_Size(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Bomb_Size.png")} // byyyyyt
{
    sprite.setScale(0.1, 0.1);
}

void Inc_Bomb_Size::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Inc_Move_Speed::Inc_Move_Speed(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/MS.png")}
{
    sprite.setScale(0.15, 0.15);
}

void Inc_Move_Speed::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Give_Shield::Give_Shield(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Shield_Powerup.png")}
{
    sprite.setScale(0.07, 0.07);
}

void Give_Shield::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Give_Knife::Give_Knife(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Knife_Powerup.png")}
{
    sprite.setScale(0.09, 0.09);
}

void Give_Knife::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Give_Kick_Bomb::Give_Kick_Bomb(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Kick_Powerup.png")}
{
    sprite.setScale(0.07, 0.07);
}

void Give_Kick_Bomb::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}

Give_Ghost_Ability::Give_Ghost_Ability(sf::Vector2f const &pos)
    : Ability{pos, Manager<sf::Texture>::load("resources/Ghost_Powerup.png")}
{
    sprite.setScale(0.1, 0.1);
}

void Give_Ghost_Ability::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
        not_existing();
    }
}
