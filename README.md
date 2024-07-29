# Usage

Just double-click the .bat or .exe files. Use Windows' Game Controllers to map button ID to button in the `config.json` file. The program uses the next button to action map (I didn't want to make this configurable for such a small game, and it is possible to either edit the code or hack a solution through the button ID to button map. Mind that trigger buttons are considered analog sticks for most controllers though):

    START -> ESCAPE
    L1 -> E
    R1 -> R
    A -> LEFT CLICK
    X -> C
    Y -> O
    B -> TAB
The program is active (i.e. its logic is executed) by default. It is possible to map a button to toggle activation. When deactivated, it will just listen to an activation input.