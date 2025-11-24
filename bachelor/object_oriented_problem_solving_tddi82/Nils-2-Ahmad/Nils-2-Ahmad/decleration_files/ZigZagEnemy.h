#ifndef RANDOM_ENEMY_H
#define RANDOM_ENEMY_H

#include "Enemy.h"
#include "Object.h"
#include "Bomb.h"

// This class is used to create a zigzag enemy that moves in a zigzag pattern.

class ZigZagEnemy : public Enemy {
public:
    explicit ZigZagEnemy(sf::Vector2f const &pos);

    void update(float dt);
    void handle_collision(Object &other) override;

private:
    int dx, dy;

};

#endif
