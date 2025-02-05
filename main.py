# Created by Liam Ralph
# https://github.com/Liam-Ralph
# Shared under the MIT License (see LICENSE file)


# Imports

import os
import subprocess
import time
import tkinter
from tkinter import ttk


# Variables

darkest_blue = "#000712"
dark_blue = "#001429"
medium_blue = "#001F3D"
light_blue = "#2C4F70"

yellow = "#FFC200"
off_white = "#C0C0C0"
medium_grey = "#8C8C8C"


# Main Function

def main():

    # Window Setup

    window = tkinter.Tk()
    window.geometry("500x500")
    window.configure(bg=darkest_blue)
    window.title("PwrStat GUI")
    window.update()

    # Starting Screen

    tkinter.Label(
        window,
        text="PwrStat GUI",
        font=("Garamond", 20),
        fg=yellow,
        bg=darkest_blue,
        height=2
    ).pack()
    tkinter.Label(
        window,
        text=(
            "A graphical user interface for PowerPanel on Linux.\n" +
            "Created by Liam Ralph.\n" +
            "v0.0\n"
        ),
        font=("Garamond", 10),
        fg=light_blue,
        bg=darkest_blue,
        height=4
    ).pack()
    window.update()

    # Dependency Check

    if (not "powerpanel" in
    subprocess.run(["dpkg-query", "--list", "powerpanel"], capture_output=True, text=True).stdout):
        tkinter.Label(
            window,
            text=(
                "PowerPanel Linux must be installed.\n" +
                "App shutdown in 5 seconds."
            ),
            font=("Arial", 20),
            fg="#AA0000",
            bg=darkest_blue,
            height=2
        ).pack()
        window.update()
        time.sleep(5)
        window.destroy()
        exit()

    # Clear Window

    clicked = tkinter.BooleanVar()
    button = tkinter.Button(
        window,
        text="Start",
        width=10,
        height=2,
        fg=light_blue,
        bg=dark_blue,
        activeforeground=light_blue,
        activebackground=medium_blue,
        command=lambda: clicked.set(True)
    )
    button.pack()
    window.update()

    button.wait_variable(clicked)
    for child in window.winfo_children():
        child.destroy()

    # Window Mainloop

    window.mainloop()


# Run Main Function

main()