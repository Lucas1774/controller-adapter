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
        swarm.run(config, screen_width, screen_height, joystick, keyboard, mouse)
    else:
        print("Invalid game")
