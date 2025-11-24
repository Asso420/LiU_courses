#ifndef End_state_h
#define End_state_h
#include "../implemetation_files/Manager.cc"
#include <string>
#include <SFML/Graphics.hpp>
#include <locale>
#include "State.h"


class End_State : public State
{

public:


  End_State ();
  void handle_event (sf::Event event, std::string & name_p1, std::string & name_p2) override;
  void update () override;
  void render (sf::RenderTarget & target, std::string & name_p1, std::string & name_p2, bool & winner) override;
  virtual int get_next_state ();



private:
  sf::Text text_ending;
  sf::Text text_ending2;
  bool menu;
  sf::Font font{Manager<sf::Font>::load("resources/ARCADE.TTF")};
 
};





#endif //End_state_h