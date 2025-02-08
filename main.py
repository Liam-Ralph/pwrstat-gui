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


# Functions
# Alphabetical order

def choose_color(parent_window, color_type):
    
    # Settings Variables

    global darkest
    global dark
    global medium
    global light
    global highlight

    # Color Replacement

    color_raw = (
        colorchooser.askcolor(
            parent=parent_window,
            title="Choose Color for " + color_type.capitalize()
        )[1]
    )

    if color_raw is not None and color_raw.startswith("#"):

        color_raw = color_raw.upper()

        if color_raw not in (darkest, dark, medium, light, highlight):

            with open("data/settings.txt", "r") as file:
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

            with open("data/settings.txt", "w") as file:
                file.write(text)

        else:

            messagebox.showwarning(
                parent=parent_window,
                title="Color Choosing Failed",
                message="Color choosing failed: color already selected."
            )

    else:

        messagebox.showwarning(
            parent=parent_window,
            title="Color Choosing Failed",
            message="Color choosing failed: operation cancelled."
        )

    # Reopen Settings Window

    parent_window.destroy()
    open_settings()

def darken_color(color_raw):
    rgb = [int(color_raw.replace("#", "")[i:i+2], 16) for i in (0, 2, 4)]
    for i in range(3):
        if rgb[i] > 3:
            rgb[i] -= 3
        else:
            rgb[i] = 0
    return "#{0:02x}{1:02x}{2:02x}".format(rgb[0], rgb[1], rgb[2])

def open_info():

    # Root Window

    global window

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

    info_window = tkinter.Toplevel(window)
    info_window.grab_set()
    info_window.geometry("500x500")
    info_window.minsize(width=500, height=500)
    info_window.maxsize(width=500, height=500)
    info_window.configure(bg=darkest)
    info_window.title("PwrStat GUI Info")

    main_frame = tkinter.Frame(info_window, width=500, height=450, bg=darkest)
    main_frame.pack_propagate(False)
    main_frame.pack(fill=tkinter.BOTH, expand=True)
    footer_frame = tkinter.Frame(info_window, width=500, height=50, bg=dark)
    footer_frame.pack_propagate(False)
    footer_frame.pack(fill=tkinter.BOTH, expand=True)
    info_window.update()

    # Close Window Button

    tkinter.Button(
        footer_frame,
        text="Close",
        font=(font, 12),
        width=10,
        height=1,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=info_window.destroy
    ).pack(
        side=tkinter.RIGHT,
        padx=10
    )
    info_window.update()

    # App Info

    tkinter.Label(
        main_frame,
        text="PwrStat GUI",
        font=(font, 20),
        fg=highlight,
        bg=darkest,
        height=2
    ).pack()
    tkinter.Label(
        main_frame,
        text=(
            name + "\n" +
            f"Created {created}\n" +
            f"Version {version}\n" +
            f"Last Updated {updated}\n"
        ),
        font=(font, 12),
        fg=light,
        bg=darkest,
        height=5
    ).pack()
    info_window.update()

    # UPS Info

    ups_info_raw = (
        subprocess.run(["sudo", "pwrstat", "-status"],
        capture_output=True, text=True).stdout
    ).strip()

    tkinter.Label(
        main_frame,
        text="UPS Information",
        font=(font, 20),
        fg=highlight,
        bg=darkest,
        height=2
    ).pack()
    info_window.update()

    if "Properties" in ups_info_raw:

        properties_raw = ups_info_raw.split("\n\n")[1].split("\n")
        properties = [
            [property_raw.split(". ")[0].strip().replace(".", ""),
            property_raw.split(". ")[1].strip()]
            for property_raw in properties_raw[1:]
        ]

        for property in properties:
            tkinter.Label(
                main_frame,
                text=f"{property[0]}: {property[1]}",
                font=(font, 12),
                fg=light,
                bg=darkest,
                height=1
            ).pack()
            info_window.update()

    else:

        tkinter.Label(
            main_frame,
            text=(
                "No UPS info available,\n" +
                "check connection using lsusb."
            ),
            font=(font, 12),
            fg=light,
            bg=darkest,
            height=7
        ).pack()
        info_window.update()

    # Window Mainloop

    info_window.mainloop()

