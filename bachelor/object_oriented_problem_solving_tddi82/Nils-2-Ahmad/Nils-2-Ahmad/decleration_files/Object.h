#ifndef Object_h
#define Object_h

#include <SFML/Graphics.hpp>
#include <string>

class Object
{
public:
    Object(sf::Vector2f const &pos, sf::Texture &texture);
    ~Object() = default;
    static bool collision(Object const &ob1, Object const &ob2);
    virtual void handle_collision(Object &obj_2) = 0;
    sf::Sprite get_sprite() const;
    sf::Vector2f get_obj_pos() const;
    void not_existing();
    bool is_existing() const;
    void move(int const m_speed, char const direction);
protected:
    sf::Sprite sprite;
    bool existing;
    sf::Vector2f old_pos{};
};

class Moving_Object : public Object
{
public:
    Moving_Object(sf::Vector2f const &pos, sf::Texture &texture);
    //void move(int const m_speed, char const direction);
};

#endif
