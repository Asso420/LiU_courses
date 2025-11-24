#ifndef Game_state_h
#define Game_state_h
#include "Player.h"
#include "Enemy.h"
#include "Wall.h"
#include "Bomb.h"
#include "Barrel.h"
#include "Object.h"
#include "State.h"
#include "Abilities.h"
#include "../implemetation_files/Manager.cc"
#include <deque>
#include <vector>
#include <locale>
#include <memory>
#include "ChaseEnemy.h"
#include "ZigZagEnemy.h"


class Game_State : public State
{
public:
    Game_State();
    void update() override;
    void handle_event(sf::Event event, std::string & name_p1, std::string & name_p2) override;
    void render(sf::RenderTarget & target, std::string & name_p1, std::string & name_p2, bool & winner) override;
    virtual int get_next_state ();

   
private:

    Player P1;
    Player P2;

    ChaseEnemy E1;
    ZigZagEnemy E2;
    sf::Clock enemy_move_clock;
    sf::Clock enemy_direction_clock;

    std::vector<std::unique_ptr<Object>> Objects;
    char winner_id{};
    void move_players(float dt);
    void place_bombs(sf::Event event);
    void explode(Bomb & b);
    void all_collision();
    void explode_and_remove();
    void check_winners();
    void move_bombs();
    void is_stuck();
    bool is_collision(Enemy &enemy);
    std::vector<std::unique_ptr<Object>> static_obj_init(); 
    std::vector<std::unique_ptr<Object>> ability_spawner();
    void pop_nonexisting();
    sf::Vector2f calc_rand_pos();
    sf::Clock ability_spawn_time;
    bool end_game{false};
    sf::Font font{Manager<sf::Font>::load("resources/ARCADE.TTF")};
    sf::Sprite life_sprite{Manager<sf::Texture>::load("resources/Life.png")};
    sf::Sprite bomb_amount_sprite{Manager<sf::Texture>::load("resources/Bomb_Amount.png")};
    sf::Sprite background_sprite{Manager<sf::Texture>::load("resources/bg2.png")};
    sf::Sprite shield_ui{Manager<sf::Texture>::load("resources/Shield_Powerup.png")};
    sf::Sprite ghost_ui{Manager<sf::Texture>::load("resources/Ghost_Powerup.png")};
    sf::Sprite kick_ui{Manager<sf::Texture>::load("resources/Kick_Powerup.png")};
    sf::Sprite knife_ui{Manager<sf::Texture>::load("resources/Knife_Powerup.png")};
};

#endif
