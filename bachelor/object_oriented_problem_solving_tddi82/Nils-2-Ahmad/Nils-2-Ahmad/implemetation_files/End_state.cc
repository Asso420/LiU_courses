#include "../decleration_files/End_state.h"

#include <string>
#include <SFML/Graphics.hpp>
#include <locale>
#include <iostream>

End_State::End_State()
    : menu{false}, text_ending{"", font}, text_ending2{"Press <ENTER> to return to Menu", font}

{
    text_ending.setStyle(sf::Text::Bold);
    text_ending.setFillColor(sf::Color::Blue);
    text_ending2.setStyle(sf::Text::Bold);
    text_ending2.setFillColor(sf::Color::Red);
}

void End_State::handle_event(sf::Event event, std::string &name_p1, std::string &name_p2)
{

    if (event.type == sf::Event::KeyPressed)
    {
        if (event.key.code == sf::Keyboard::Return)
        {   
            name_p1.clear();
            name_p2.clear();
            menu = true;
        }
    }
}

void End_State::update()
{
}

void End_State::render(sf::RenderTarget &target, std::string &name_p1, std::string &name_p2, bool &winner)
{
    if (winner)
    {
        text_ending.setString(name_p1 + " WON!");
    }
    else
    {
        text_ending.setString(name_p2 + " WON!");
    }

    auto size{text_ending.getGlobalBounds()};
    auto tarsize{target.getSize()};
    text_ending.setOrigin((size.width / 2), (size.height / 2));
    text_ending.setPosition((tarsize.x / 2), (tarsize.y / 2 - 75));
    auto size2{text_ending2.getGlobalBounds()};
    text_ending2.setOrigin((size2.width / 2), (size2.height / 2));
    text_ending2.setPosition((tarsize.x / 2), (tarsize.y / 2 + 75));

    target.draw(text_ending);
    target.draw(text_ending2);
}

int End_State::get_next_state()
{
    if (menu)
    {
        menu = false;
        return MENU_STATE;
    }
    else
    {
        return END_STATE;
    }
}