def open_settings():

    # Root Window

    global window

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

    settings_window = tkinter.Toplevel(window)
    settings_window.grab_set()
    settings_window.geometry("750x500")
    settings_window.minsize(width=800, height=600)
    settings_window.maxsize(width=800, height=600)
    settings_window.configure(bg=darkest)
    settings_window.title("PwrStat GUI Settings")

    main_frame = tkinter.Frame(settings_window, width=800, height=550, bg=darkest)
    main_frame.pack_propagate(False)
    main_frame.pack(fill=tkinter.BOTH, expand=True)
    footer_frame = tkinter.Frame(settings_window, width=800, height=50, bg=dark)
    footer_frame.pack_propagate(False)
    footer_frame.pack(fill=tkinter.BOTH, expand=True)
    settings_window.update()

    # Footer Frame Buttons

    tkinter.Button(
        footer_frame,
        text="Close",
        font=(font, 12),
        width=10,
        height=1,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=settings_window.destroy
    ).pack(
        side=tkinter.RIGHT,
        padx=10
    )

    tkinter.Button(
        footer_frame,
        text="Reset Settings",
        font=(font, 12),
        width=15,
        height=1,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=lambda: reset_settings(settings_window)
    ).pack(
        side=tkinter.RIGHT,
        padx=10
    )

    # Settings Title

    tkinter.Label(
        main_frame,
        text="Settings",
        font=(font, 20),
        fg=highlight,
        bg=darkest,
        height=2
    ).pack()
    settings_window.update()

    # Settings Frames

    color_set_frame = tkinter.Frame(
        main_frame,
        width=800, 
        height=50, 
        bg=darken_color(darkest)
    )
    color_set_frame.pack_propagate(False)
    color_set_frame.pack(fill=tkinter.BOTH, expand=True) # Actual height > 50

    font_frame = tkinter.Frame(
        main_frame,
        width=800,
        height=50,
        bg=darkest
    )
    font_frame.pack_propagate(False)
    font_frame.pack(fill=tkinter.BOTH, expand=True)

    log_path_frame = tkinter.Frame(
        main_frame,
        width=800,
        height=50,
        bg=darken_color(darkest)
    )
    log_path_frame.pack_propagate(False)
    log_path_frame.pack(fill=tkinter.BOTH, expand=True)

    log_toggle_frame = tkinter.Frame(
        main_frame,
        width=800,
        height=50,
        bg=darkest
    )
    log_toggle_frame.pack_propagate(False)
    log_toggle_frame.pack(fill=tkinter.BOTH, expand=True)

    sample_interval_frame = tkinter.Frame(
        main_frame,
        width=800,
        height=50,
        bg=darken_color(darkest)
    )
    sample_interval_frame.pack_propagate(False)
    sample_interval_frame.pack(fill=tkinter.BOTH, expand=True)

    settings_window.update()

    # Color Set Setting

    tkinter.Label(
        color_set_frame,
        text="Color Set",
        font=(font, 14),
        fg=highlight,
        bg=darken_color(darkest),
        width=8,
        height=1
    ).pack(
        side=tkinter.LEFT,
        padx=5
    )

    tkinter.Button(
        color_set_frame,
        text=(
            "Darkest\n" +
            darkest + "\n" +
            "Default:\n#000712"
        ),
        font=(font, 10),
        width=12,
        height=4,
        fg=light,
        bg=darkest,
        activeforeground=highlight,
        activebackground=light,
        command=lambda: choose_color(settings_window, "darkest")
    ).pack(
        side=tkinter.LEFT,
        padx=5
    )

    tkinter.Button(
        color_set_frame,
        text=(
            "Dark\n" +
            dark + "\n" +
            "Default:\n#001429"
        ),
        font=(font, 10),
        width=12,
        height=4,
        fg=light,
        bg=dark,
        activeforeground=highlight,
        activebackground=light,
        command=lambda: choose_color(settings_window, "dark")
    ).pack(
        side=tkinter.LEFT,
        padx=5
    )

    tkinter.Button(
        color_set_frame,
        text=(
            "Medium\n" +
            medium + "\n" +
            "Default:\n#001F3D"
        ),
        font=(font, 10),
        width=12,
        height=4,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=lambda: choose_color(settings_window, "medium")
    ).pack(
        side=tkinter.LEFT,
        padx=5
    )

    tkinter.Button(
        color_set_frame,
        text=(
            "Light\n" +
            light + "\n" +
            "Default:\n#2C4F70"
        ),
        font=(font, 10),
        width=12,
        height=4,
        fg=darkest,
        bg=light,
        activeforeground=highlight,
        activebackground=light,
        command=lambda: choose_color(settings_window, "light")
    ).pack(
        side=tkinter.LEFT,
        padx=5
    )

    tkinter.Button(
        color_set_frame,
        text=(
            "Highlight\n" +
            highlight + "\n" +
            "Default:\n#FFC300"
        ),
        font=(font, 10),
        width=12,
        height=4,
        fg=darkest,
        bg=highlight,
        activeforeground=highlight,
        activebackground=light,
        command=lambda: choose_color(settings_window, "highlight")
    ).pack(
        side=tkinter.LEFT,
        padx=5
    )

    settings_window.update()

    # Window Mainloop

    settings_window.mainloop()

