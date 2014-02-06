#!/usr/bin/env python

import Tkinter as tk
from tkFileDialog import askopenfilename
from subprocess import call


root = tk.Tk()


def openfile():
   filename = askopenfilename(parent=root)
   call(['./convert.py', filename])

def setup_gui():
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=openfile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)

def run():
    setup_gui()
    root.mainloop()


if __name__ == '__main__':
    run()
