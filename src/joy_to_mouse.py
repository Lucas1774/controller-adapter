import json
import time

import pyautogui
import pygame
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController


def press_then_release(key):
    keyboard.press(key)
    time.sleep(0.01)
    keyboard.release(key)


running = True
key_state = {"a": False, "d": False, "w": False, "s": False}

with open("config.json", "r") as config:
    config = json.load(config)
    button_mapping = {
        int(k) - 1: v
        for k, v in config.get(
            "button_mapping",
            {
                "1": "A",
                "2": "B",
                "3": "X",
                "4": "Y",
                "5": "L1",
                "6": "R1",
                "7": "SELECT",
                "8": "START",
                "9": "L3",
                "10": "R3",
                "11": "XBOX",
                "12": "ACTIVATE",
            },
        ).items()
    }
    LEFT_JOYSTICK_DEAD_ZONE = config.get("LEFT_JOYSTICK_DEAD_ZONE", 0.5)
    RIGHT_JOYSTICK_DEAD_ZONE = config.get("RIGHT_JOYSTICK_DEAD_ZONE", 0.2)
    SENSITIVITY = config.get("SENSITIVITY", 0.9)
    CROSS_SENSITIVITY = config.get("CROSS_SENSITIVITY", 0.5)
    del config

keyboard = KeyboardController()
mouse = MouseController()
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2

try:
    while True:
        pygame.event.pump()
        if not running:
            for event in pygame.event.get(eventtype=pygame.JOYBUTTONDOWN):
                button = button_mapping.get(event.button)
                if button == "ACTIVATE":
                    running = not running
                    break
        else:
            # left joystick
            left_x_axis = joystick.get_axis(0)
            left_y_axis = joystick.get_axis(1)
            new_key_state = {"a": False, "d": False, "w": False, "s": False}
            if abs(left_x_axis) > LEFT_JOYSTICK_DEAD_ZONE:
                if left_x_axis < 0:
                    new_key_state["a"] = True
                else:
                    new_key_state["d"] = True
            if abs(left_y_axis) > LEFT_JOYSTICK_DEAD_ZONE:
                if left_y_axis < 0:
                    new_key_state["w"] = True
                else:
                    new_key_state["s"] = True
            for key, is_pressed in new_key_state.items():
                if is_pressed and not key_state[key]:
                    keyboard.press(key)
                elif not is_pressed and key_state[key]:
                    keyboard.release(key)
            key_state.update(new_key_state)

            # right joystick
            right_x_axis = joystick.get_axis(2)
            right_y_axis = joystick.get_axis(3)
            if (
                abs(right_x_axis) > RIGHT_JOYSTICK_DEAD_ZONE
                or abs(right_y_axis) > RIGHT_JOYSTICK_DEAD_ZONE
            ):
                pyautogui.moveTo(
                    int((right_x_axis * center_x * SENSITIVITY) + center_x),
                    int((right_y_axis * center_y * SENSITIVITY) + center_y),
                )

            # buttons
            for event in pygame.event.get(eventtype=pygame.JOYBUTTONDOWN):
                button = button_mapping.get(event.button)
                if button == "ACTIVATE":
                    running = not running
                    break
                elif running:
                    if button == "START":
                        press_then_release(Key.esc)
                    elif button == "L1":
                        press_then_release("e")
                    elif button == "R1":
                        press_then_release("r")
                    elif button == "A":
                        mouse.click(Button.left)
                    elif button == "X":
                        press_then_release("c")
                    elif button == "Y":
                        press_then_release("o")
                    elif button == "B":
                        press_then_release(Key.tab)

            # cross
            for event in pygame.event.get(eventtype=pygame.JOYHATMOTION):
                if event.value[1] == -1:
                    pyautogui.moveTo(center_x, center_y)
                elif event.value[0] == 1:
                    pyautogui.moveTo(center_x + center_x * CROSS_SENSITIVITY, center_y)
                elif event.value[0] == -1:
                    pyautogui.moveTo(center_x - center_x * CROSS_SENSITIVITY, center_y)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
