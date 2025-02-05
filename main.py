# Created by Liam Ralph
# https://github.com/Liam-Ralph
# Shared under the MIT License (see LICENSE file)


# Imports

import os
import multiprocessing
import tkinter


# Colors

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

    # Window Mainloop

    window.mainloop()


# Run Main Function
main()