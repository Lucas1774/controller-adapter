# Usage

Just double-click the .bat file. Use Windows' Game Controllers to map button ID to button in the `config.json` file.  
In some controllers, the pad inputs are handled differently, and don't need id mapping. In others, they are regular buttons. The program will correctly handle either. Back triggers are similar in this aspect, and can be either buttons or analog axis.
It is possible to configure whether the program is activated on boot or not, as well as it is to map a button to toggle activation. When deactivated, it will just listen to an activation input.

## Swarm

The program uses the next button to action map (I didn't want to make this configurable for such a small game, and it is possible to either edit the code or hack a solution through the button ID to button map. Mind that trigger buttons are considered analog sticks for most controllers though):

    START -> ESCAPE
    L1 -> E
    R1 -> R
    A -> LEFT CLICK
    X -> C
    Y -> O
    B (hold) -> TAB
    R3 -> toggle high precision mode (e.g for Jinx rocket)
    L2 (hold) -> high precision mode
    LEFT JOYSTICK (hold) -> WASD
    RIGHT JOYSTICK (hold) -> moves the camera
    UP, DOWN, LEFT, RIGHT -> moves the mouse to pick a card or reroll