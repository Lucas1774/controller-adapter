import threading
import time

from pynput.keyboard import Key

KEY_MAPPING = {
    "esc": Key.esc,
    "tab": Key.tab,
}


class Functions:
    def __init__(self, keyboard, mouse, input_to_logic_before, input_to_logic_after):
        self.keyboard = keyboard
        self.mouse = mouse
        self.input_to_logic_before = input_to_logic_before
        self.input_to_logic_after = input_to_logic_after

    def callback_before_action(self, input):
        if input in self.input_to_logic_before:
            self.input_to_logic_before[input]()

    def callback_after_action(self, input):
        if input in self.input_to_logic_after:
            self.input_to_logic_after[input]()

    def move_mouse(self, mouse, x, y):
        mouse.position = (x, y)

    def move_mouse_relative(self, mouse, x, y):
        current_x, current_y = mouse.position
        mouse.position = (current_x + x, current_y + y)

    def press_then_release(self, key_to_tap, callback=None):
        self.keyboard.press(KEY_MAPPING.get(key_to_tap, key_to_tap))
        time.sleep(0.01)
        self.keyboard.release(KEY_MAPPING.get(key_to_tap, key_to_tap))
        if callback:
            callback()

    def handle_to_key_tap_input(self, input_state, input, key_to_tap):
        if input_state == "JUST_PRESSED":
            self.callback_before_action(input)
            threading.Thread(
                target=self.press_then_release, args=(key_to_tap, lambda: self.callback_after_action(input))
            ).start()

    def handle_to_key_hold_input(self, input_state, input, key_to_press):
        if input_state == "JUST_PRESSED":
            self.callback_before_action(input)
            self.keyboard.press(KEY_MAPPING.get(key_to_press, key_to_press))
        elif input_state == "JUST_RELEASED":
            self.keyboard.release(KEY_MAPPING.get(key_to_press, key_to_press))
            self.callback_after_action(input)

    def handle_to_mouse_absolute_move_input(self, input_state, input, x, y):
        if input_state == "JUST_PRESSED":
            self.callback_before_action(input)
            self.move_mouse(self.mouse, x, y)
            self.callback_after_action(input)

    def handle_to_click_input(self, input_state, input, button_to_click):
        if input_state == "JUST_PRESSED":
            self.callback_before_action(input)
            self.mouse.click(button_to_click)
            self.callback_after_action(input)

    def handle_to_key_tap_release(self, input_state, input, key_to_tap):
        if input_state == "JUST_RELEASED":
            self.callback_before_action(input)
            threading.Thread(
                target=self.press_then_release, args=(key_to_tap, lambda: self.callback_after_action(input))
            ).start()

    def handle_state(self, state, is_pressed):
        if is_pressed:
            if state == "NOT_PRESSED":
                state = "JUST_PRESSED"
        else:
            if state == "PRESSED":
                state = "JUST_RELEASED"
        return state
