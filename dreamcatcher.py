import math
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
limited_lvl = level
lvlStr = StringVar()

# midpoint of circle frame
m_circle = [250, 200]

# empty canvas
canvas = tk.Canvas(left_f, width=550, height=700, bg='gray55')
canvas.place(x=0, y=0)
canvas.pack()

branches = []


def dec_lvl():
    global level
    if level > 1:
        level -= 1
        refresh()


def inc_lvl():
    global level
    if level < 8:
        level += 1
        refresh()


def refresh():
    global limited_lvl
    limited_lvl = level if level < 7 else 6
    lvlStr.set(level)
    global branches
    for b in branches:
        canvas.delete(b)
    branches = []
    RC_C()


level_label = Label(right_f, textvariable=lvlStr)
lvlStr.set(level)
level_label.pack()

minus = Button(right_f, text='-', command=dec_lvl)
plus = Button(right_f, text='+', command=inc_lvl)

minus.pack(side=LEFT)
plus.pack(side=RIGHT, padx=10)


def fibonacci(n):
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


def num_dendrites():
    return fibonacci(level + 2)


def point_unit_circle(p, r, theta):
    return [p[0] + r * math.cos(math.radians(theta)), p[1] + r * math.sin(math.radians(theta))]


def RC_C():
    # draw the outer circle
    canvas.create_oval(100, 50, 400, 350, outline='white', width=3)

    # calculate the angle between dendrites
    angle = 360 / num_dendrites()
    # loop to make dendrites spread
    for i in range(0, num_dendrites()):
        RC_A(m_circle, 0 + angle * i, 0)


def RC_A(start, theta, rec_depth):
    if rec_depth < level and rec_depth < 5:
        h1 = 150 / (1 + 0.75 * (limited_lvl - 1))
        r = h1 * pow(0.75, rec_depth)
        end = point_unit_circle(start, r, theta)
        color = "#%02x%02x%02x" % (135 + rec_depth * 10, 188 + rec_depth * 5, 240)
        branches.append(canvas.create_line(start[0], start[1], end[0], end[1], fill=color, width=10 - rec_depth * 2))
        RC_A(end, theta, rec_depth + 1)


# main method
if __name__ == '__main__':
    RC_C()
    root.mainloop()
