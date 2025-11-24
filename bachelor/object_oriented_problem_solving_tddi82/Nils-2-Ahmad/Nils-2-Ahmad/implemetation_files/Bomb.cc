#include <SFML/Graphics.hpp>
#include "../decleration_files/Bomb.h"
#include "Manager.cc"
#include <iostream>
#include "../decleration_files/Game_state.h"

//class Game_State;

Bomb::Bomb(int const s, sf::Vector2f const &pos, bool const P_id)
    : Moving_Object{pos,
                    Manager<sf::Texture>::load("resources/Bomb.png")},
      bomb_size{s}, Player1{P_id}
{
    sprite.setScale(0.1, 0.1);
    time.restart();
}
void Bomb::handle_collision(Object &obj_2)
{
    if(dynamic_cast<Wall*>(&obj_2) != nullptr || dynamic_cast<Barrel*>(&obj_2) != nullptr)
    {
        if(is_moving)
        {
            explode = true;
        }
    }
    
    else if(dynamic_cast<Player*>(&obj_2) != nullptr)
    {
     Player p {dynamic_cast<Player&>(obj_2)};
     if(!p.check_kick() && is_moving)
     {
        explode = true;
     }
     else if(p.check_kick() && p.get_bomb_place_timer().getElapsedTime().asSeconds() >= 0.5)
        {
            is_moving = true;
            auto diff_x{p.get_obj_pos().x - sprite.getPosition().x};
            auto diff_y{p.get_obj_pos().y - sprite.getPosition().y};
            if (std::abs(diff_x) > std::abs(diff_y))
            {
                if (p.get_obj_pos().x >= sprite.getPosition().x)
                {
                    direction = 'L';
                }
                else
                {
                    direction = 'R';
                }
            }
            else
            {
                if (p.get_obj_pos().y >= sprite.getPosition().y)
                {
                    direction = 'U';
                }
                else
                {
                    direction = 'D';
                }
            }
        }   
    }
}



Explossion::Explossion(sf::Vector2f pos, int ex)
    : Object{pos, Manager<sf::Texture>::load("resources/explosion.png")}, ex_size{ex}
{
    sprite.setScale(0.6, 0.6);
    time.restart();
}

void Explossion::rot(double b_size)
{
    sf::Vector2f originalPosition = sprite.getPosition();
    double originalRotation = sprite.getRotation();

    sprite.setPosition(originalPosition.x, originalPosition.y - b_size);
    sprite.setRotation(originalRotation);

    sprite.setPosition(originalPosition.x + b_size, originalPosition.y);
    sprite.setRotation(originalRotation + 90.f);

    sprite.setPosition(originalPosition.x, originalPosition.y + b_size);
    sprite.setRotation(originalRotation + 180.f);

    sprite.setPosition(originalPosition.x - b_size, originalPosition.y);
    sprite.setRotation(originalRotation + 270.f);
}

void Explossion::handle_collision(Object &obj_2)
{
}

void Explossion::exploded()
{
}

char Bomb::get_direction() const
{
    return direction;
}

bool Bomb::check_explode() const
{return explode;}
