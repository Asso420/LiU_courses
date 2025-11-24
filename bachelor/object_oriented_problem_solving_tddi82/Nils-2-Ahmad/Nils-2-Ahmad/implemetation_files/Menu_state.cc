#include "../decleration_files/Menu_state.h"
#include <string>
#include <SFML/Graphics.hpp>
#include <locale>
#include <iostream>




Menu_State::Menu_State()
    : play{false}, 
	text_p1{"Player 1 :", font}, 
	text_p2{"Player 2 :", font}, 
	text_start{"Fill out players names", font},
	text_start2{"and press <Enter> to start", font},
	text_title{"BOMBERMAN", font}
{
}

void Menu_State::handle_event(sf::Event event, std::string & name_p1, std::string & name_p2)
{

	if(event.type == sf::Event::TextEntered)
	{
  		if(std::isprint(event.text.unicode))
		{
  			if(!first_name_done)
    			name_p1 += event.text.unicode;
  			else
    			name_p2 += event.text.unicode;
		}	   
	}
	else if (event.type == sf::Event::KeyPressed)
	{
        if (event.key.code == sf::Keyboard::Return && !name_p2.empty())
        {
            play = true;
			first_name_done = false;
        }
  		else if(event.key.code == sf::Keyboard::Return && !name_p1.empty())
		{
  			first_name_done = true;
			// text_p1.setStyle(sf::Text::Regular);
			// text_p2.setStyle(sf::Text::Underlined);

		}
  		else if(event.key.code == sf::Keyboard::BackSpace)
		{
  			if(!first_name_done)
    		{
      			if (!name_p1.empty())
					name_p1.pop_back();
    		}
  			else
    		{
      			if(!name_p2.empty())
					name_p2.pop_back();
    		}
		}
	}
}

void Menu_State::update ()
{
	text_title.setFillColor(sf::Color::Red);
	text_title.setStyle(sf::Text::Bold | sf::Text::Underlined);

	text_p1.setFillColor(sf::Color::Blue);
  	text_p2.setFillColor(sf::Color::Red);
	text_start.setFillColor(sf::Color::White);
	text_start2.setFillColor(sf::Color::White);
	if(!first_name_done)
	{
		text_p1.setStyle(sf::Text::Underlined);
		text_p2.setStyle(sf::Text::Regular);
	}
	else
	{
		text_p2.setStyle(sf::Text::Underlined);
		text_p1.setStyle(sf::Text::Regular);
		text_start.setFillColor(sf::Color::Green);
		text_start2.setFillColor(sf::Color::Green);
	}
}

void Menu_State::render (sf::RenderTarget & target, std::string & name_p1, std::string & name_p2, bool & winner)
{
	target.draw(background_sprite);
    text_p1.setPosition (sf::Vector2f(100, 170));
    text_p2.setPosition (text_p1.getPosition() + sf::Vector2f(0,100));

    auto tarsize{target.getSize()};
	auto size{text_start.getLocalBounds()};
	text_start.setOrigin((size.width / 2), (size.height / 2));
    text_start.setPosition((tarsize.x / 2), (tarsize.y / 2 + 100));

	size = text_start2.getGlobalBounds();
	text_start2.setOrigin((size.width / 2), (size.height / 2));
    text_start2.setPosition((tarsize.x / 2), (tarsize.y / 2 + 250));

	size = text_title.getGlobalBounds();
	text_title.setOrigin((size.width / 2), (size.height / 2));
	text_title.setPosition(tarsize.x / 2, 40);

	sf::Text output_name_p1{name_p1, font};
	output_name_p1.setPosition(text_p1.getPosition()+ sf::Vector2f(300, 0));
	sf::Text output_name_p2{name_p2, font};
	output_name_p2.setPosition(text_p2.getPosition()+sf::Vector2f(300, 0));

	target.draw(text_title);
	target.draw(text_p1);
	target.draw(text_p2);
	target.draw(text_start);
	target.draw(text_start2);
	target.draw(output_name_p1);
	target.draw(output_name_p2);
}




int Menu_State::get_next_state()
{
    if (play)
    {
        play = false;
        return GAME_STATE;
    }
    else
    {
        return MENU_STATE;
    }
}
