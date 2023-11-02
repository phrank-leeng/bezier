import math
import tkinter as tk
from tkinter import *

# empty window
root = tk.Tk()
root.title("DreamCatcher")
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

level = 6
limited_lvl = level
lvlStr = StringVar()

circle = None
# midpoint of circle frame
m_circle = [250, 200]

# empty canvas
canvas = tk.Canvas(left_f, width=550, height=700, bg='gray55')
canvas.place(x=0, y=0)
canvas.pack()

dynamic_elems = []

length_vane = 40
D1 = 14
W1 = 3


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
    global dynamic_elems
    for e in dynamic_elems:
        canvas.delete(e)
    dynamic_elems = []
    RC_C()
    RC_B_1()
    RC_B_2()
    RC_B_3()


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
    # make dendrites stop spreading after level 6
    return fibonacci(level + 2) if level < 7 else fibonacci(6 + 2)


def point_unit_circle(p, r, theta):
    # negate sin because y coordinates are reversed in tkinter
    return [p[0] + r * math.cos(math.radians(theta)), p[1] + r * -math.sin(math.radians(theta))]


def get_color(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def get_feather_color():
    return get_color(145, 168, 208)


def get_flower_color():
    return get_color(247, 202, 201)


def draw_line(p1, p2, color, w):
    return canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=w)


def RC_C():
    if circle is None:
        # draw the outer circle
        canvas.create_oval(100, 50, 400, 350, outline='white', width=3)

    # red horizontal line down the middle for debugging purposes
    # canvas.create_line(250, 50, 250, 350, fill='red')

    # calculate the angle between dendrites
    angle = 360 / num_dendrites()
    # loop to make dendrites spread
    theta = 0
    for i in range(0, num_dendrites()):
        theta += angle
        RC_A(point_unit_circle(m_circle, 150, theta), theta + 180, 0, theta + 180)


def RC_A(start, theta, rec_depth, theta_0):
    if theta + 30 < theta_0 + 90 or theta - 30 > theta_0 - 90:
        if rec_depth < limited_lvl:
            h1_factor = 0
            for i in range(0, limited_lvl):
                h1_factor += pow(0.75, i)
            h_n = 150 / h1_factor * pow(0.75, rec_depth)
            # if rec_depth is uneven the radius changes to the hypotenuse instead of the opposite
            r = h_n if rec_depth % 2 == 0 else h_n / math.sin(math.radians(180 - 90 - 30))
            end = point_unit_circle(start, r, theta)
            color = get_color(135 + rec_depth * 10, 188 + rec_depth * 5, 240)
            dynamic_elems.append(draw_line(start, end, color, 10 - rec_depth * 2))
            # left branch
            RC_A(end, theta - 30, rec_depth + 1, theta_0)
            # right branch
            RC_A(end, theta + 30, rec_depth + 1, theta_0)


def RC_B_1():
    # create feathers
    if level > 5:
        draw_shafts()


def draw_shafts():
    for i in range(0, 3):
        p = point_unit_circle(m_circle, 150, 225 + i * 45)
        dynamic_elems.append(canvas.create_line(p[0], p[1], p[0], p[1] + 225, fill=get_feather_color(), width=5))
        draw_vanes([p[0], p[1] + 67.5], 0)


def draw_vanes(start, rec_depth):
    # draw 8 vanes
    if rec_depth < 8:
        p_right = point_unit_circle(start, length_vane, 30)
        p_left = point_unit_circle(start, length_vane, 150)
        width = 5
        dynamic_elems.append(draw_line(start, p_right, get_feather_color(), width))
        dynamic_elems.append(draw_line(start, p_left, get_feather_color(), width))
        draw_vanes([start[0], start[1] + 157.5 / 7], rec_depth + 1)


def RC_B_2():
    # create fractal flowers recursively
    if level > 6:
        for i in range(0, 3):
            p = point_unit_circle(m_circle, 150, 225 + i * 45)
            p = [p[0], p[1] + 67.5]
            draw_flowers(p, 0)


def draw_flowers(start, rec_depth):
    if rec_depth < 8:
        m_flower = length_vane * 2 / 3
        p_right = point_unit_circle(start, m_flower, 30)
        dynamic_elems.append(draw_circle(p_right, D1 / 2, get_flower_color(), W1))
        p_left = point_unit_circle(start, m_flower, 150)
        dynamic_elems.append(draw_circle(p_left, D1 / 2, get_flower_color(), W1))
        draw_flowers([start[0], start[1] + 157.5 / 7], rec_depth + 1)


def draw_circle(p, r, color, width):
    return canvas.create_oval(p[0] - r, p[1] - r, p[0] + r, p[1] + r, outline=color, width=width)


def RC_B_3():
    # create fractal petals recursively
    if level > 7:
        for i in range(0, 3):
            p = point_unit_circle(m_circle, 150, 225 + i * 45)
            p = [p[0], p[1] + 67.5]
            draw_petals(p, 0)


def draw_petals(start, rec_depth):
    if rec_depth < 8:
        m_flower = length_vane * 2 / 3
        p_right = point_unit_circle(start, m_flower, 30)
        draw_petal(p_right, 0)
        p_left = point_unit_circle(start, m_flower, 150)
        draw_petal(p_left, 0)
        draw_petals([start[0], start[1] + 157.5 / 7], rec_depth + 1)


def draw_petal(p, rec_depth):
    if rec_depth < 6:
        D2 = D1 * 0.5
        r = D2 / 2
        W2 = W1 - 2
        m_petal = point_unit_circle(p, D2, 60 * rec_depth)
        draw_circle(m_petal, r, get_flower_color(), W2)
        draw_petal(p, rec_depth + 1)


# main method
if __name__ == '__main__':
    RC_C()
    refresh()
    root.mainloop()
