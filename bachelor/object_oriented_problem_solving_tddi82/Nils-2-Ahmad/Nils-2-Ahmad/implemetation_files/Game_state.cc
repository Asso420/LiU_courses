#include "../decleration_files/Game_state.h"
#include "../decleration_files/Object.h"
#include "../decleration_files/constants.h"

#include <fstream>
#include <SFML/Graphics.hpp>
#include <string>
#include <vector>
#include <iostream>
#include <typeinfo>
#include <memory>
#include <time.h>
#include <algorithm>
#include <utility>
#include <cmath>


std::vector<std::unique_ptr<Object>> Game_State::static_obj_init()
{

  std::ifstream ifs;
  ifs.open("resources/wall_position.txt");
  int x;
  int y;
  std::vector<std::unique_ptr<Object>> obj;
  while (ifs >> x >> y)
  {
    obj.push_back(std::make_unique<Wall>(sf::Vector2f(x, y)));
  }

  std::ifstream ifs2;
  ifs2.open("resources/barrel_position.txt");
  while (ifs2 >> x >> y)
  {
    obj.push_back(std::make_unique<Barrel>(sf::Vector2f(x, y)));
  }
  return obj;
}

std::vector<std::unique_ptr<Object>> Game_State::ability_spawner()
{
  std::vector<std::unique_ptr<Object>> tmp;
  srand((unsigned)time(NULL));

  tmp.push_back(std::make_unique<Give_Ghost_Ability>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Give_Kick_Bomb>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Give_Shield>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Inc_Move_Speed>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Inc_Bomb_Amount>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Inc_Life>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Give_Knife>(calc_rand_pos()));
  tmp.push_back(std::make_unique<Inc_Bomb_Size>(calc_rand_pos()));

  return tmp;
}

sf::Vector2f Game_State::calc_rand_pos()
{
  std::vector<Barrel *> tmp;
  for (auto &obj : Objects)
  {
    if (Barrel *b = dynamic_cast<Barrel *>(&(*obj)))
      tmp.push_back(b);
  }
  return sf::Vector2f(tmp.at(0 + (rand() % tmp.size()))->get_obj_pos());
}

Game_State::Game_State()


    : P1{sf::Vector2f(60, 60)}, P2{sf::Vector2f(1140, 60)},
      E1{sf::Vector2f(1140, 600)}, 
      E2{sf::Vector2f(60, 660)},

      Objects{static_obj_init()}

{
  enemy_move_clock.restart();

  std::vector<std::unique_ptr<Object>> inital_abilities{ability_spawner()};
  Objects.insert(Objects.end(), std::make_move_iterator(inital_abilities.begin()), std::make_move_iterator(inital_abilities.end()));
}




void Game_State::move_players(float dt)
{
  //======================= SPELARE 1 rörelse ========================
  if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::W) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::D))
  {
    P1.move(P1.get_move_speed(), 'E');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::W) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::A))
  {
    P1.move(P1.get_move_speed(), 'Q');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::A) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::S))
  {
    P1.move(P1.get_move_speed(), 'Z');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::S) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::D))
  {
    P1.move(P1.get_move_speed(), 'X');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::W))
  {
    P1.move(P1.get_move_speed(), 'U');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::S))
  {
    P1.move(P1.get_move_speed(), 'D');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::A))
  {
    P1.move(P1.get_move_speed(), 'L');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::D))
  {
    P1.move(P1.get_move_speed(), 'R');
  }
  //======================= SPELARE 2 rörelse ========================
  if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Up) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Right))
  {
    P2.move(P2.get_move_speed(), 'E');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Up) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Left))
  {
    P2.move(P2.get_move_speed(), 'Q');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Left) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Down))
  {
    P2.move(P2.get_move_speed(), 'Z');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Down) && sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Right))
  {
    P2.move(P2.get_move_speed(), 'X');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Up))
  {
    P2.move(P2.get_move_speed(), 'U');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Down))
  {
    P2.move(P2.get_move_speed(), 'D');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Left))
  {
    P2.move(P2.get_move_speed(), 'L');
  }
  else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Right))
  {
    P2.move(P2.get_move_speed(), 'R');
  }
  //======================= Enemy Movement  ========================

  sf::Vector2f p1 = P1.get_obj_pos();
  sf::Vector2f p2 = P2.get_obj_pos();
  sf::Vector2f epos = E1.get_sprite().getPosition();

  float dx1 = p1.x - epos.x, dy1 = p1.y - epos.y;
  float dx2 = p2.x - epos.x, dy2 = p2.y - epos.y;
  float dist1_sq = dx1*dx1 + dy1*dy1;
  float dist2_sq = dx2*dx2 + dy2*dy2;
  // pick the target
  sf::Vector2f target = (dist1_sq < dist2_sq) ? p1 : p2;

  // std::cout << "E1 at (" << epos.x << "," << epos.y << ")  "
  //         << "p1(" << p1.x << "," << p1.y << ")  "
  //         << "p2(" << p2.x << "," << p2.y << ")  "
  //         << "chasing " << ((dist1_sq < dist2_sq) ? "P1" : "P2")
  //         << std::endl;

  E1.update(target, dt);
  E2.update(dt);
}

