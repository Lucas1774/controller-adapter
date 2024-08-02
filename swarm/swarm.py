import json
import time

import pygame
from pynput.mouse import Button

from util.functions import Functions

PRESSED = {"PRESSED", "JUST_PRESSED"}
NOT_PRESSED = {"NOT_PRESSED", "JUST_RELEASED"}


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

    def toggle_high_precision_always_on():
        nonlocal high_precision_always_on
        high_precision_always_on = not high_precision_always_on

    def reset_radius():
        nonlocal current_radius
        current_radius = MAX_RADIUS_HIGH_PRECISION_OFF

    def handle_state(state, is_pressed):
        if is_pressed:
            if state == "NOT_PRESSED":
                state = "JUST_PRESSED"
        else:
            if state == "PRESSED":
                state = "JUST_RELEASED"
        return state

    LEFT_JS_X_ID = config.get("left_joystick_x_id")
    LEFT_JS_Y_ID = config.get("left_joystick_y_id")
    RIGHT_JS_X_ID = config.get("right_joystick_x_id")
    RIGHT_JS_Y_ID = config.get("right_joystick_y_id")
    LEFT_TRIGGER_ID = config.get("left_trigger_id")
    RIGHT_TRIGGER_ID = config.get("right_trigger_id")
    LEFT_JS_DEAD_ZONE = config.get("left_joystick_dead_zone")
    RIGHT_JS_DEAD_ZONE = config.get("right_joystick_dead_zone")
    RIGHT_TRIGGER_DEAD_ZONE = config.get("right_trigger_dead_zone")
    LEFT_TRIGGER_DEAD_ZONE = config.get("left_trigger_dead_zone")
    RIGHT_JS_SENSITIVITY = config.get("right_joystick_sensitivity")
    BUTTON_MAPPING = {v - 1: k for k, v in config.get("button_mapping").items()}
    running = config.get("run_automatically")
    with open("swarm/config.json", "r") as config_file:
        config = json.load(config_file)
        high_precision_always_on = config.get("high_precision_on_by_default")
        MAX_RADIUS_HIGH_PRECISION_OFF = config.get("default_radius")
        current_radius = MAX_RADIUS_HIGH_PRECISION_OFF
    center_x = screen_width // 2
    center_y = screen_height // 2

    INPUT_TO_KEY_TAP = {
        "START": "esc",
        "X": "c",
        "Y": "o",
    }

    INPUT_TO_KEY_HOLD = {
        "LEFT_JS_LEFT": "a",
        "LEFT_JS_RIGHT": "d",
        "LEFT_JS_UP": "w",
        "LEFT_JS_DOWN": "s",
        "B": "tab",
        "R2": "t",
    }

    INPUT_TO_MOUSE_MOVE = {
        "LEFT": (720, center_y),
        "RIGHT": (1200, center_y),
        "UP": (center_x, center_y),
        "DOWN": (center_x, 825),
        "R3": (center_x, center_y),
    }

    RELEASE_TO_KEY_TAP = {
        "R1": "r",
        "L1": "e",
    }

    INPUT_TO_LOGIC_BEFORE = {
        "R2": lambda: functions.move_mouse(mouse, center_x, center_y),
        "R3": toggle_high_precision_always_on,
    }

    INPUT_TO_LOGIC_AFTER = {"R1": reset_radius, "L1": reset_radius}

    functions = Functions(keyboard, mouse, INPUT_TO_LOGIC_BEFORE, INPUT_TO_LOGIC_AFTER)

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
                # controller state
                for key in button_state:
                    if button_state[key] == "JUST_PRESSED":
                        button_state[key] = "PRESSED"
                    elif button_state[key] == "JUST_RELEASED":
                        button_state[key] = "NOT_PRESSED"

                left_x = joystick.get_axis(LEFT_JS_X_ID)
                left_y = joystick.get_axis(LEFT_JS_Y_ID)
                is_left_x_active = abs(left_x) > LEFT_JS_DEAD_ZONE
                is_left_y_active = abs(left_y) > LEFT_JS_DEAD_ZONE
                to_left = left_x < 0
                to_up = left_y < 0
                button_state["LEFT_JS_LEFT"] = handle_state(button_state["LEFT_JS_LEFT"], is_left_x_active and to_left)
                button_state["LEFT_JS_RIGHT"] = handle_state(button_state["LEFT_JS_RIGHT"], is_left_x_active and not to_left)
                button_state["LEFT_JS_UP"] = handle_state(button_state["LEFT_JS_UP"], is_left_y_active and to_up)
                button_state["LEFT_JS_DOWN"] = handle_state(button_state["LEFT_JS_DOWN"], is_left_y_active and not to_up)
                right_x = joystick.get_axis(RIGHT_JS_X_ID)
                right_y = joystick.get_axis(RIGHT_JS_Y_ID)
                is_right_x_active = abs(right_x) > RIGHT_JS_DEAD_ZONE
                is_right_y_active = abs(right_y) > RIGHT_JS_DEAD_ZONE
                if has_triggers:
                    is_left_trigger_axis_active = joystick.get_axis(LEFT_TRIGGER_ID) > LEFT_TRIGGER_DEAD_ZONE
                    is_right_trigger_axis_active = joystick.get_axis(RIGHT_TRIGGER_ID) > RIGHT_TRIGGER_DEAD_ZONE

                for event in events:
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = BUTTON_MAPPING.get(event.button)
                        if button is not None:
                            button_state[button] = handle_state(button_state[button], True)
                    elif event.type == pygame.JOYBUTTONUP:
                        button = BUTTON_MAPPING.get(event.button)
                        if button is not None:
                            button_state[button] = handle_state(button_state[button], False)
                    elif event.type == pygame.JOYHATMOTION:
                        button_state["LEFT"] = handle_state(button_state["LEFT"], event.value[0] == -1)
                        button_state["RIGHT"] = handle_state(button_state["RIGHT"], event.value[0] == 1)
                        button_state["DOWN"] = handle_state(button_state["DOWN"], event.value[1] == -1)
                        button_state["UP"] = handle_state(button_state["UP"], event.value[1] == 1)

                # program state
                if button_state["ACTIVATE"] == "JUST_PRESSED":
                    running = False
                    continue
                if has_triggers:
                    high_precision = is_left_trigger_axis_active
                    button_state["R2"] = handle_state(button_state["R2"], is_right_trigger_axis_active)
                else:
                    high_precision = button_state["L2"] in PRESSED
                if button_state["R1"] in PRESSED or button_state["L1"] in PRESSED:
                    current_radius += RIGHT_JS_SENSITIVITY * 0.002
                if button_state["L3"] == "JUST_PRESSED":
                    button_state["R1"] = "NOT_PRESSED"
                    button_state["L1"] = "NOT_PRESSED"

                # action
                for input, key_to_tap in INPUT_TO_KEY_TAP.items():
                    functions.handle_to_key_tap_input(button_state[input], input, key_to_tap)
                for input, key_to_press in INPUT_TO_KEY_HOLD.items():
                    functions.handle_to_key_hold_input(button_state[input], input, key_to_press)
                for input, (x, y) in INPUT_TO_MOUSE_MOVE.items():
                    functions.handle_to_mouse_absolute_move_input(button_state[input], input, x, y)
                for input, key_to_tap in RELEASE_TO_KEY_TAP.items():
                    functions.handle_to_key_tap_release(button_state[input], input, key_to_tap)
                functions.handle_to_click_input(button_state["A"], "A", Button.left)

                if is_right_x_active or is_right_y_active:
                    if high_precision_always_on or high_precision:
                        if time.perf_counter() - last_update_time > 0.1:
                            functions.move_mouse_relative(
                                mouse,
                                round(right_x * RIGHT_JS_SENSITIVITY * 150),
                                round(right_y * RIGHT_JS_SENSITIVITY * 150),
                            )
                            last_update_time = time.perf_counter()
                    else:
                        functions.move_mouse(
                            mouse,
                            round((right_x * center_x * current_radius) + center_x),
                            round((right_y * center_y * current_radius) + center_y),
                        )

            time.sleep(max(0.001 - (time.perf_counter() - loop_start_time), 0))

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
