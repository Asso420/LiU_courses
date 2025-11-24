#ifndef PATHING_ENEMY_H
#define PATHING_ENEMY_H

#include "Enemy.h"
#include "Object.h"
#include "Bomb.h"


// This class is used to create a chase enemy that chases the player when they are within a certain radius.
class ChaseEnemy : public Enemy {
public:
    explicit ChaseEnemy(sf::Vector2f const &pos);

    void update(sf::Vector2f const &player_pos, float dt);

private:
    float reach_threshold; 
    float chase_radius;   
};

#endif
