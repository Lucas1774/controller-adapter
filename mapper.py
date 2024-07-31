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
        "A": False,
        "B": False,
        "X": False,
        "Y": False,
        "L1": False,
        "R1": False,
        "SELECT": False,
        "START": False,
        "L3": False,
        "R3": False,
        "XBOX": False,
        "UP": False,
        "LEFT": False,
        "RIGHT": False,
        "DOWN": False,
        "L2": False,
        "R2": False,
        "ACTIVATE": False,
        "LEFT_JOYSTICK_LEFT": False,  # for non actually analogic joysticks
        "LEFT_JOYSTICK_RIGHT": False,
        "LEFT_JOYSTICK_UP": False,
        "LEFT_JOYSTICK_DOWN": False,
        "RIGHT_JOYSTICK_LEFT": False,
        "RIGHT_JOYSTICK_RIGHT": False,
        "RIGHT_JOYSTICK_UP": False,
        "RIGHT_JOYSTICK_DOWN": False,
    }

    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        keyboard = KeyboardController()
        mouse = MouseController()
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        screen_width, screen_height = pyautogui.size()

        if game == "swarm":
            swarm.run(
                button_state,
                config,
                screen_width,
                screen_height,
                joystick,
                keyboard,
                mouse,
            )
        else:
            print("Invalid game")