void Game_State::all_collision()
{
  if (Object::collision(P1, P2))
  {
    P1.handle_collision(P2);
    P2.handle_collision(P1);
  }

  for (auto a{Objects.begin()}; a != Objects.end(); ++a)
  {
    if (Object::collision(*(*a), P1))
    {
      (*a)->handle_collision(P1);
      P1.handle_collision(*(*a));
    }

    if (Object::collision(*(*a), P2))
    {
      (*a)->handle_collision(P2);
      P2.handle_collision(*(*a));
    }
    if (Object::collision(*(*a), E1))
    {
      (*a)->handle_collision(E1);
      E1.handle_collision(*(*a));
    }

    if (Object::collision(*(*a), E2))
    {
      (*a)->handle_collision(E2);
      E2.handle_collision(*(*a));
    }

    for (auto b{a + 1}; b != Objects.end(); ++b)
    {
      if (Object::collision(*(*a), *(*b)))
      {
        (*a)->handle_collision(*(*b));
        (*b)->handle_collision(*(*a));
      }
    }
  }
}

void Game_State::place_bombs(sf::Event event)
{
  auto key{event.key};
  if (key.code == sf::Keyboard::Key::Space)
  {
    if (P1.get_bomb_amount() != 0 && P1.get_place_timer().getElapsedTime().asSeconds() >= 1)
    {
      P1.change_bomb_coll(false);
      P1.place_bomb(Objects, '1');
      P1.reset_place_clock();
    }
  }

  if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::P))
  {
    if (P2.get_bomb_amount() != 0 && P2.get_place_timer().getElapsedTime().asSeconds() >= 1)
    {
      P2.change_bomb_coll(false);
      P2.place_bomb(Objects, '2');
      P2.reset_place_clock();
    }
  }
}

