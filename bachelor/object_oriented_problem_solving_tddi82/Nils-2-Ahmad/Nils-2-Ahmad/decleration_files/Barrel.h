#ifndef Barrel_h
#define Barrel_h 
#include "Object.h"
#include <SFML/Graphics.hpp>

class Barrel : public Object
{
    public: 
    Barrel(sf::Vector2f const& pos);
    void handle_collision(Object & obj_2) override;
    
    //sf::Sprite get_sprite() const;
};

#endif
