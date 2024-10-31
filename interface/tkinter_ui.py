import tkinter as tk
from tkinter import Button, Label
import pyautogui

def get_mouse_position():
    position = pyautogui.position()
    return position

def display_position():
    position = get_mouse_position()
    position_label.config(text=f"Position: {position}")
    root.after(100, display_position)  # refresh position every 100 ms

def copy_position():
    position = get_mouse_position()
    root.clipboard_clear()
    root.clipboard_append(str(position))

root = tk.Tk()
root.title("Mouse Position Tracker")

position_label = Label(root, text="")
position_label.pack()

copy_button = Button(root, text="Copy Position", command=copy_position)
copy_button.pack()

display_position()  # start displaying positionPoint(x=483, y=277)

root.mainloop()
