#ifndef Wall_h
#define Wall_h

#include "Object.h"
#include <SFML/Graphics.hpp>


class Wall : public Object
{
public:
    Wall(sf::Vector2f const& pos);
    void handle_collision(Object & obj_2) override;
};

#endif