void Game_State::explode(Bomb &b)
{
  sf::Vector2f bomb_position = b.get_sprite().getPosition();

  std::unique_ptr<Explossion> ex1(new Explossion{bomb_position, b.bomb_size});
  Objects.push_back(std::move(ex1));
  bool tmp2_w{false};
  bool tmp3_w{false};
  bool tmp4_w{false};
  bool tmp5_w{false};

  bool tmp2_b{false};
  bool tmp3_b{false};
  bool tmp4_b{false};
  bool tmp5_b{false};

  int one_time_b2{2};
  int one_time_b3{2};
  int one_time_b4{2};
  int one_time_b5{2};

  for (int i{}; i <= b.bomb_size; i++)
  {
    std::unique_ptr<Explossion> ex2(new Explossion{bomb_position + sf::Vector2f(60 * i, 0), b.bomb_size});
    std::unique_ptr<Explossion> ex3(new Explossion{bomb_position + sf::Vector2f(0, 60 * i), b.bomb_size});
    std::unique_ptr<Explossion> ex4(new Explossion{bomb_position + sf::Vector2f(-60 * i, 0), b.bomb_size});
    std::unique_ptr<Explossion> ex5(new Explossion{bomb_position + sf::Vector2f(0, -60 * i), b.bomb_size});

    for (auto obj{Objects.begin()}; obj != Objects.end(); ++obj)
    {
      /*WALL*/
      if (dynamic_cast<Wall *>(obj->get()) != nullptr)
      {
        if (Object::collision(*(*obj), *ex2))
        {
          tmp2_w = true;
        }
        if (Object::collision(*(*obj), *ex3))
        {
          tmp3_w = true;
        }
        if (Object::collision(*(*obj), *ex4))
        {
          tmp4_w = true;
        }
        if (Object::collision(*(*obj), *ex5))
        {
          tmp5_w = true;
        }
      }
      /*BARRELS*/
      if (dynamic_cast<Barrel *>(obj->get()) != nullptr)
      {
        if (Object::collision(*(*obj), *ex2))
        {
          tmp2_b = true;
          one_time_b2--;
        }
        if (Object::collision(*(*obj), *ex3))
        {
          tmp3_b = true;
          one_time_b3--;
        }
        if (Object::collision(*(*obj), *ex4))
        {
          tmp4_b = true;
          one_time_b4--;
        }
        if (Object::collision(*(*obj), *ex5))
        {
          tmp5_b = true;
          one_time_b5--;
        }
      }
    }

    if (!tmp2_w && one_time_b2 >= 1)
    {
      Objects.push_back(std::move(ex2));
      if (tmp2_b)
      {
        one_time_b2--;
      }
    }
    if (!tmp3_w && one_time_b3 >= 1)
    {
      Objects.push_back(std::move(ex3));
      if (tmp3_b)
      {
        one_time_b3--;
      }
    }
    if (!tmp4_w && one_time_b4 >= 1)
    {
      Objects.push_back(std::move(ex4));
      if (tmp4_b)
      {
        one_time_b4--;
      }
    }
    if (!tmp5_w && one_time_b5 >= 1)
    {
      Objects.push_back(std::move(ex5));
      if (tmp5_b)
      {
        one_time_b5--;
      }
    }
  }

  if (b.Player1)
  {
    P1.inc_bomb_amount();
  }
  else
  {
    P2.inc_bomb_amount();
  }
}

void Game_State::explode_and_remove()
{

  for (auto obj{Objects.begin()}; obj != Objects.end(); ++obj)
  {
    if (auto bomb = dynamic_cast<Bomb *>(obj->get()))
    {
      if (bomb->time.getElapsedTime().asSeconds() >= 3 || bomb->check_explode())
      {
        explode(*bomb);
        (*obj)->not_existing();
      }
    }

    if (auto explo = dynamic_cast<Explossion *>(obj->get()))
    {
      if (explo->time.getElapsedTime().asSeconds() >= 1)
      {
        (*obj)->not_existing();
      }
    }
  }
}

void Game_State::check_winners()
{
  if (P1.get_life_amount() <= 0)
  {
    end_game = true;
    winner_id = '2';
  }
  else if (P2.get_life_amount() <= 0)
  {
    winner_id = '1';
    end_game = true;
  }
}

void Game_State::move_bombs()
{
  for (auto &obj : Objects)
  {
    if (auto b = dynamic_cast<Bomb *>(obj.get()))
    {
      if (b->is_moving)
      {
        obj->move(4, b->get_direction());
      }
    }
  }
}

