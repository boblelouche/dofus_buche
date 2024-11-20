import sys

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


def compute_biggest_ratio_rectangle(width, height):
    if width / 4 > height / 3:
        return (height * 4 // 3, height)
    else:
        return (width, width * 3 // 4)


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
                print(window["kCGWindowName"])
                if window["kCGWindowName"] == title:
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
            return self.app.activateWithOptions_(True)

    # i = 0
    # dofuswindow=None
    # for window in windowList:
    #     if window["kCGWindowName"].startswith("Anonway"):
    #         print(i, window)
    #         dofuswindow = window
    #         break
    #     i += 1
    # i = 0
    # dofuswindow = None
    # for window in apps:
    #     if window.localizedName().startswith("Dofus"):
    #         print(i, window)
    #         dofuswindow = window
    #         break
    #     i += 1
    # dofuswindow.activateWithOptions_(True)
    if sys.platform != "darwin":

        @staticmethod
        def get_active_window_title():
            return pgw.getActiveWindowTitle()

        def foreground(self):
            self.window.activate()
