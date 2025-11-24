#ifndef Menu_state_h
#define Menu_state_h

#include "State.h"
#include "../implemetation_files/Manager.cc"

#include <string>
#include <SFML/Graphics.hpp>
#include <locale>



class Menu_State : public State
{

public:
  // Menu_State ();
  // virtual void handle_event (Event event) override;
  // virtual void update () override;
  // virtual void render (RenderTarget & target) override;
  // virtual int get_next_state () override;

  Menu_State ();
  void handle_event (sf::Event event, std::string & name_p1, std::string & name_p2) override;
  void update () override;
  void render (sf::RenderTarget & target, std::string & name_p1, std::string & name_p2, bool & winner) override;
  virtual int get_next_state ();



private:
  // std::string name_p1;
  // std::string name_p2;
  sf::Text text_title;
  sf::Text text_p1;
  sf::Text text_p2;
  sf::Text text_start;
  sf::Text text_start2;
  sf::Font font{Manager<sf::Font>::load("resources/ARCADE.TTF")};
  sf::Sprite background_sprite{Manager<sf::Texture>::load("resources/bg2.png")};
  bool first_name_done{false};
  bool play;
  


};





#endif //Menu_state_h