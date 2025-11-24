#include "../decleration_files/Game.h"
#include "../decleration_files/constants.h"

/*
 * If you want to study the code, it is recommended that
 * you start looking in Game.h.
 */

int main ()
{
    // We only want the main function to start the Game and then run it
    Game g { "Bomberman", screen_width, screen_height };
    g.start();
    return 0;
}
