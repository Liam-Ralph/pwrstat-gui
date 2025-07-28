# Copyright (C) 2025 Liam Ralph
# https://github.com/liam-ralph

# This program, including this file, is licensed under the
# GNU General Public License v3.0 (GNU GPLv3).
# See LICENSE or this project's source for more information.
# Project Source: https://github.com/liam-ralph/pwrstat-gui

# PwrStat GUI, a GUI for CyberPower's pwrstat terminal command.

# Search convert-python for help converting this program into a
# standalone Python program.


# Imports

# Tkinter

import tkinter
import tkinter.filedialog
from tkinter import colorchooser
from tkinter import messagebox

# System

import os
import setproctitle
import subprocess
import sys

# Pillow Imaging Library

from PIL import Image, ImageTk

# Others

import csv
import datetime
import re
import threading
import time
import traceback


# Paths

global PATH_DATA
global PATH_IMAGES

# convert-python Change these paths
PATH_DATA = "/usr/share/pwrstat-gui/data"
PATH_IMAGES = "/usr/share/pwrstat-gui/images"


# Functions
# Alphabetical order

def change_color(color_type):

    # Window Variables

    global window_home
    global window_info
    global window_settings

    # Settings Variables

    global darkest
    global dark
    global medium
    global light
    global highlight

    # Getting Color Choice

    color_raw = (
        colorchooser.askcolor(
            parent = window_settings,
            title = "Choose Color for " + color_type.capitalize()
        )[1]
    )

    # Checking Color Choice

    if color_raw is not None and color_raw.startswith("#"):

        color_raw = color_raw.upper()

        if color_raw not in (darkest, dark, medium, light, highlight):

            # Change Variable and Settings File

            with open(PATH_DATA+"/settings.txt", "r") as file:
                text = file.read().strip()

            match (color_type):
                case "darkest":
                    text = text.replace(darkest, color_raw, 1)
                    darkest = color_raw
                case "dark":
                    text = text.replace(dark, color_raw, 1)
                    dark = color_raw
                case "medium":
                    text = text.replace(medium, color_raw, 1)
                    medium = color_raw
                case "light":
                    text = text.replace(light, color_raw, 1)
                    light = color_raw
                case "highlight":
                    text = text.replace(highlight, color_raw, 1)
                    highlight = color_raw

            with open(PATH_DATA+"/settings.txt", "w") as file:
                file.write(text)

            # Reload Windows

            reload_windows()

        else:

            # Color Used Elsewhere

            messagebox.showwarning(
                parent = window_settings,
                title = "Color Choosing Failed",
                message = "Color choosing failed: color already used elsewhere."
            )

    else:

        # Operation Cancelled by User

        messagebox.showwarning(
            parent = window_settings,
            title = "Color Choosing Failed",
            message = "Color choosing failed: operation cancelled."
        )

def change_font(new_font):

    # Global Variables

    global window_settings
    global font

    # Change Font Variable and Settings File

    with open(PATH_DATA+"/settings.txt", "r") as file:
        text = file.read().strip().replace(font, new_font)

    font = new_font

    with open(PATH_DATA+"/settings.txt", "w") as file:
        file.write(text)

    # Reload Windows

    reload_windows()

def change_log_path():

    # Global Variables

    global logging
    global log_path

    # Exit if Logging

    if logging:

        # Logging Active

        messagebox.showwarning(
            parent = window_settings,
            title = "Log Path Choosing Failed",
            message = "Log path choosing failed: cannot change path while logging active."
        )

    else:

        # Choose Log Path

        choice = tkinter.filedialog.askdirectory(parent=window_settings) + "/"

        if not os.path.exists(choice):

            # Chosen Directory Does Not Exist

            messagebox.showwarning(
                parent = window_settings,
                title = "Log Path Choosing Failed",
                message = f"Log path choosing failed: Directory {choice} does not exist."
            )

        else:

            # Change Logging Path Variable and Settings File

            with open(PATH_DATA+"/settings.txt", "r") as file:
                text = file.read().strip().replace(log_path, choice)

            log_path = choice

            with open(PATH_DATA+"/settings.txt", "w") as file:
                file.write(text)

            # Reload Windows

            reload_windows()

