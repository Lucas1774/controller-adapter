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

    def handle_to_key_tap_input(self, button_state, input, key_to_tap):
        if button_state[input]:
            self.callback_before_action(input)
            threading.Thread(
                target=self.press_then_release, args=(key_to_tap, lambda: self.callback_after_action(input))
            ).start()
            button_state[input] = False

    def handle_to_key_hold_input(self, button_state, key_state, input, key_to_press):
        if button_state[input]:
            if not key_state[key_to_press]:
                self.callback_before_action(input)
                self.keyboard.press(KEY_MAPPING.get(key_to_press, key_to_press))
                key_state[key_to_press] = True
                self.callback_after_action(input)
        else:
            if key_state[key_to_press]:
                self.keyboard.release(KEY_MAPPING.get(key_to_press, key_to_press))
                key_state[key_to_press] = False

    def handle_to_mouse_absolute_move_input(self, button_state, input, x, y):
        if button_state[input]:
            self.callback_before_action(input)
            self.move_mouse(self.mouse, x, y)
            button_state[input] = False
            self.callback_after_action(input)

    def handle_to_click_input(self, button_state, input, button_to_click):
        if button_state[input]:
            self.callback_before_action(input)
            self.mouse.click(button_to_click)
            button_state[input] = False
            self.callback_after_action(input)

    def handle_to_key_tap_release(self, button_state, key_state, input, key_to_tap):
        if not button_state[input]:
            if key_state[key_to_tap]:
                self.callback_before_action(input)
                threading.Thread(
                    target=self.press_then_release, args=(key_to_tap, lambda: self.callback_after_action(input))
                ).start()
                key_state[key_to_tap] = False
                self.callback_after_action(input)
        else:
            key_state[key_to_tap] = True