void Game_State::is_stuck()
{

  std::partition(Objects.begin(), Objects.end(),
                 [](auto const &obj)
                 { return dynamic_cast<Barrel *>(obj.get()) == nullptr; });

  bool out_of_barrelP1{true};
  bool out_of_barrelP2{true};
  bool out_of_bombP1{true};
  bool out_of_bombP2{true};
  for (auto obj{Objects.begin()}; obj != Objects.end(); obj++)
  {
    /*Barrels*/
    if (dynamic_cast<Barrel *>(obj->get()) != nullptr)
    {
      if (Object::collision((*(*obj)), P1))
      {
        out_of_barrelP1 = false;
      }
      if (out_of_barrelP1 && P1.get_ghost_timer().getElapsedTime().asSeconds() >= 7.0 && obj == Objects.end() - 1)
      {
        P1.change_barrel_coll(true);
      }
      if (Object::collision((*(*obj)), P2))
      {
        out_of_barrelP2 = false;
      }
      if (out_of_barrelP2 && P2.get_ghost_timer().getElapsedTime().asSeconds() >= 7.0 && obj == Objects.end() - 1 /*&& it == v_barrels.end() - 1*/)
      {
        P2.change_barrel_coll(true);
      }
    }

    /*Bombs*/
    if (dynamic_cast<Bomb *>(obj->get()) != nullptr)
    {
      if (Object::collision((*(*obj)), P1))
      {
        out_of_bombP1 = false;
      }
      if (Object::collision((*(*obj)), P2))
      {
        out_of_bombP2 = false;
      }
    }
  }

  if (out_of_bombP1)
  {
    P1.change_bomb_coll(true);
  }
  if (out_of_bombP2)
  {
    P2.change_bomb_coll(true);
  }
}

void Game_State::pop_nonexisting()
{
  for (auto &&it{Objects.begin()}; it != Objects.end();)
  {
    if (!(*it)->is_existing())
    {

      it = Objects.erase(it);
    }
    else
    {
      it++;
    }
  }
}

void Game_State::update()
{
  float dt = enemy_move_clock.restart().asSeconds();
  if (dt > 0.1f) dt = 0.1f;
  move_players(dt);
  //move_players();
  move_bombs();
  explode_and_remove();
  pop_nonexisting();
  is_stuck();
  int barrel_amount{};
  for (auto &obj : Objects)
  {
    if (dynamic_cast<Barrel *>(obj.get()) != nullptr)
      ++barrel_amount;
  }

  if (ability_spawn_time.getElapsedTime().asSeconds() >= 20 && barrel_amount != 0)
  {
    std::vector<std::unique_ptr<Object>> tmptmp{ability_spawner()};

    Objects.insert(Objects.end(), std::make_move_iterator(tmptmp.begin()), std::make_move_iterator(tmptmp.end()));
    ability_spawn_time.restart();
  }

  /*-----------------*/

  all_collision();
  check_winners();

  P1.check_if_invincible();
  P2.check_if_invincible();
}

void Game_State::handle_event(sf::Event event, std::string &name_p1, std::string &name_p2)
{
  place_bombs(event);
}

