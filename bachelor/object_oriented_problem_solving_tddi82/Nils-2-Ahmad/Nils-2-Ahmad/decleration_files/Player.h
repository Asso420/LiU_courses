#ifndef Player_h
#define Player_h
#include "Object.h"
#include "Bomb.h"
#include <string>

class Bomb;

class Player : public Moving_Object
{
public:
    Player(sf::Vector2f const &pos);
    void place_bomb(std::vector<std::unique_ptr<Object>>& v, char const P_id);
    void handle_collision(Player &killing_time);
    void handle_collision(Object &obj_2) override;
    int get_move_speed() const;
    void decrement_life();
    int get_bomb_amount() const;
    void inc_bomb_amount();
    int get_life_amount() const;
    sf::Clock get_bomb_place_timer()const;
    sf::Clock get_bomb_timer() const;
    sf::Clock get_ghost_timer() const;
    sf::Clock get_place_timer() const;
    void check_if_invincible();
    void change_bomb_coll(bool b);
    bool check_if_bomb_coll() const;
    void change_barrel_coll(bool b);
    bool check_if_barrel_coll() const;
    void reset_place_clock();
    bool check_shield() const;
    bool check_kick() const;
    bool pick_knife() const;

protected:
    bool shield;
    bool knife;
    bool kick_bomb;
    bool ghost_ability;
    bool invincible;
    bool barrel_coll_on{true};
    bool bomb_coll_on{false};
    int life;
    int move_speed;
    int bomb_amount;
    int bomb_size;
    sf::Clock bomb_place_timer;
    sf::Clock bomb_timer;
    sf::Clock ghost_timer;
    sf::Clock shield_timer;
    sf::Clock knife_timer;
    sf::Clock kick_timer;
};
#endif
