import time

import pyautogui
import pygame
from pynput.keyboard import Key
from pynput.mouse import Button


def press_then_release(keyboard, key):
    keyboard.press(key)
    time.sleep(0.01)
    keyboard.release(key)


def run(
    config,
    screen_width,
    screen_height,
    joystick,
    keyboard,
    mouse,
):
    key_state = {"a": False, "d": False, "w": False, "s": False}
    center_x = screen_width // 2
    center_y = screen_height // 2
    running = config.get("run_automatically")
    BUTTON_MAPPING = {v - 1: k for k, v in config.get("button_mapping").items()}
    LEFT_JOYSTICK_X_ID = config.get("left_joystick_x_id")
    LEFT_JOYSTICK_Y_ID = config.get("left_joystick_y_id")
    RIGHT_JOYSTICK_X_ID = config.get("right_joystick_x_id")
    RIGHT_JOYSTICK_Y_ID = config.get("right_joystick_y_id")
    LEFT_JOYSTICK_DEAD_ZONE = config.get("left_joystick_dead_zone")
    RIGHT_JOYSTICK_DEAD_ZONE = config.get("right_joystick_dead_zone")
    LEFT_JOYSTICK_SENSITIVITY = config.get("left_joystick_sensitivity")
    RIGHT_JOYSTICK_SENSITIVITY = config.get("right_joystick_sensitivity")
    CROSS_SENSITIVITY = config.get("cross_sensitivity")
    pyautogui.FAILSAFE = not (RIGHT_JOYSTICK_SENSITIVITY == 1 or CROSS_SENSITIVITY == 1)

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
                # left joystick
                left_x_axis = joystick.get_axis(LEFT_JOYSTICK_X_ID)
                left_y_axis = joystick.get_axis(LEFT_JOYSTICK_Y_ID)
                new_key_state = {"a": False, "d": False, "w": False, "s": False}
                if abs(left_x_axis) > LEFT_JOYSTICK_DEAD_ZONE:
                    new_key_state["a"] = left_x_axis < 0
                    new_key_state["d"] = left_x_axis > 0
                if abs(left_y_axis) > LEFT_JOYSTICK_DEAD_ZONE:
                    new_key_state["w"] = left_y_axis < 0
                    new_key_state["s"] = left_y_axis > 0
                for key, is_pressed in new_key_state.items():
                    if is_pressed and not key_state[key]:
                        keyboard.press(key)
                    elif not is_pressed and key_state[key]:
                        keyboard.release(key)
                key_state.update(new_key_state)

                # right joystick
                right_x_axis = joystick.get_axis(RIGHT_JOYSTICK_X_ID)
                right_y_axis = joystick.get_axis(RIGHT_JOYSTICK_Y_ID)
                if (
                    abs(right_x_axis) > RIGHT_JOYSTICK_DEAD_ZONE
                    or abs(right_y_axis) > RIGHT_JOYSTICK_DEAD_ZONE
                ):
                    pyautogui.moveTo(
                        int(
                            (right_x_axis * center_x * LEFT_JOYSTICK_SENSITIVITY)
                            + center_x
                        ),
                        int(
                            (right_y_axis * center_y * LEFT_JOYSTICK_SENSITIVITY)
                            + center_y
                        ),
                    )

                for event in events:  # buttons
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = BUTTON_MAPPING.get(event.button)
                        if button == "ACTIVATE":
                            running = not running
                            break
                        elif running:
                            if button == "START":
                                press_then_release(keyboard, Key.esc)
                            elif button == "L1":
                                press_then_release(keyboard, "e")
                            elif button == "R1":
                                press_then_release(keyboard, "r")
                            elif button == "A":
                                mouse.click(Button.left)
                            elif button == "X":
                                press_then_release(keyboard, "c")
                            elif button == "Y":
                                press_then_release(keyboard, "o")
                            elif button == "B":
                                press_then_release(keyboard, Key.tab)
                            elif button == "DOWN":
                                pyautogui.moveTo(center_x, center_y)
                            elif button == "RIGHT":
                                pyautogui.moveTo(
                                    center_x + center_x * CROSS_SENSITIVITY,
                                    center_y,
                                )
                            elif button == "LEFT":
                                pyautogui.moveTo(
                                    center_x - center_x * CROSS_SENSITIVITY,
                                    center_y,
                                )

                    elif event.type == pygame.JOYHATMOTION:  # cross
                        if event.value[1] == -1:
                            pyautogui.moveTo(center_x, center_y)
                        elif event.value[0] == 1:
                            pyautogui.moveTo(
                                center_x + center_x * CROSS_SENSITIVITY, center_y
                            )
                        elif event.value[0] == -1:
                            pyautogui.moveTo(
                                center_x - center_x * CROSS_SENSITIVITY, center_y
                            )

            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