void Game_State::render(sf::RenderTarget &target, std::string &name_p1, std::string &name_p2, bool &winner)
{

  /*Draw background*/
  target.draw(background_sprite);

  /*---------------*/
  /*Draw players, bombs and explosions*/

  for (auto &obj : Objects)
  {
    target.draw(obj->get_sprite());
  }

  target.draw(P1.get_sprite());
  target.draw(P2.get_sprite());
  target.draw(E1.get_sprite());
  target.draw(E2.get_sprite());
  
  // std::cout << "E1 spawn at: "
  //         << E1.get_sprite().getPosition().x << ","
  //         << E1.get_sprite().getPosition().y << "\n";

  if (winner_id == '2')
  {
    winner = false;
  }
  else if (winner_id == '1')
  {
    winner = true;
  }

  /*UI TEST(Life, bombamount osv..)*/
  /*Player names*/
  sf::Text output_name_p1{name_p1, font};
  output_name_p1.setPosition(130, 705);
  output_name_p1.setFillColor(sf::Color::Blue);
  sf::Text output_name_p2{name_p2, font};
  sf::FloatRect rightbounds = output_name_p2.getLocalBounds();
  output_name_p2.setPosition(1070 - rightbounds.width, 705);
  output_name_p2.setFillColor(sf::Color::Red);

  target.draw(output_name_p1);
  target.draw(output_name_p2);
  /*------------*/

  /*Bomb_amount sprite and text*/

  bomb_amount_sprite.setScale(0.12, 0.12);
  bomb_amount_sprite.setPosition(sf::Vector2f(50, 685));
  target.draw(bomb_amount_sprite);
  bomb_amount_sprite.setPosition(sf::Vector2f(1100, 685));
  target.draw(bomb_amount_sprite);

  sf::Text p1_bombs{static_cast<char>(P1.get_bomb_amount() + 48), font};
  p1_bombs.setCharacterSize(20);
  p1_bombs.setPosition(sf::Vector2f(64, 710));
  sf::Text p2_bombs{static_cast<char>(P2.get_bomb_amount() + 48), font};
  p2_bombs.setCharacterSize(20);
  p2_bombs.setPosition(sf::Vector2f(1114, 710));

  target.draw(p1_bombs);
  target.draw(p2_bombs);
  /*---------------------------*/

  /*Life_amount sprite and text*/
  life_sprite.setScale(0.13, 0.13);
  life_sprite.setPosition(sf::Vector2f(-5, 690));
  target.draw(life_sprite);
  life_sprite.setPosition(sf::Vector2f(1140, 690));
  target.draw(life_sprite);

  sf::Text p1_life{static_cast<char>(P1.get_life_amount() + 48), font};

  p1_life.setCharacterSize(20);
  p1_life.setPosition(sf::Vector2f(18, 710));
  sf::Text p2_life{static_cast<char>(P2.get_life_amount() + 48), font};
  p2_life.setCharacterSize(20);
  p2_life.setPosition(sf::Vector2f(1163, 710));

  target.draw(p1_life);
  target.draw(p2_life);
  /*---------------------------*/

  if (P1.check_shield())
  {
    shield_ui.setPosition(P1.get_obj_pos().x - 50, P1.get_obj_pos().y - 50);
    shield_ui.setScale(0.04, 0.04);
    target.draw(shield_ui);
  }
  if (P2.check_shield())
  {
    shield_ui.setPosition(P2.get_obj_pos().x - 50, P2.get_obj_pos().y - 50);
    shield_ui.setScale(0.04, 0.04);
    target.draw(shield_ui);
  }
  if (!P1.check_if_barrel_coll())
  {
    ghost_ui.setPosition(P1.get_obj_pos().x - 25, P1.get_obj_pos().y - 50);
    ghost_ui.setScale(0.04, 0.04);
    target.draw(ghost_ui);
  }
  if (!P2.check_if_barrel_coll())
  {
    ghost_ui.setPosition(P2.get_obj_pos().x - 25, P2.get_obj_pos().y - 50);
    ghost_ui.setScale(0.04, 0.04);
    target.draw(ghost_ui);
  }

  if (P1.pick_knife())
  {
    knife_ui.setPosition(P1.get_obj_pos().x - 35, P1.get_obj_pos().y - 50);
    knife_ui.setScale(0.04, 0.04);
    target.draw(knife_ui);
  }

  if (P2.pick_knife())
  {
    knife_ui.setPosition(P2.get_obj_pos().x - 35, P2.get_obj_pos().y - 50);
    knife_ui.setScale(0.04, 0.04);
    target.draw(knife_ui);
  }

  if (P1.check_kick())
  {
    kick_ui.setPosition(P1.get_obj_pos().x - 5, P1.get_obj_pos().y - 50);
    kick_ui.setScale(0.02, 0.02);
    target.draw(kick_ui);
  }

  if (P2.check_kick())
  {
    kick_ui.setPosition(P2.get_obj_pos().x - 5, P2.get_obj_pos().y - 50);
    kick_ui.setScale(0.02, 0.02);
    target.draw(kick_ui);
  }
}

int Game_State ::get_next_state()
{
  if (end_game)
  {
    *this = Game_State();
    end_game = false;
    return END_STATE;
  }

  return GAME_STATE;
}
