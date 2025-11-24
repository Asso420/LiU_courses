#ifndef Game_h
#define Game_h

#include "constants.h"
#include "State.h"
#include <SFML/Graphics.hpp>
#include <string>
#include <memory>

class Game
{
public: 
    Game(std::string const & title, unsigned width, unsigned height);
    void start();

private:
    bool p1_winner{true}; 
    std::string name_p1; 
    std::string name_p2;
    sf::RenderWindow window;
    std::map<int, std::unique_ptr<State>> states;
    int current_state;
    bool running;
    void handle_events();
    void delay(sf::Clock & clock) const;

};

#endif