def change_sampling_interval(new_sampling_interval):

    # Settings Variable

    global sampling_interval

    # Change Sampling Interval Variable and Settings File

    with open(PATH_DATA+"/settings.txt", "r") as file:
        text = (
            file.read().strip().replace(
                "sampling-interval: " + str(sampling_interval),
                "sampling-interval: " + str(new_sampling_interval)
            ) # '"sampling-interval: " +' needed to prevent replacing an integer from color-set
        )

    sampling_interval = new_sampling_interval

    with open(PATH_DATA+"/settings.txt", "w") as file:
        file.write(text)

    # Reload Windows

    reload_windows()

def check_exit_flag():

    # Used to differentiate between closing windows and reloading windows,
    # since the program will be halted on main window close

    # Global Variables

    global exit_flag
    global clicked

    # Check Exit Flag

    if exit_flag:

        # Update Clicked

        clicked.set(True)

        sys.exit() 

def darken_color(color_raw):

    # Convert Hex Code to RGB

    rgb = [int(color_raw.replace("#", "")[i:i+2], 16) for i in (0, 2, 4)]

    # Darken RGB

    for i in range(3):
        if rgb[i] > 5:
            rgb[i] -= 5
        else:
            rgb[i] = 5 # lighten if dark

    # Return Darkened RGB as Hex Code

    return "#{0:02x}{1:02x}{2:02x}".format(rgb[0], rgb[1], rgb[2])

def open_window_home(window_dimensions=[800, 600], settings_dimensions=None):

    # Home Window Variable

    global window_home

    # Info and Settings Variables

    global names
    global created
    global version
    global updated

    global darkest
    global dark
    global medium
    global light
    global highlight
    global font
    global log_path
    global sampling_interval

    # Logging and Status

    global logging
    global logging_button
    global frame_sides_height
    global frame_main_center
    global graph

    # Exit Flag

    global exit_flag

    exit_flag = True

    # Window Setup

    window_width = window_dimensions[0]
    window_height = window_dimensions[1]

    window_home = tkinter.Tk()
    window_home.geometry(f"{window_width}x{window_height}")
    window_home.minsize(width=window_width, height=window_height)
    window_home.configure(bg=darkest)
    window_home.title("PwrStat GUI")
    window_home.protocol("WM_DELETE_WINDOW", check_exit_flag)
    window_home.iconphoto(
        True,
        ImageTk.PhotoImage(Image.open(PATH_IMAGES+"/logo.png"))
    )
    window_home.update()

    # Home Screen

    frame_main = tkinter.Frame(
        window_home,
        width = window_width,
        height = window_height - 60,
        bg = darkest
    )
    frame_main.pack_propagate(False)
    frame_main.pack(fill=tkinter.BOTH, expand=True)
    frame_footer = tkinter.Frame(
        window_home,
        width = window_width,
        height = 60,
        bg = dark
    )
    frame_footer.pack_propagate(False)
    frame_footer.pack(fill=tkinter.BOTH, expand=False)
    window_home.update()

    # Footer Frame Buttons

    tkinter.Button(
        frame_footer,
        text = "Close",
        font = (font, 12),
        width = 10,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = window_home.destroy
    ).pack(
        side = tkinter.RIGHT,
        padx = 10
    )
    tkinter.Button(
        frame_footer,
        text = "Info",
        font = (font, 12),
        width = 10,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = open_window_info
    ).pack(
        side = tkinter.RIGHT,
        padx = 10
    )
    tkinter.Button(
        frame_footer,
        text = "Settings",
        font = (font, 12),
        width = 10,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = open_window_settings
    ).pack(
        side = tkinter.RIGHT,
        padx = 10
    )
    window_home.update()

    # Logging Toggle

    logging_button = tkinter.Checkbutton(
        frame_footer,
        text = "Logging",
        bg = medium,
        fg = light,
        command = toggle_logging
    )
    logging_button.pack(
        side = tkinter.LEFT,
        padx = 15
    )
    window_home.update()

    # Main Frame

    frame_main_title = tkinter.Label(
        frame_main,
        text = "UPS Monitoring",
        font = (font, 12),
        bg = darkest,
        fg = highlight
    )
    frame_main_title.pack(
        pady = 10
    )

    frame_sides_height = 60 - frame_main_title.winfo_height()

    frame_main_left = tkinter.Frame(
        frame_main,
        width = 200,
        height = window_height - frame_sides_height,
        bg = darkest
    )
    frame_main_left.pack_propagate(False)
    frame_main_left.pack(
        side = tkinter.LEFT,
        fill = tkinter.BOTH,
        expand = False
    )

    frame_main_center = tkinter.Frame(
        frame_main,
        width = 200,
        height = window_height - frame_sides_height,
        bg = darkest
    )
    frame_main_center.pack_propagate(False)
    frame_main_center.pack(
        side = tkinter.LEFT,
        fill = tkinter.BOTH,
        expand = False
    )

    frame_main_right = tkinter.Frame(
        frame_main,
        width = window_width - 400,
        height = window_height - frame_sides_height,
        bg = dark
    )
    frame_main_right.pack_propagate(False)
    frame_main_right.pack(
        side = tkinter.RIGHT,
        fill = tkinter.BOTH,
        expand = True
    )
    window_home.update()

    # Main Left Frame

    for item in [
        "State", "Utility Voltage", "Output Voltage",
        "Battery Capacity", "Remaining Runtime", "Load (Watts)", "Load (%)"
    ]:
        tkinter.Label(
            frame_main_left,
            text = item,
            font = (font, 12),
            anchor = "e",
            width = 20,
            fg = light,
            bg = darkest,
            height = 1
        ).pack(
            padx = 10,
            pady = 10
        )
        window_home.update()

    # Main Center Frame

    for _ in range(7):
        tkinter.Label(
            frame_main_center,
            text = "...",
            font = (font, 12),
            width = 20,
            fg = highlight,
            bg = darkest,
            height = 1
        ).pack(
            padx = 10,
            pady = 10
        )
        window_home.update()

    # Main Right Frame

    graph = tkinter.Canvas(
        frame_main_right,
        width = frame_main_right.winfo_width(),
        height = frame_main_right.winfo_height(),
        bg = darkest
    )
    graph.pack(fill=tkinter.BOTH, expand=True)

    # Open Child Window

    if settings_dimensions is not None:
        open_window_settings(settings_dimensions)

    # Window Mainloop

    window_home.mainloop()

