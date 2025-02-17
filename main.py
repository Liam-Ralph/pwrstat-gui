# Created by Liam Ralph
# https://github.com/liam-ralph
# Source at https://github.com/liam-ralph/pwrstat-gui


# Imports

from PIL import Image, ImageTk
import setproctitle
import subprocess
import time
import tkinter
from tkinter import colorchooser
from tkinter import messagebox


# Variables

global PATH_DATA
global PATH_IMAGES

PATH_DATA = "data"
PATH_IMAGES = "images"


# Functions
# Alphabetical order

def change_font(new_font):

    # Settings Variable

    global font

    # Change Font Variable and Settings File

    with open(PATH_DATA+"/settings.txt", "r") as file:
        text = file.read().strip().replace(font, new_font)

    font = new_font

    with open(PATH_DATA+"/settings.txt", "w") as file:
        file.write(text)

    # Reload Windows

    reload_windows()

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

    # Color Replacement

    color_raw = (
        colorchooser.askcolor(
            parent = window_settings,
            title = "Choose Color for " + color_type.capitalize()
        )[1]
    )

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

            messagebox.showwarning(
                parent = window_settings,
                title = "Color Choosing Failed",
                message = "Color choosing failed: color already selected."
            )

    else:

        messagebox.showwarning(
            parent = window_settings,
            title = "Color Choosing Failed",
            message = "Color choosing failed: operation cancelled."
        )

def change_sample_interval(new_sample_interval):

    # Settings Variable

    global sample_interval

    # Change Font Variable and Settings File

    with open(PATH_DATA+"/settings.txt", "r") as file:
        text = (
            file.read().strip().replace(
                "sample-interval: " + str(sample_interval),
                "sample-interval: " + str(new_sample_interval)
            ) # '"sample-interval: " +' needed to prevent replacing an integer from color-set
        )

    sample_interval = new_sample_interval

    with open(PATH_DATA+"/settings.txt", "w") as file:
        file.write(text)

    # Reload Windows

    reload_windows()

def check_exit_flag():

    # Global Variables

    global exit_flag
    global clicked

    # Check Exit Flag

    if exit_flag:

        # Update Clicked

        clicked.set(True)

        exit()

def darken_color(color_raw):

    # Convert Hex Code to RGB

    rgb = [int(color_raw.replace("#", "")[i:i+2], 16) for i in (0, 2, 4)]

    # Darken RGB

    for i in range(3):
        if rgb[i] > 3:
            rgb[i] -= 3
        else:
            rgb[i] = 3 # lighten if dark

    # Return Darkened RGB as Hex Code

    return "#{0:02x}{1:02x}{2:02x}".format(rgb[0], rgb[1], rgb[2])

def open_window_home(window_dimensions=[800, 600], settings_dimensions=None):

    # Home Window Variable

    global window_home

    # Info and Settings Variables

    global name
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
    global sample_interval

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
    window_home.update()

    # Home Screen

    frame_main = tkinter.Frame(
        window_home,
        width = window_width,
        height = window_height - 100,
        bg = darkest
    )
    frame_main.pack_propagate(False)
    frame_main.pack(fill=tkinter.BOTH, expand=True)
    frame_footer = tkinter.Frame(
        window_home,
        width = window_width,
        height = 100,
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

    global name
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

    frame_main = tkinter.Frame(
        window_info,
        width = window_width,
        height = window_height - 100,
        bg = darkest
    )
    frame_main.pack_propagate(False)
    frame_main.pack(fill=tkinter.BOTH, expand=True)
    frame_footer = tkinter.Frame(
        window_info,
        width = window_width,
        height = 100,
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
            name + "\n" +
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
            ["sudo", "pwrstat", "-status"],
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
    global sample_interval

    # Settings Window Setup

    window_width = window_dimensions[0]
    window_height = window_dimensions[1]

    window_settings = tkinter.Toplevel(window_home, bg=darkest)
    window_settings.grab_set()
    window_settings.geometry(f"{window_width}x{window_height}")
    window_settings.minsize(width=window_width, height=window_height)
    window_settings.minsize(width=window_width, height=window_height)
    window_settings.title("PwrStat GUI Settings")

    frame_main = tkinter.Frame(
        window_settings,
        width = window_width,
        height = window_height - 100,
        bg = darkest
    )
    frame_main.pack_propagate(False)
    frame_main.pack(fill=tkinter.BOTH, expand=True)
    frame_footer = tkinter.Frame(window_settings,
        width = window_width,
        height = 100,
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

    log_toggle_frame = tkinter.Frame(
        frame_main,
        width = 800,
        height = 50,
        bg = darkest
    )
    log_toggle_frame.pack_propagate(False)
    log_toggle_frame.pack(fill=tkinter.BOTH, expand=True)

    sample_interval_frame = tkinter.Frame(
        frame_main,
        width = 800,
        height = 50,
        bg = darken_color(darkest)
    )
    sample_interval_frame.pack_propagate(False)
    sample_interval_frame.pack(fill=tkinter.BOTH, expand=True)

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
            "Default:\n#000712"
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
            "Default:\n#001429"
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
            "Default:\n#001F3D"
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
            "Default:\n#2C4F70"
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
            "Default:\n#FFC300"
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

    # Sample Interval Setting

    sample_interval_choice = tkinter.DoubleVar()
    sample_interval_choice.set(sample_interval)
    tkinter.Label(
        sample_interval_frame,
        text = "Sample Interval",
        font = (font, 14),
        fg = highlight,
        bg = darken_color(darkest),
        width = 17,
        height = 1
    ).pack(
        side = tkinter.LEFT,
        padx = 5
    )

    tkinter.Scale(
        sample_interval_frame,
        variable = sample_interval_choice,
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
        sample_interval_frame,
        text = "Update",
        font = (font, 10),
        width = 8,
        height = 1,
        fg = light,
        bg = medium,
        activeforeground = highlight,
        activebackground = light,
        command = lambda: change_sample_interval(sample_interval_choice.get())
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
        window_home.winfo_width(),
        window_home.winfo_height()
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
    global sample_interval

    # Resetting Variables

    darkest = "#000712"
    dark = "#001429"
    medium = "#001F3D"
    light = "#2C4F70"
    highlight = "#FFC300"
    font = "Garamond"
    log_path = "NOT SET"
    sample_interval = 1.0

    # Resetting Settings File

    with open(PATH_DATA+"/settings.txt", "w") as file:
        file.write(
            """color-set: #000712, #001429, #001F3D, #2C4F70, #FFC300
            font: Garamond
            log-path: NOT SET
            sample-interval: 1.0""".replace("    ", "")
        )

    # Reload Windows

    reload_windows()


# Main Function

def main():

    # Info and Settings Variables

    global name
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
    global sample_interval

    # Button Clicked

    global clicked

    # Exit Flag

    global exit_flag

    exit_flag = True

    # Info and Settings Reading

    with open(PATH_DATA+"/info.txt", "r") as file:
        info_raw = file.read().split("\n")
    name = info_raw[0].replace("Name: ", "")
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
    sample_interval = float(settings_raw[3].replace("sample-interval: ", ""))

    # Window Setup

    window_start = tkinter.Tk()
    window_start.geometry("800x600")
    window_start.minsize(width=800, height=600)
    window_start.configure(bg=darkest)
    window_start.title("PwrStat GUI")
    window_start.protocol("WM_DELETE_WINDOW", check_exit_flag)
    window_start.iconphoto(True, ImageTk.PhotoImage(Image.open(PATH_IMAGES+"/logo.png")))
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
            "Created by Liam Ralph.\n" +
            "v0.0\n"
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
        exit()

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