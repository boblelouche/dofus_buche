from pynput import mouse, keyboard
import logging
from typing import Callable


def on_key_press(key):
    try:
        logging.debug(f"Key {key.char} pressed")
    except AttributeError:
        logging.debug(f"Special key {key} pressed")


def get_wait_key_handler(
    key: keyboard.Key, callback: Callable[[keyboard.Key], None] | None = None
):
    def handler(pressed_key: keyboard.Key):
        try:
            logging.debug(f"Key {key.char} released")
        except AttributeError:
            logging.debug(f"Special key {key} released")

        if callback is not None:
            callback(pressed_key)

        return pressed_key != key

    return handler


def wait_for_key(
    key: keyboard.Key, callback: Callable[[keyboard.Key], None] | None = None
):
    on_release = get_wait_key_handler(key, callback)

    with keyboard.Listener(on_key_press, on_release) as listener:
        listener.join()


def wait_for_esc(callback: Callable[[keyboard.Key], None] | None = None):
    logging.info("waiting for press escape")
    wait_for_key(keyboard.Key.esc, callback)


def get_wait_click_handler(result: list | None = None):
    def on_mouse_click(x, y, button, pressed):
        logging.debug(f"{button} {"Pressed" if pressed else "Released"} at {(x, y)}")

        if result is not None:
            result[0] = x
            result[1] = y

        if not pressed:
            return False

    return on_mouse_click


# Click other than left click doesn't work on OSX
def wait_for_click(result: list | None = None):
    result = result or [None, None]

    # on_mouse_click = get_wait_click_handler(result)
    def on_mouse_click(x, y, button, pressed):
        logging.debug(f"{button} {"Pressed" if pressed else "Released"} at {(x, y)}")

        if result is not None:
            result[0] = x
            result[1] = y

        if not pressed:
            return False

    with mouse.Listener(on_click=on_mouse_click) as listener:
        listener.join()

    return (result[0], result[1])
