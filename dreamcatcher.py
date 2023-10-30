import tkinter as tk
from tkinter import *

# empty window
root = tk.Tk()
root.title("Bezier Curve")
w = 800  # width for the Tk root
h = 700  # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2) - 20

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

left_f = Frame(root, width=550, height=700)
left_f.pack(side='left')
right_f = Frame(root, width=250, height=700)
right_f.pack(side='right')

level = 1

# empty canvas
canvas = tk.Canvas(left_f, width=550, height=700, bg='gray55')
canvas.place(x=0, y=0)
canvas.pack()


def dec_lvl():
    global level
    if level > 1:
        level -= 1


def inc_lvl():
    global level
    if level < 8:
        level += 1


minus = Button(right_f, text='-', command=dec_lvl)
plus = Button(right_f, text='+', command=inc_lvl)

minus.pack(side=LEFT)
plus.pack(side=RIGHT, padx=20)


def fibonacci(n):
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


def num_dendrites():
    return fibonacci(level + 2)


def draw_dendrite():
    color = "#%02x%02x%02x" % (135, 188, 240)


# main method
if __name__ == '__main__':
    canvas.create_oval(100, 50, 400, 350, outline='white', width=3)

    print(num_dendrites())

    root.mainloop()