def open_window_info(window_dimensions=[500, 500]):

    # Window Variables

    global window_home
    global window_info

    # Info and Settings Variables

    global names
    global created
    global version
    global updated

    global darkest
    global dark
    global medium
    global light
    global highlight
    global font

    # Info Window Setup

    window_width = window_dimensions[0]
    window_height = window_dimensions[1]

    window_info = tkinter.Toplevel(window_home, bg=darkest)
    window_info.grab_set()
    window_info.geometry(f"{window_width}x{window_height}")
    window_info.minsize(width=window_width, height=window_height)
    window_info.title("PwrStat GUI Info")
    window_info.iconphoto(
        True,
        ImageTk.PhotoImage(Image.open(PATH_IMAGES+"/info.png"))
    )

    frame_main = tkinter.Frame(
        window_info,
        width = window_width,
        height = window_height - 60,
        bg = darkest
    )
    frame_main.pack_propagate(False)
    frame_main.pack(fill=tkinter.BOTH, expand=True)
    frame_footer = tkinter.Frame(
        window_info,
        width = window_width,
        height = 60,
        bg = dark
    )
    frame_footer.pack_propagate(False)
    frame_footer.pack(fill=tkinter.BOTH, expand=False)
    window_info.update()

    # Close Window Button

    tkinter.Button(
        frame_footer,
        text = "Close",
        font = (font, 12),
        width = 10,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = window_info.destroy
    ).pack(
        side = tkinter.RIGHT,
        padx = 10
    )
    window_info.update()

    # App Info

    tkinter.Label(
        frame_main,
        text = "PwrStat GUI",
        font = (font, 20),
        fg = highlight,
        bg = darkest,
        height = 2
    ).pack()
    tkinter.Label(
        frame_main,
        text = (
            names + "\n" +
            f"Created {created}\n" +
            f"Version {version}\n" +
            f"Last Updated {updated}\n"
        ),
        font = (font, 12),
        fg = light,
        bg = darkest,
        height = 5
    ).pack()
    window_info.update()

    # UPS Info

    ups_info_raw = (
        subprocess.run(
            ["pwrstat", "-status"],
            capture_output = True,
            text = True
        ).stdout
    ).strip()

    tkinter.Label(
        frame_main,
        text = "UPS Information",
        font = (font, 20),
        fg = highlight,
        bg = darkest,
        height = 2
    ).pack()
    window_info.update()

    if "Properties" in ups_info_raw:

        properties_raw = ups_info_raw.split("\n\n")[1].split("\n")
        properties = [
            [property_raw.split(". ")[0].strip().replace(".", ""),
            property_raw.split(". ")[1].strip()]
            for property_raw in properties_raw[1:]
        ]

        for property in properties:
            tkinter.Label(
                frame_main,
                text = f"{property[0]}: {property[1]}",
                font = (font, 12),
                fg = light,
                bg = darkest,
                height = 1
            ).pack()
            window_info.update()

    else:

        tkinter.Label(
            frame_main,
            text = (
                "No UPS info available,\n" +
                "check connection using lsusb."
            ),
            font = (font, 12),
            fg = light,
            bg = darkest,
            height = 7
        ).pack()
        window_info.update()

    # Window Mainloop

    window_info.mainloop()

