#include "../decleration_files/Object.h"
#include <iostream>

Object::Object(sf::Vector2f const &pos, sf::Texture &texture)
    : sprite{texture}, /*obj_name{name},*/ existing{true}
{
    sprite.setPosition(pos);
    auto size{texture.getSize()};
    sprite.setOrigin(size.x / 2, size.y / 2);
}
bool Object::collision(Object const &ob1, Object const &ob2)
{
    auto ob1_b{ob1.sprite.getGlobalBounds()};
    auto ob2_b{ob2.sprite.getGlobalBounds()};
    return ob1_b.intersects(ob2_b);
}

Moving_Object::Moving_Object(sf::Vector2f const &pos, sf::Texture &texture)
    : Object{pos, texture}
{
}
void Object::move(int const m_speed, char const direction) //borde ligga i moving men :(
{
    old_pos = sprite.getPosition();
    
    if (direction == 'U')
    {
        sprite.setRotation(180);
        sprite.move(0, -m_speed);
    }
    else if (direction == 'D')
    {
        sprite.setRotation(0);
        sprite.move(0, m_speed);
    }
    else if (direction == 'L')
    {
        sprite.setRotation(90);
        sprite.move(-m_speed, 0);
    }
    else if (direction == 'R')
    {
        sprite.setRotation(-90);
        sprite.move(m_speed, 0);
    }
    else if (direction == 'E')
    {
        sprite.setRotation(-135);
        sprite.move(m_speed, -m_speed);
    }
    else if (direction == 'Q')
    {
        sprite.setRotation(135);
        sprite.move(-m_speed, -m_speed);
    }
    else if (direction == 'Z')
    {
        sprite.setRotation(45);
        sprite.move(-m_speed, m_speed);
    }
    else if (direction == 'X')
    {
        sprite.setRotation(-45);
        sprite.move(m_speed, m_speed);
    }
}

sf::Sprite Object::get_sprite() const
{
    return sprite;
}

sf::Vector2f Object::get_obj_pos() const
{
    return sprite.getPosition();
}

void Object::not_existing()
{existing = false;}

bool Object::is_existing() const
{return existing;}
