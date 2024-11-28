import sys
import time
import pyautogui
from config import path, directories
from .Cell import Cell
import logging
from Script.ocr import get_text

if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )
else:
    import pywinctl as pwc
    import pygetwindow as pgw


class WindowNotFoundException(Exception):
    pass


def from_cell_id_to_x_y_pos(cell_id, width):
    pos_y = (cell_id // (((width) * 2) - 1)) * 2
    if (cell_id % (((width) * 2) - 1)) >= width:
        pos_y += 1
    if cell_id > (width - 1) * 2:
        add = 1
        pos_x = (cell_id + (pos_y // 2)) % (width) + add
    else:
        pos_x = cell_id % (width) + 1
    return pos_x - 1, pos_y


def compute_biggest_ratio_rectangle(width, height):
    if width / 4 > height / 3:
        return (height * 4 // 3, height)
    else:
        return (width, width * 3 // 4)


MAX_CELL_IN_WIDTH = 14
MAX_CELL_IN_HEIGHT = 16
MINIMAP_POSITION_RATIO = 1.13
CHAR_WIDTH = 13
CHAR_HEIGHT = 25


class Window:
    def __init__(self, title: str):
        self.title = title
        if sys.platform == "darwin":
            self.window = Window.get_window_by_title(title)
            self.app = Window.get_app_by_pid(self.window["kCGWindowOwnerPID"])
            bounds = self.window["kCGWindowBounds"]
            self.height = int(bounds["Height"])
            self.width = int(bounds["Width"])
            self.left = int(bounds["X"])
            self.top = int(bounds["Y"])
        else:
            try:
                self.window = pwc.getWindowsWithTitle(self.title)[0]
            except IndexError as e:
                print(e)
                raise WindowNotFoundException()
            self.width = self.window.width
            self.height = self.window.height
            self.left = self.window.left
            self.top = self.window.top
        self.chat_bar_height = int(0.2165 * self.height)
        self.game_bounds = self.get_game_bounds()
        self.mini_map_width = self.chat_bar_height - 85

        self.minimap_coords = (
            int(
                self.game_bounds[0]
                + (self.game_bounds[2] // 2) * MINIMAP_POSITION_RATIO
                - (self.mini_map_width // 2)
            ),
            int(self.game_bounds[1] + self.game_bounds[3] - self.mini_map_width - 30),
        )

    def get_game_bounds(self):
        (play_box_width, play_box_height) = compute_biggest_ratio_rectangle(
            self.width, self.height - 35
        )
        self.play_box_width = play_box_width
        self.play_box_height = play_box_height
        self.margin_width = (self.width - play_box_width) // 2
        left = self.left + self.margin_width
        top = self.top + 35
        width = self.width - self.margin_width * 2
        height = self.height - 45

        return (left, top, width, height)

    if sys.platform == "darwin":

        @staticmethod
        def get_active_window_title():
            return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()

        @staticmethod
        def get_window_by_title(title: str):
            options = kCGWindowListOptionOnScreenOnly

            windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
            active_window = None
            for window in windowList:
                print(window)
                if "kCGWindowName" in window and window["kCGWindowName"] == title:
                    print(window["kCGWindowName"])
                    active_window = window
                    break

            if not active_window:
                raise WindowNotFoundException()

            return active_window

        @staticmethod
        def get_app_by_pid(pid: int):
            apps = NSWorkspace.sharedWorkspace().runningApplications()

            searched_app = None
            for app in apps:
                if app.processIdentifier() == pid:
                    searched_app = app

            if not searched_app:
                raise WindowNotFoundException()

            return searched_app

        def foreground(self):
            return self.app.activateWithOptions_(0)

    if sys.platform != "darwin":

        @staticmethod
        def get_active_window_title():
            return pgw.getActiveWindowTitle()

        def foreground(self):
            self.window.activate()

    def get_current_position_text(self, nb_chars=7):
        (left, top, width, height) = self.game_bounds
        screenshot_path = path.join(directories["temp"], "minimap.png")
        pyautogui.moveTo(left, top)
        time.sleep(0.5)
        print("move to center")
        self.move_to_minimap_center()
        screenshot = pyautogui.screenshot(
            screenshot_path,
            region=(
                self.minimap_coords[0] + self.mini_map_width // 2,
                self.minimap_coords[1] + self.mini_map_width // 2 - 30,
                CHAR_WIDTH * nb_chars,
                CHAR_HEIGHT,
            ),
        )
        screenshot.save(screenshot_path)
        print("get text")

        return get_text(screenshot_path).strip(" \n\t")

    def confirm_map_change(self, target_position: tuple[int, int], timeout: int = 6):
        print("confirm map change")

        target_position_text = f"{target_position[0]},{target_position[1]}"
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                print("try detection")
                current_position_text = self.get_current_position_text(
                    len(target_position_text)
                )
                logging.info(
                    f"position read {current_position_text} last position {target_position_text}"
                )
                if current_position_text == target_position_text:
                    return True
            except Exception as e:
                print("Map change not confirmed", e)
        return False

    def click_cell(self, cell: Cell, map_width: int):
        padding = (MAX_CELL_IN_WIDTH + 3) - map_width
        (left, top, width, height) = self.game_bounds
        cell_width = width // MAX_CELL_IN_WIDTH
        cell_height = (height - self.chat_bar_height) // MAX_CELL_IN_HEIGHT

        x = (cell.coordinates[0]) * cell_width + padding // 2 + left + cell_width // 2
        y = (cell.coordinates[1] // 2) * cell_height + top + cell_height // 2

        logging.info(f"clicking on {cell.coordinates} at {x, y}")
        pyautogui.click(x, y)

        time.sleep(0.5)

    def move_to_minimap_center(self):
        left = self.minimap_coords[0] + self.mini_map_width // 2
        top = self.minimap_coords[1] + self.mini_map_width // 2

        logging.info(f"moving to minimap center {left} {top}")
        pyautogui.moveTo(
            left,
            top,
        )
