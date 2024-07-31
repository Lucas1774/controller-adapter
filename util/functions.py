import threading
import time

import pyautogui
from pynput.keyboard import Key

KEY_MAPPING = {
    "esc": Key.esc,
    "tab": Key.tab,
}


class Functions:
    def __init__(self, keyboard, mouse, input_to_logic_before):
        self.keyboard = keyboard
        self.mouse = mouse
        self.input_to_logic_before = input_to_logic_before

    def press_then_release(self, key_to_tap):
        self.keyboard.press(KEY_MAPPING.get(key_to_tap, key_to_tap))
        time.sleep(0.01)
        self.keyboard.release(KEY_MAPPING.get(key_to_tap, key_to_tap))

    def handle_to_key_tap_input(self, button_state, input, key_to_tap):
        if button_state[input]:
            if input in self.input_to_logic_before:
                self.input_to_logic_before[input]()
            threading.Thread(target=self.press_then_release, args=(key_to_tap,)).start()
            button_state[input] = False

    def handle_to_key_hold_input(self, button_state, key_state, input, key_to_press):
        if button_state[input]:
            if not key_state[key_to_press]:
                if input in self.input_to_logic_before:
                    self.input_to_logic_before[input]()
                self.keyboard.press(KEY_MAPPING.get(key_to_press, key_to_press))
                key_state[key_to_press] = True
        else:
            if key_state[key_to_press]:
                self.keyboard.release(KEY_MAPPING.get(key_to_press, key_to_press))
                key_state[key_to_press] = False

    def handle_to_mouse_absolute_move_input(self, button_state, input, x, y):
        if button_state[input]:
            if input in self.input_to_logic_before:
                self.input_to_logic_before[input]()
            pyautogui.moveTo(x, y)
            button_state[input] = False

    def handle_to_click_input(self, button_state, input, button_to_click):
        if button_state[input]:
            if input in self.input_to_logic_before:
                self.input_to_logic_before[input]()
            self.mouse.click(button_to_click)
            button_state[input] = False
