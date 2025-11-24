#include "../decleration_files/Game.h"
#include "../decleration_files/Menu_state.h"
#include "../decleration_files/Game_state.h"
#include "../decleration_files/End_state.h"

Game ::Game(std::string const &title,
            unsigned width,
            unsigned height)
    : window{sf::VideoMode{width, height},
             title, sf::Style::Titlebar | sf::Style::Close},
      current_state{MENU_STATE},
      running{true}
{

    states.insert(std::pair<int,
                            std::unique_ptr<State>>({MENU_STATE,
                                                     std::make_unique<Menu_State>()}));

    states.insert(std::pair<int,
                            std::unique_ptr<State>>({GAME_STATE,
                                                     std::make_unique<Game_State>()}));

    states.insert(std::pair<int,
                            std::unique_ptr<State>>({END_STATE,
                                                     std::make_unique<End_State>()}));
}

void Game ::start()
{

    sf::Clock clock{};
    while (running)
    {
        handle_events();
        states.at(current_state) -> update();
        window.clear ();
        states.at(current_state) -> render(window, name_p1, name_p2, p1_winner);
        window.display ();
        current_state = states.at(current_state) -> get_next_state();
        delay (clock);
    }
}

void Game ::handle_events()
{
    sf::Event event;
    while (window.pollEvent(event))
    {
        if (event.type == sf::Event::Closed)
            running = false;

        states.at(current_state)->handle_event(event, name_p1, name_p2);
    }
}

void Game ::delay(sf::Clock &clock) const
{
    sf::sleep(sf::milliseconds(1000.0 / fps) - clock.getElapsedTime());
    clock.restart();
}
