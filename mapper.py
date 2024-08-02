import json
import sys

import pyautogui
import pygame
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

from swarm import swarm

if __name__ == "__main__":
    try:
        game = sys.argv[1]
    except IndexError:
        print("No game was specified")
        exit()

    button_state = {
        "A": "NOT_PRESSED",
        "B": "NOT_PRESSED",
        "X": "NOT_PRESSED",
        "Y": "NOT_PRESSED",
        "L1": "NOT_PRESSED",
        "R1": "NOT_PRESSED",
        "SELECT": "NOT_PRESSED",
        "START": "NOT_PRESSED",
        "L3": "NOT_PRESSED",
        "R3": "NOT_PRESSED",
        "XBOX": "NOT_PRESSED",
        "UP": "NOT_PRESSED",
        "LEFT": "NOT_PRESSED",
        "RIGHT": "NOT_PRESSED",
        "DOWN": "NOT_PRESSED",
        "L2": "NOT_PRESSED",
        "R2": "NOT_PRESSED",
        "ACTIVATE": "NOT_PRESSED",
        # for non actually analog sticks or to abstract digital input from those that are
        "LEFT_JS_LEFT": "NOT_PRESSED",
        "LEFT_JS_RIGHT": "NOT_PRESSED",
        "LEFT_JS_UP": "NOT_PRESSED",
        "LEFT_JS_DOWN": "NOT_PRESSED",
        "RIGHT_JS_LEFT": "NOT_PRESSED",
        "RIGHT_JS_RIGHT": "NOT_PRESSED",
        "RIGHT_JS_UP": "NOT_PRESSED",
        "RIGHT_JS_DOWN": "NOT_PRESSED",
    }

    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    screen_width, screen_height = pyautogui.size()
    keyboard = KeyboardController()
    mouse = MouseController()
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    try:
        joystick.get_axis(config.get("left_trigger_id"))
        has_triggers = True
    except (pygame.error, TypeError):
        has_triggers = False

    if game == "swarm":
        swarm.run(
            button_state,
            has_triggers,
            config,
            screen_width,
            screen_height,
            joystick,
            keyboard,
            mouse,
        )
    else:
        print("Invalid game")
