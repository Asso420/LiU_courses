#ifndef Bomb_h
#define Bomb_h
#include "Object.h"
#include <SFML/Graphics.hpp>
#include <iomanip>
#include "Player.h"

class Player;

class Bomb : public Moving_Object
{
public:
    Bomb(int const s, sf::Vector2f const &pos, bool const P_id);
    char get_direction() const;
    void handle_collision(Object &obj_2) override;
    void handle_collision(Player const &p);
    bool check_explode() const;

    int bomb_size;
    sf::Clock time;
    bool Player1;
    bool is_moving{false};
private:
    bool explode{false};
    char direction;
    sf::Time duration;
};

class Explossion : public Object
{
public:
    Explossion(sf::Vector2f pos, int ex);
    void setPosition(sf::Vector2f newPosition);
    void handle_collision(Object &obj_2) override;
    void exploded();
    void rot(double b_size);
    sf::Vector2f getPosition() const;
    sf::Clock time;
    int bomb_size;
    double b_size;
    sf::Vector2f position;

private:
    int ex_size;
};

#endif
