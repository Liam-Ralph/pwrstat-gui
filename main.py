# Created by Liam Ralph
# https://github.com/Liam-Ralph
# Shared under the MIT License (see LICENSE file)


# Imports

import os
import setproctitle
import subprocess
import time
import tkinter


# Variables

darkest = "#000712"
dark = "#001429"
medium = "#001F3D"
light = "#2C4F70"
highlight = "#FFC200"
off_white = "#C0C0C0"
medium_grey = "#8C8C8C"


# Functions
# Alphabetical order

def open_info():

    # Info Window Setup

    info_window = tkinter.Tk()
    info_window.geometry("500x500")
    info_window.minsize(width=500, height=500)
    info_window.maxsize(width=500, height=500)
    info_window.configure(bg=darkest)
    info_window.title("PwrStat GUI Info")

    main_frame = tkinter.Frame(info_window, width=500, height=450, bg=darkest)
    main_frame.pack_propagate(False)
    main_frame.pack(fill=tkinter.BOTH, expand=True)
    footer_frame = tkinter.Frame(info_window, width=500, height=50, bg=dark)
    main_frame.pack_propagate(False)
    footer_frame.pack(fill=tkinter.BOTH, expand=True)
    info_window.update()

    # Close Window Button

    tkinter.Button(
        footer_frame,
        text="Close",
        font=("Garamond", 12),
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
        font=("Arial", 20),
        fg=highlight,
        bg=darkest,
        height=2
    ).pack()
    tkinter.Label(
        main_frame,
        text=(
            "Liam Ralph\n" +
            "Created March 2025\n" +
            "Version 0.0\n" +
            "Last Updated March 2025\n"
        ),
        font=("Arial", 12),
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
        font=("Arial", 20),
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
                font=("Arial", 12),
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
            font=("Arial", 12),
            fg=light,
            bg=darkest,
            height=7
        ).pack()

        info_window.update()

def open_settings():

    # Settings Window Setup

    settings_window = tkinter.Tk()
    settings_window.geometry("500x500")
    settings_window.minsize(width=500, height=500)
    settings_window.maxsize(width=500, height=500)
    settings_window.configure(bg=darkest)
    settings_window.title("PwrStat GUI Settings")

    main_frame = tkinter.Frame(settings_window, width=500, height=450, bg=darkest)
    main_frame.pack(fill=tkinter.BOTH, expand=True)
    footer_frame = tkinter.Frame(settings_window, width=500, height=50, bg=dark)
    footer_frame.pack(fill=tkinter.BOTH, expand=True)
    settings_window.update()

    # Close Window Button

    tkinter.Button(
        footer_frame,
        text="Close",
        font=("Garamond", 12),
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


# Main Function

def main():

    # Window Setup

    window = tkinter.Tk()
    window.geometry("500x500")
    window.minsize(width=500, height=500)
    window.maxsize(width=500, height=500)
    window.configure(bg=darkest)
    window.title("PwrStat GUI")
    window.update()

    setproctitle.setproctitle("PwrStat GUI")

    # Starting Screen

    tkinter.Label(
        window,
        text="PwrStat GUI",
        font=("Garamond", 20),
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
        font=("Garamond", 10),
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
            font=("Arial", 20),
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
        font=("Garamond", 12),
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

    main_frame = tkinter.Frame(window, width=500, height=450, bg=darkest)
    main_frame.pack(fill=tkinter.BOTH, expand=True)
    footer_frame = tkinter.Frame(window, width=500, height=50, bg=dark)
    footer_frame.pack(fill=tkinter.BOTH, expand=True)
    window.update()

    # Footer Frame Buttons

    tkinter.Button(
        footer_frame,
        text="Close",
        font=("Garamond", 12),
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
        text="Settings",
        font=("Garamond", 12),
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
    tkinter.Button(
        footer_frame,
        text="Info",
        font=("Garamond", 12),
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
    window.update()

    # Window Mainloop

    window.mainloop()


# Run Main Function

main()