def reset_settings(settings_window):
    
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
    sample_interval = 1

    # Resetting Settings File

    with open("data/settings.txt", "w") as file:
        file.write(
            """color-set: #000712, #001429, #001F3D, #2C4F70, #FFC300
            font: Garamond
            log-path: NOT SET
            sample-interval: 1""".replace("    ", "")
        )

    # Reopen Settings Window

    settings_window.destroy()
    open_settings()


# Main Function

def main():

    # Root Window

    global window

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

    with open("data/info.txt", "r") as file:
        info_raw = file.read().split("\n")
    name = info_raw[0].replace("Name: ", "")
    created = info_raw[1].replace("Created: ", "")
    version = info_raw[2].replace("Version: ", "")
    updated = info_raw[3].replace("Updated: ", "")

    with open("data/settings.txt", "r") as file:
        settings_raw = file.read().split("\n")
    color_set = settings_raw[0].replace("color-set: ", "").split(", ")
    darkest = color_set[0]
    dark = color_set[1]
    medium = color_set[2]
    light = color_set[3]
    highlight = color_set[4]
    font = settings_raw[1].replace("font: ", "")
    log_path = settings_raw[2].replace("log-path: ", "")
    font = int(settings_raw[3].replace("sample-interval: ", ""))

    # Window Setup

    window = tkinter.Tk()
    window.protocol("WM_DELETE_WINDOW", exit)
    window.geometry("800x600")
    window.minsize(width=800, height=600)
    window.maxsize(width=800, height=600)
    window.configure(bg=darkest)
    window.title("PwrStat GUI")
    window.iconphoto(True, ImageTk.PhotoImage(Image.open("images/logo.png")))
    window.update()

    setproctitle.setproctitle("pwrstat-gui")

    # Starting Screen

    tkinter.Label(
        window,
        text="PwrStat GUI",
        font=(font, 20),
        fg=highlight,
        bg=darkest,
        height=2
    ).pack()
    tkinter.Label(
        window,
        text=(
            "A graphical user interface for PowerPanel on Linux.\n" +
            "Created by Liam Ralph.\n" +
            "v0.0\n"
        ),
        font=(font, 10),
        fg=light,
        bg=darkest,
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
            font=(font, 20),
            fg="#AA0000",
            bg=darkest,
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
        font=(font, 12),
        width=10,
        height=2,
        fg=light,
        bg=dark,
        activeforeground=highlight,
        activebackground=medium,
        command=lambda: clicked.set(True)
    )
    button.pack()
    window.update()

    button.wait_variable(clicked)
    for child in window.winfo_children():
        child.destroy()

    # Home Screen

    main_frame = tkinter.Frame(window, width=800, height=550, bg=darkest)
    main_frame.pack_propagate(False)
    main_frame.pack(fill=tkinter.BOTH, expand=True)
    footer_frame = tkinter.Frame(window, width=800, height=50, bg=dark)
    footer_frame.pack_propagate(False)
    footer_frame.pack(fill=tkinter.BOTH, expand=True)
    window.update()

    # Footer Frame Buttons

    tkinter.Button(
        footer_frame,
        text="Close",
        font=(font, 12),
        width=10,
        height=1,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=window.destroy
    ).pack(
        side=tkinter.RIGHT,
        padx=10
    )
    tkinter.Button(
        footer_frame,
        text="Info",
        font=(font, 12),
        width=10,
        height=1,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=open_info
    ).pack(
        side=tkinter.RIGHT,
        padx=10
    )
    tkinter.Button(
        footer_frame,
        text="Settings",
        font=(font, 12),
        width=10,
        height=1,
        fg=light,
        bg=medium,
        activeforeground=highlight,
        activebackground=light,
        command=open_settings
    ).pack(
        side=tkinter.RIGHT,
        padx=10
    )
    window.update()

    # Window Mainloop

    window.mainloop()


# Run Main Function

if __name__ == "__main__":
    main()