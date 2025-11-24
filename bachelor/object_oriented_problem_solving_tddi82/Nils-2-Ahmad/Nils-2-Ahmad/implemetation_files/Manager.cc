#ifndef MANAGER
#define MANAGER
#include <map>
#include <string>
#include <exception>
#include <SFML/Graphics.hpp>

template<typename T>
T load_from_file(std::string const& file)
{
    T loaded_file{};
    if(!loaded_file.loadFromFile(file))
    {
        throw std::runtime_error("missing file in this directory");
    }
    return loaded_file;
}

template<typename T>
class Manager
{

    static std::map<std::string, T> resources;
public:
    static T& load(std::string const& file)
    {
        auto it = resources.find(file);
        if(it == resources.end())
        {
            T res {load_from_file<T>(file)};
                it = resources.emplace(make_pair(file, res)).first;
        }
        return it->second;
    }
};

template<typename T>
std::map<std::string, T> Manager<T>::resources;


#endif