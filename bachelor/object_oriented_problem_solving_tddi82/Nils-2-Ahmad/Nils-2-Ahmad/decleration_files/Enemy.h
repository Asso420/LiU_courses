#ifndef Enemy_h
#define Enemy_h
#include "Object.h"
#include "Bomb.h"
#include <string>

class Bomb;

class Enemy : public Moving_Object
{
public:
    Enemy(sf::Vector2f const &pos);
    void handle_collision(Object &obj_2) override;
    int get_move_speed() const;

protected:
    int move_speed;
};
#endif