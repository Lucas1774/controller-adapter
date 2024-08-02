import json
import time

import pygame
from pynput.mouse import Button

from util.functions import Functions


def run(
    button_state,
    has_triggers,
    config,
    screen_width,
    screen_height,
    joystick,
    keyboard,
    mouse,
):

    def toggle_high_precision():
        nonlocal high_precision
        high_precision = not high_precision

    LEFT_JOYSTICK_X_ID = config.get("left_joystick_x_id")
    LEFT_JOYSTICK_Y_ID = config.get("left_joystick_y_id")
    RIGHT_JOYSTICK_X_ID = config.get("right_joystick_x_id")
    RIGHT_JOYSTICK_Y_ID = config.get("right_joystick_y_id")
    LEFT_TRIGGER_ID = config.get("left_trigger_id")
    RIGHT_TRIGGER_ID = config.get("right_trigger_id")
    LEFT_JOYSTICK_DEAD_ZONE = config.get("left_joystick_dead_zone")
    RIGHT_JOYSTICK_DEAD_ZONE = config.get("right_joystick_dead_zone")
    LEFT_TRIGGER_DEAD_ZONE = config.get("left_trigger_dead_zone")
    RIGHT_TRIGGER_DEAD_ZONE = config.get("right_trigger_dead_zone")
    RIGHT_JOYSTICK_SENSITIVITY = config.get("right_joystick_sensitivity")
    BUTTON_MAPPING = {v - 1: k for k, v in config.get("button_mapping").items()}
    running = config.get("run_automatically")
    with open("swarm/config.json", "r") as config_file:
        config = json.load(config_file)
        high_precision = config.get("high_precision_on_by_default")
        MAX_RADIUS_HIGH_PRECISION_OFF = config.get("default_radius")
        current_radius = MAX_RADIUS_HIGH_PRECISION_OFF
    key_state = {
        "a": False,
        "d": False,
        "w": False,
        "s": False,
        "tab": False,
        "t": False,
    }
    center_x = screen_width // 2
    center_y = screen_height // 2

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
        "L3": "t",
    }

    INPUT_TO_MOUSE_MOVE = {
        "LEFT": (720, center_y),
        "RIGHT": (1200, center_y),
        "UP": (center_x, center_y),
        "DOWN": (center_x, 825),
        "R3": (center_x, center_y),
    }

    INPUT_TO_LOGIC_BEFORE = {
        "L3": lambda: functions.move_mouse(mouse, center_x, center_y),
        "R3": toggle_high_precision,
    }

    functions = Functions(keyboard, mouse, INPUT_TO_LOGIC_BEFORE)

    try:
        last_update_time = time.perf_counter()
        while True:
            loop_start_time = time.perf_counter()
            pygame.event.pump()
            events = pygame.event.get()

            if not running:
                for event in events:
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = BUTTON_MAPPING.get(event.button)
                        if button == "ACTIVATE":
                            running = True
                            break
            else:
                # state
                left_x_axis = joystick.get_axis(LEFT_JOYSTICK_X_ID)
                left_y_axis = joystick.get_axis(LEFT_JOYSTICK_Y_ID)
                is_left_x_axis_active = abs(left_x_axis) > LEFT_JOYSTICK_DEAD_ZONE
                is_left_y_axis_active = abs(left_y_axis) > LEFT_JOYSTICK_DEAD_ZONE
                button_state["LEFT_JOYSTICK_LEFT"] = is_left_x_axis_active and left_x_axis < 0
                button_state["LEFT_JOYSTICK_RIGHT"] = is_left_x_axis_active and left_x_axis > 0
                button_state["LEFT_JOYSTICK_UP"] = is_left_y_axis_active and left_y_axis < 0
                button_state["LEFT_JOYSTICK_DOWN"] = is_left_y_axis_active and left_y_axis > 0
                right_x_axis = joystick.get_axis(RIGHT_JOYSTICK_X_ID)
                right_y_axis = joystick.get_axis(RIGHT_JOYSTICK_Y_ID)
                is_right_x_axis_active = abs(right_x_axis) > RIGHT_JOYSTICK_DEAD_ZONE
                is_right_y_axis_active = abs(right_y_axis) > RIGHT_JOYSTICK_DEAD_ZONE

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

                if has_triggers:
                    button_state["R2"] = joystick.get_axis(RIGHT_TRIGGER_ID) > RIGHT_TRIGGER_DEAD_ZONE
                    button_state["L2"] = joystick.get_axis(LEFT_TRIGGER_ID) > LEFT_TRIGGER_DEAD_ZONE
                if high_precision or button_state["R2"] and button_state["L2"]:
                    button_state["R2"] = False
                    button_state["L2"] = False
                if button_state["R2"]:
                    if current_radius < 1:
                        current_radius += RIGHT_JOYSTICK_SENSITIVITY * 0.001
                elif button_state["L2"]:
                    if current_radius > 0.2:
                        current_radius -= RIGHT_JOYSTICK_SENSITIVITY * 0.001
                else:
                    current_radius = MAX_RADIUS_HIGH_PRECISION_OFF

                if button_state["ACTIVATE"]:
                    running = False
                    button_state["ACTIVATE"] = False
                    continue

                # action
                for input, key_to_tap in INPUT_TO_KEY_TAP.items():
                    functions.handle_to_key_tap_input(button_state, input, key_to_tap)
                for input, key_to_press in INPUT_TO_KEY_HOLD.items():
                    functions.handle_to_key_hold_input(button_state, key_state, input, key_to_press)
                for input, (x, y) in INPUT_TO_MOUSE_MOVE.items():
                    functions.handle_to_mouse_absolute_move_input(button_state, input, x, y)
                functions.handle_to_click_input(button_state, "A", Button.left)

                if is_right_x_axis_active or is_right_y_axis_active:
                    if high_precision:
                        if time.perf_counter() - last_update_time > 0.1:
                            functions.move_mouse_relative(
                                mouse,
                                round(right_x_axis * RIGHT_JOYSTICK_SENSITIVITY * 100),
                                round(right_y_axis * RIGHT_JOYSTICK_SENSITIVITY * 100),
                            )
                            last_update_time = time.perf_counter()
                    else:
                        functions.move_mouse(
                            mouse,
                            round((right_x_axis * center_x * current_radius) + center_x),
                            round((right_y_axis * center_y * current_radius) + center_y),
                        )

            time.sleep(max(0.001 - (time.perf_counter() - loop_start_time), 0))

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
