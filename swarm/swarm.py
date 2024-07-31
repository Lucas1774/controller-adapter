import threading
import time

import pyautogui
import pygame
from pynput.keyboard import Key
from pynput.mouse import Button


KEY_MAPPING = {
    "esc": Key.esc,
    "tab": Key.tab,
}
high_precision = False
pyautogui.FAILSAFE = False
key_state = {"a": False, "d": False, "w": False, "s": False, "tab": False}


def run(
    button_state,
    config,
    screen_width,
    screen_height,
    joystick,
    keyboard,
    mouse,
):

    def press_then_release(key_to_tap):
        keyboard.press(KEY_MAPPING.get(key_to_tap, key_to_tap))
        time.sleep(0.01)
        keyboard.release(KEY_MAPPING.get(key_to_tap, key_to_tap))

    def handle_to_key_tap_input(input, key_to_tap):
        if button_state[input]:
            threading.Thread(target=press_then_release, args=(key_to_tap,)).start()
            button_state[input] = False

    def handle_to_key_hold_input(input, key_to_press):
        if button_state[input]:
            if not key_state[key_to_press]:
                keyboard.press(KEY_MAPPING.get(key_to_press, key_to_press))
                key_state[key_to_press] = True
        else:
            if key_state[key_to_press]:
                keyboard.release(KEY_MAPPING.get(key_to_press, key_to_press))
                key_state[key_to_press] = False

    def handle_to_mouse_absolute_move_input(input, x, y):
        if button_state[input]:
            pyautogui.moveTo(x, y)
            button_state[input] = False

    def handle_to_click_input(input, button_to_click):
        if button_state[input]:
            mouse.click(button_to_click)
            button_state[input] = False

    LEFT_JOYSTICK_X_ID = config.get("left_joystick_x_id")
    LEFT_JOYSTICK_Y_ID = config.get("left_joystick_y_id")
    RIGHT_JOYSTICK_X_ID = config.get("right_joystick_x_id")
    RIGHT_JOYSTICK_Y_ID = config.get("right_joystick_y_id")
    LEFT_TRIGGER_ID = config.get("left_trigger_id")
    LEFT_JOYSTICK_DEAD_ZONE = config.get("left_joystick_dead_zone")
    RIGHT_JOYSTICK_DEAD_ZONE = config.get("right_joystick_dead_zone")
    LEFT_TRIGGER_DEAD_ZONE = config.get("left_trigger_dead_zone")
    RIGHT_JOYSTICK_SENSITIVITY = config.get("right_joystick_sensitivity")
    BUTTON_MAPPING = {v - 1: k for k, v in config.get("button_mapping").items()}
    running = config.get("run_automatically")
    high_precision_always_on = config.get("high_precision_default")
    center_x = screen_width // 2
    center_y = screen_height // 2
    try:
        joystick.get_axis(LEFT_TRIGGER_ID)
        has_triggers = True
    except pygame.error:
        has_triggers = False

    INPUT_TO_KEY_TAP = {
        "START": "esc",
        "X": "c",
        "Y": "o",
        "L1": "e",
        "R1": "r",
    }

    INPUT_TO_KEY_HOLD = {
        "LEFT_JOYSTICK_LEFT": "a",
        "LEFT_JOYSTICK_RIGHT": "d",
        "LEFT_JOYSTICK_UP": "w",
        "LEFT_JOYSTICK_DOWN": "s",
        "B": "tab",
    }

    INPUT_TO_MOUSE_MOVE = {
        "LEFT": (720, center_y),
        "RIGHT": (1200, center_y),
        "UP": (center_x, center_y),
        "DOWN": (center_x, 825),
    }

    try:
        while True:
            pygame.event.pump()
            events = pygame.event.get()

            if not running:
                for event in events:
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = BUTTON_MAPPING.get(event.button)
                        if button == "ACTIVATE":
                            running = not running
                            break
            else:
                # state
                left_x_axis = joystick.get_axis(LEFT_JOYSTICK_X_ID)
                left_y_axis = joystick.get_axis(LEFT_JOYSTICK_Y_ID)
                is_x_axis_active = abs(left_x_axis) > LEFT_JOYSTICK_DEAD_ZONE
                is_y_axis_active = abs(left_y_axis) > LEFT_JOYSTICK_DEAD_ZONE
                button_state["LEFT_JOYSTICK_LEFT"] = (
                    is_x_axis_active and left_x_axis < LEFT_JOYSTICK_DEAD_ZONE
                )
                button_state["LEFT_JOYSTICK_RIGHT"] = (
                    is_x_axis_active and left_x_axis > LEFT_JOYSTICK_DEAD_ZONE
                )
                button_state["LEFT_JOYSTICK_UP"] = (
                    is_y_axis_active and left_y_axis < LEFT_JOYSTICK_DEAD_ZONE
                )
                button_state["LEFT_JOYSTICK_DOWN"] = (
                    is_y_axis_active and left_y_axis > LEFT_JOYSTICK_DEAD_ZONE
                )
                right_x_axis = joystick.get_axis(RIGHT_JOYSTICK_X_ID)
                right_y_axis = joystick.get_axis(RIGHT_JOYSTICK_Y_ID)

                for event in events:
                    if event.type == pygame.JOYBUTTONDOWN:
                        button_state[BUTTON_MAPPING.get(event.button)] = True
                    elif event.type == pygame.JOYBUTTONUP:
                        button_state[BUTTON_MAPPING.get(event.button)] = False
                    elif event.type == pygame.JOYHATMOTION:
                        button_state["LEFT"] = event.value[0] == -1
                        button_state["RIGHT"] = event.value[0] == 1
                        button_state["DOWN"] = event.value[1] == -1
                        button_state["UP"] = event.value[1] == 1

                if not high_precision_always_on:
                    if has_triggers:
                        high_precision = (
                            joystick.get_axis(LEFT_TRIGGER_ID) > LEFT_TRIGGER_DEAD_ZONE
                        )
                    else:
                        high_precision = button_state["L2"]
                if button_state["ACTIVATE"]:
                    running = False
                    button_state["ACTIVATE"] = False
                    continue
                if button_state["R3"]:
                    high_precision_always_on = not high_precision_always_on
                    pyautogui.moveTo(center_x, center_y)
                    button_state["R3"] = False

                # action
                for input, key_to_tap in INPUT_TO_KEY_TAP.items():
                    handle_to_key_tap_input(input, key_to_tap)
                for input, key_to_press in INPUT_TO_KEY_HOLD.items():
                    handle_to_key_hold_input(input, key_to_press)
                for input, (x, y) in INPUT_TO_MOUSE_MOVE.items():
                    handle_to_mouse_absolute_move_input(input, x, y)
                handle_to_click_input("A", Button.left)

                if (
                    abs(right_x_axis) > RIGHT_JOYSTICK_DEAD_ZONE
                    or abs(right_y_axis) > RIGHT_JOYSTICK_DEAD_ZONE
                ):
                    if high_precision_always_on or high_precision:
                        pyautogui.moveRel(
                            int(right_x_axis * RIGHT_JOYSTICK_SENSITIVITY * 100),
                            int(right_y_axis * RIGHT_JOYSTICK_SENSITIVITY * 100),
                        )
                    else:
                        pyautogui.moveTo(
                            int(
                                (right_x_axis * center_x * RIGHT_JOYSTICK_SENSITIVITY)
                                + center_x
                            ),
                            int(
                                (right_y_axis * center_y * RIGHT_JOYSTICK_SENSITIVITY)
                                + center_y
                            ),
                        )

            time.sleep(0.001)

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
