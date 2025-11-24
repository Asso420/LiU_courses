#ifndef STATE_H
#define STATE_H
#include <SFML/Graphics.hpp>
#include <string>


int const MENU_STATE{0};
int const GAME_STATE{1};
int const END_STATE{2};


class State
{
public:
    virtual ~State () = default;
    virtual void handle_event (sf::Event event, std::string & name_p1, std::string & name_p2) = 0;
    virtual void update () = 0;
    virtual void render(sf::RenderTarget & target, std::string & name_p1, std::string & name_p2, bool & winner) = 0;
    virtual int get_next_state() = 0;


    // std::string name_p1;
    // std::string name_p2;


};

#endif //STATE_H