def open_window_settings(window_dimensions=[800, 600]):

    # Window Variables

    global window_home
    global window_settings

    # Settings Variables

    global darkest
    global dark
    global medium
    global light
    global highlight
    global font
    global log_path
    global sampling_interval

    # Settings Window Setup

    window_width = window_dimensions[0]
    window_height = window_dimensions[1]

    window_settings = tkinter.Toplevel(window_home, bg=darkest)
    window_settings.grab_set()
    window_settings.geometry(f"{window_width}x{window_height}")
    window_settings.minsize(width=window_width, height=window_height)
    window_settings.minsize(width=window_width, height=window_height)
    window_settings.title("PwrStat GUI Settings")
    window_settings.iconphoto(
        True,
        ImageTk.PhotoImage(Image.open(PATH_IMAGES+"/settings.png"))
    )

    frame_main = tkinter.Frame(
        window_settings,
        width = window_width,
        height = window_height - 60,
        bg = darkest
    )
    frame_main.pack_propagate(False)
    frame_main.pack(fill=tkinter.BOTH, expand=True)
    frame_footer = tkinter.Frame(window_settings,
        width = window_width,
        height = 60,
        bg = dark
    )
    frame_footer.pack_propagate(False)
    frame_footer.pack(fill=tkinter.BOTH, expand=False)
    window_settings.update()

    # Footer Frame Buttons

    tkinter.Button(
        frame_footer,
        text = "Close",
        font = (font, 12),
        width = 10,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = window_settings.destroy
    ).pack(
        side = tkinter.RIGHT,
        padx = 10
    )

    tkinter.Button(
        frame_footer,
        text = "Reset Settings",
        font = (font, 12),
        width = 15,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = reset_settings
    ).pack(
        side = tkinter.RIGHT,
        padx = 10
    )

    # Settings Title

    tkinter.Label(
        frame_main,
        text = "Settings",
        font = (font, 20),
        fg = highlight,
        bg = darkest,
        height = 2
    ).pack()
    window_settings.update()

    # Settings Frames

    color_set_frame = tkinter.Frame(
        frame_main,
        width = 800,
        height = 50,
        bg = darken_color(darkest)
    )
    color_set_frame.pack_propagate(False)
    color_set_frame.pack(fill=tkinter.BOTH, expand=True) # Actual height > 50

    font_frame = tkinter.Frame(
        frame_main,
        width = 800,
        height = 50,
        bg = darkest
    )
    font_frame.pack_propagate(False)
    font_frame.pack(fill=tkinter.BOTH, expand=True)

    log_path_frame = tkinter.Frame(
        frame_main,
        width = 800,
        height = 50,
        bg = darken_color(darkest)
    )
    log_path_frame.pack_propagate(False)
    log_path_frame.pack(fill=tkinter.BOTH, expand=True)

    sampling_interval_frame = tkinter.Frame(
        frame_main,
        width = 800,
        height = 50,
        bg = darkest
    )
    sampling_interval_frame.pack_propagate(False)
    sampling_interval_frame.pack(fill=tkinter.BOTH, expand=True)

    window_settings.update()

    # Color Set Setting

    tkinter.Label(
        color_set_frame,
        text = "Color Set",
        font = (font, 14),
        fg = highlight,
        bg = darken_color(darkest),
        width = 11,
        height = 1
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        color_set_frame,
        text = (
            "Darkest\n" +
            darkest + "\n" +
            "Default:\n#000000"
        ),
        font = (font, 10),
        width = 12,
        height = 4,
        fg = light,
        bg = darkest,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_color("darkest")
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        color_set_frame,
        text = (
            "Dark\n" +
            dark + "\n" +
            "Default:\n#101010"
        ),
        font = (font, 10),
        width = 12,
        height = 4,
        fg = light,
        bg = dark,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_color("dark")
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        color_set_frame,
        text = (
            "Medium\n" +
            medium + "\n" +
            "Default:\n#202020"
        ),
        font = (font, 10),
        width = 12,
        height = 4,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_color("medium")
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        color_set_frame,
        text = (
            "Light\n" +
            light + "\n" +
            "Default:\n#404040"
        ),
        font = (font, 10),
        width = 12,
        height = 4,
        fg = darkest,
        bg = light,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_color("light")
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        color_set_frame,
        text = (
            "Highlight\n" +
            highlight + "\n" +
            "Default:\n#AA0000"
        ),
        font = (font, 10),
        width = 12,
        height = 4,
        fg = darkest,
        bg = highlight,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_color("highlight")
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    window_settings.update()

    # Font Setting

    tkinter.Label(
        font_frame,
        text = "Font",
        font = (font, 14),
        fg = highlight,
        bg = darkest,
        width = 6,
        height = 1
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    font_choice = tkinter.StringVar()
    font_choice.set(font)
    tkinter.OptionMenu(
        font_frame,
        font_choice,
        *[
            "Garamond",
            "Segoe UI",
            "Times New Roman",
            "Arial",
            "Verdana",
            "Helvetica",
            "Ubuntu",
            "Noto Sans",
            "Comic Sans",
            "Courier New",
            "Hack",
            "Monospace Regular 12",
        ],
        command = change_font
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    window_settings.update()

    # Logging Path Setting

    tkinter.Label(
        log_path_frame,
        text = f"Log Path: {log_path}",
        font = (font, 14),
        fg = highlight,
        bg = darken_color(darkest),
        width = (10 + len(log_path)),
        height = 1
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        log_path_frame,
        text = "Change Log Path",
        font = (font, 10),
        width = 16,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = change_log_path
    ).pack(
        side = tkinter.LEFT,
        padx = 15
    )

    # Sampling Interval Setting

    sampling_interval_choice = tkinter.DoubleVar()
    sampling_interval_choice.set(sampling_interval)
    tkinter.Label(
        sampling_interval_frame,
        text = "Sampling Interval",
        font = (font, 14),
        fg = highlight,
        bg = darkest,
        width = 17,
        height = 1
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Scale(
        sampling_interval_frame,
        variable = sampling_interval_choice,
        from_ = 1,
        to = 10,
        resolution = 0.5,
        orient = tkinter.HORIZONTAL,
        fg = highlight,
        bg = medium,
        troughcolor = dark,
        activebackground = light
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Button(
        sampling_interval_frame,
        text = "Update",
        font = (font, 10),
        width = 8,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_sampling_interval(sampling_interval_choice.get())
    ).pack(
        side = tkinter.LEFT,
        padx = 15
    )

    window_settings.update()

    # Window Mainloop

    window_settings.mainloop()

def reload_windows():

    # Window Variables

    global window_home
    global window_settings

    # Exit Flag

    global exit_flag

    exit_flag = False

    # Get Current Window Heights

    current_home_dimensions = [
        window_home.winfo_width(),
        window_home.winfo_height()
    ]
    current_settings_dimensions = [
        window_settings.winfo_width(),
        window_settings.winfo_height()
    ]

    # Close Home Window

    window_home.destroy()

    # Reopen Home Window

    open_window_home(
        window_dimensions = current_home_dimensions,
        settings_dimensions = current_settings_dimensions
    )

def reset_settings():

    # Global Variables

    global darkest
    global dark
    global medium
    global light
    global highlight
    global font
    global log_path
    global sampling_interval

    # Resetting Variables

    darkest = "#000000"
    dark = "#101010"
    medium = "#202020"
    light = "#404040"
    highlight = "#AA0000"
    font = "Garamond"
    log_path = "NOT SET"
    sampling_interval = 1.0

    # Resetting Settings File

    with open(PATH_DATA+"/settings.txt", "w") as file:
        file.write(
            """color-set: #000000, #101010, #202020, #404040, #AA0000
            font: Garamond
            log-path: NOT SET
            sampling-interval: 1.0""".replace("    ", "") # remove code indents
        )

    # Reload Windows

    reload_windows()

def toggle_logging():

    # Home Window

    global window_home

    # Logging Variables

    global logging
    global logging_button
    global log_path

    if not logging:

        # Start Logging

        if log_path == "NOT SET":

            messagebox.showwarning(
                parent = window_home,
                title = "Logging Failed",
                message = "Logging failed: path not set."
            )

            logging_button.deselect()
            return

        elif not os.path.exists(log_path):

            messagebox.showwarning(
                parent = window_home,
                title = "Logging Failed",
                message = f"Logging failed: Directory {log_path} does not exist."
            )

            logging_button.deselect()
            return
        
    # Change Logging

    logging = not logging

def update_graph():

    # Global Variables

    global stats_list
    global graph
    global sampling_interval
    global max_watts
    global font

    while True:

        try:

            if "stats_list" in globals() and "graph" in globals() and stats_list != []:
            # Check if these variables exist yet

                # Clear Graph

                graph.delete(tkinter.ALL)

                # Calculate Variables

                width = graph.winfo_width()
                height = graph.winfo_height()
                max_time = stats_list[-1][0]
                if len(stats_list) == 60:
                    time_width = max_time - stats_list[0][0]
                else:
                    time_width = 60 * sampling_interval

                # Create Polygon Points

                # Bottom left point, polygon start point
                points = [
                    (width - int(round(width * (max_time - stats_list[0][0]) / time_width)), height)
                ]

                for [stat_time, watts] in stats_list:
                    # Top points, show data
                    time_pct = (max_time - stat_time) / time_width
                    watts_pct = watts / max_watts
                    points.append((
                        width - int(round(width * time_pct)),
                        height - int(round(height * watts_pct))
                    ))

                # Bottom right point, polygon end point
                points.append((width, height))

                # Create Polygon on Graph

                # after() is needed because tkinter isn't thread-safe
                # (stupid? maybe. functional? hopefully)
                graph.winfo_toplevel().after(0, lambda: graph.create_polygon(
                    points,
                    fill = highlight
                ))

                # Create Graph Lines

                for i in range(10):

                    line_height = i / 10 * height

                    graph.winfo_toplevel().after(0, lambda: graph.create_line(
                        0,
                        line_height,
                        width,
                        line_height,
                        fill = dark
                    ))
                    graph.winfo_toplevel().after(0, lambda: graph.create_text(
                        30,
                        line_height - 10,
                        text = str(int((10 - i) / 10 * max_watts)),
                        font = (font, 15),
                        fill = light
                    ))

                # Wait 100 Miliseconds to Update Graph

                time.sleep(0.1)

            else:

                # Variables not ready, wait and check again
                time.sleep(0.5)

        except(NameError, tkinter.TclError):

            # Error Caught, Print Warning and Wait

            print(
                "An error has been detected, and caught.\n" +
                "If you don't notice any problems, this error can be ignored.\n\n" +
                traceback.format_exc() + "\n"
            )
            
            time.sleep(0.5)

def update_status():

    # Global Variables

    global stats_list
    global max_watts
    global logging
    global log_path
    global frame_main_center
    global sampling_interval

    # Create Stats List

    if "stats_list" not in globals():
        stats_list = []

    while True:

        try:

            # Get UPS Info

            ups_info_raw = (
                subprocess.run(
                    ["pwrstat", "-status"],
                    capture_output = True,
                    text = True
                ).stdout
            ).strip()

            if "Properties" in ups_info_raw:

                # UPS Known, Getting State

                lines = ups_info_raw.replace(".", "").split("\n")

                state = "Unknown"

                for line in lines:
                    if "State" in line:
                        state = line.replace("State", "").strip()
                        break

                if state == "Normal":

                    # UPS Connected, Processing Info

                    values = ["0"] * 6

                    for line in lines:
                        if "Rating Power" in line:
                            max_watts = int(re.sub(r"\D", "", line))
                            continue
                        elif "Utility" in line:
                            values[0] = re.sub(r"\D", "", line)
                            continue
                        elif "Output" in line:
                            values[1] = re.sub(r"\D", "", line)
                            continue
                        elif "Battery" in line:
                            values[2] = re.sub(r"\D", "", line)
                            continue
                        elif "Runtime" in line:
                            values[3] = re.sub(r"\D", "", line)
                            continue
                        elif "Load" in line:
                            value = re.sub(r"[^\d(]", "", line)
                            values[4], values[5] = value.split("(")

                    # Logging

                    if logging:

                        file_path = (
                            log_path + datetime.datetime.today().strftime("%Y-%m-%d") +
                            "_pwrstat-gui-log.csv"
                        )
                        # e.g. /home/john-doe/Desktop/2000-01-01_pwrstat-gui-log.csv

                        if not os.path.exists(file_path):

                            # File Doesn't Exist, Create and Add First Row

                            with open(file_path, mode="w", newline="") as file:
                                csv.writer(file).writerows(
                                    [[
                                        "Time", "Utility Voltage", "Output Voltage",
                                        "Battery Capacity", "Remaining Runtime",
                                        "Load (Watts)", "Load (%)"
                                    ]]
                                )

                        # Add Info Row

                        extended_values = [str(time.time())]
                        extended_values.extend(values)

                        with open(file_path, mode="a", newline="") as file:
                            csv.writer(file).writerows(
                                [
                                    extended_values
                                ]
                            )

                    # Update Stats List

                    stats_list.append([time.time(), int(values[4])])

                    if len(stats_list) > 60:
                        stats_list = stats_list[-60:]

                    # Update Main Window Values

                    values[0] += " Volts"
                    values[1] += " Volts"
                    values[2] += "%"
                    values[3] += " mins"
                    values[4] += " Watts"
                    values[5] += "%"

                    children = frame_main_center.winfo_children()
                    children[0].config(text="Normal")

                    for i in range(6):
                        children[i+1].config(text=values[i])

                else:

                    # UPS Not Connected

                    for child in frame_main_center.winfo_children():

                        child.config(text="N/A")
                    
                    frame_main_center.winfo_children()[0].config(text=state)

            else:

                # UPS Unknown

                for child in frame_main_center.winfo_children():

                    child.config(text="N/A")

            time.sleep(sampling_interval)

        except(NameError, tkinter.TclError):

            # Error Caught, Print Warning and Wait

            print(
                "An error has been detected, and caught.\n" +
                "If you don't notice any problems, this error can be ignored.\n\n" +
                traceback.format_exc() + "\n"
            )

            time.sleep(0.5)


# Main Function

def main():

    # Info and Settings Variables

    global names
    global created
    global version
    global updated

    global darkest
    global dark
    global medium
    global light
    global highlight
    global font
    global log_path
    global sampling_interval

    # Logging

    global logging

    logging = False

    # Exit Flag

    global exit_flag
    global clicked

    exit_flag = True

    # Getting Root Privileges
    # convert-python Remove this section, up to "Info and Settings Reading"

    if os.geteuid() != 0:

        # Get DISPLAY and XAUTHORITY if they exist
        env = os.environ.copy()
        display = env.get("DISPLAY", ":0")  # Default to :0 if missing
        xauthority = env.get("XAUTHORITY", "/tmp/xauth_XIOaut")

        # Relaunch with pkexec and pass the environment variables

        command = [
            "pkexec",
            "env",
            f"DISPLAY={display}",
            f"XAUTHORITY={xauthority}",
            sys.executable
        ] + sys.argv
        os.execvp("pkexec", command)

    # Info and Settings Reading

    with open(PATH_DATA+"/info.txt", "r") as file:
        info_raw = file.read().split("\n")
    names = info_raw[0].replace("Names: ", "")
    created = info_raw[1].replace("Created: ", "")
    version = info_raw[2].replace("Version: ", "")
    updated = info_raw[3].replace("Updated: ", "")

    with open(PATH_DATA+"/settings.txt", "r") as file:
        settings_raw = file.read().split("\n")
    color_set = settings_raw[0].replace("color-set: ", "").split(", ")
    darkest = color_set[0]
    dark = color_set[1]
    medium = color_set[2]
    light = color_set[3]
    highlight = color_set[4]
    font = settings_raw[1].replace("font: ", "")
    log_path = settings_raw[2].replace("log-path: ", "")
    sampling_interval = float(settings_raw[3].replace("sampling-interval: ", ""))

    # Window Setup

    window_start = tkinter.Tk()
    window_start.geometry("800x600")
    window_start.minsize(width=800, height=600)
    window_start.configure(bg=darkest)
    window_start.title("PwrStat GUI")
    window_start.protocol("WM_DELETE_WINDOW", check_exit_flag)
    window_start.iconphoto(
        False,
        ImageTk.PhotoImage(Image.open(PATH_IMAGES+"/logo.png"))
    )
    window_start.update()

    setproctitle.setproctitle("pwrstat-gui")

    # Starting Screen

    tkinter.Label(
        window_start,
        text = "PwrStat GUI",
        font = (font, 20),
        fg = highlight,
        bg = darkest,
        height = 2
    ).pack()
    tkinter.Label(
        window_start,
        text = (
            "A graphical user interface for PowerPanel on Linux.\n" +
            "Created by " + names + ".\n" +
            "Licensed under the GNU General Public License v3.0.\n" +
            "v" + version + "\n\n"
        ),
        font = (font, 10),
        fg = light,
        bg = darkest,
        height = 4
    ).pack()
    window_start.update()

    # Dependency Check

    if (not "powerpanel" in subprocess.run(
        ["dpkg-query", "--list", "powerpanel"],
        capture_output = True,
        text = True
    ).stdout):
        tkinter.Label(
            window_start,
            text = (
                "PowerPanel Linux must be installed.\n" +
                "App shutdown in 5 seconds."
            ),
            font = (font, 20),
            fg = "#AA0000",
            bg = darkest,
            height = 2
        ).pack()
        window_start.update()
        time.sleep(5)
        window_start.destroy()
        sys.exit()

    # Starting Threading

    update_thread = threading.Thread(target=update_status)
    update_thread.daemon = True
    update_thread.start()

    update_graph_thread = threading.Thread(target=update_graph)
    update_graph_thread.daemon = True
    update_graph_thread.start()

    # Clear Window

    clicked = tkinter.BooleanVar()
    button = tkinter.Button(
        window_start,
        text = "Start",
        font = (font, 12),
        width = 10,
        height = 2,
        fg = light,
        bg = dark,
        activeforeground = highlight,
        activebackground = medium,
        command = lambda: clicked.set(True)
    )
    button.pack()
    window_start.update()

    button.wait_variable(clicked)
    exit_flag = False
    window_start.destroy()

    # Home Window

    open_window_home()


# Run Main Function

if __name__ == "__main__":
    main()