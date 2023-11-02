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

# divide window into two parts, one for the dream catcher and the other for the buttons
left_f = Frame(root, width=550, height=700)
left_f.pack(side='left')
right_f = Frame(root, width=250, height=700)
right_f.pack(side='right')

level = 1
limited_lvl = level
lvlStr = StringVar()

# store circle frame object once created
circle = None
# midpoint of circle frame
m_circle = [250, 200]

# empty canvas
canvas = tk.Canvas(left_f, width=550, height=700, bg='gray55')
canvas.place(x=0, y=0)
canvas.pack()

# array to store dynamically generated elements to erase them when de-/increasing level
dynamic_elems = []

# properties for feathers/flowers/petals
length_vane = 40
D1 = 14
W1 = 3


# decreases level
def dec_lvl():
    global level
    if level > 1:
        level -= 1
        refresh()


# increases level
def inc_lvl():
    global level
    if level < 8:
        level += 1
        refresh()


# resets the level label above the buttons and draw dream catcher according to level
def refresh():
    global limited_lvl
    limited_lvl = level if level < 7 else 6
    lvlStr.set(level)
    # erase all previously drawn elements first
    global dynamic_elems
    for e in dynamic_elems:
        canvas.delete(e)
    dynamic_elems = []
    # call all approaches
    RC_C()
    RC_B_1()
    RC_B_2()
    RC_B_3()


# generate right side of window
level_label = Label(right_f, textvariable=lvlStr)
lvlStr.set(level)
level_label.pack()

minus = Button(right_f, text='-', command=dec_lvl)
plus = Button(right_f, text='+', command=inc_lvl)

minus.pack(side=LEFT)
plus.pack(side=RIGHT, padx=10)


def fibonacci(n):
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


# calculates the number of dendrites the dream catcher should have
def num_dendrites():
    # make dendrites stop spreading after level 6
    return fibonacci(level + 2) if level < 7 else fibonacci(6 + 2)


# calculates any point on a circle given the midpoint, radius and the angle theta
def point_on_circle(p, r, theta):
    # negate sin because y coordinates are reversed in tkinter
    return [p[0] + r * math.cos(math.radians(theta)), p[1] + r * -math.sin(math.radians(theta))]


# helper method converts RGB to hex format because tkinter takes hex format
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
        # draw the outer circle if it does not exist yet
        canvas.create_oval(100, 50, 400, 350, outline='white', width=3)

    # red horizontal line down the middle for debugging purposes
    # canvas.create_line(250, 50, 250, 350, fill='red')

    # calculate the angle between dendrites
    angle = 360 / num_dendrites()
    # loop to make dendrites spread
    theta = 0
    for i in range(0, num_dendrites()):
        theta += angle
        # call RC_A approach to calculate branches and draw them
        RC_A(point_on_circle(m_circle, 150, theta), theta + 180, 0, theta + 180)


# recursively calculates branches on dendrites
def RC_A(start, theta, rec_depth, theta_0):
    # check if the branch will be pruned, if yes no need to calculate
    if theta + 30 < theta_0 + 90 or theta - 30 > theta_0 - 90:
        # branch depth
        if rec_depth < limited_lvl:
            h1_factor = 0
            # calculate the factor to solve the formula 150 = h1_factor * h1
            for i in range(0, limited_lvl):
                # for example for 3 branches, h3 = 0.75 * h2 = 0.75 * 0.75 * h1
                h1_factor += pow(0.75, i)
            # calculate h_n according to rec_depth
            h_n = 150 / h1_factor * pow(0.75, rec_depth)
            # if rec_depth is uneven the radius changes to the hypotenuse instead of the opposite
            r = h_n if rec_depth % 2 == 0 else h_n / math.sin(math.radians(180 - 90 - 30))
            # calculate end point of branch
            end = point_on_circle(start, r, theta)
            color = get_color(135 + rec_depth * 10, 188 + rec_depth * 5, 240)
            # draw branch
            dynamic_elems.append(draw_line(start, end, color, 10 - rec_depth * 2))
            # continue recursion for left branch
            RC_A(end, theta - 30, rec_depth + 1, theta_0)
            # continue recursion for right branch
            RC_A(end, theta + 30, rec_depth + 1, theta_0)


def RC_B_1():
    # create feathers
    if level > 5:
        draw_feathers()


def draw_feathers():
    # iterate through all 3 feathers/starting points
    for i in range(0, 3):
        # find starting points on the circle
        p = point_on_circle(m_circle, 150, 225 + i * 45)
        # draw straight vertical lines from points
        dynamic_elems.append(canvas.create_line(p[0], p[1], p[0], p[1] + 225, fill=get_feather_color(), width=5))
        draw_vanes([p[0], p[1] + 67.5], 0)


# draws 8 vanes down the starting point
def draw_vanes(start, rec_depth):
    if rec_depth < 8:
        p_right = point_on_circle(start, length_vane, 30)
        p_left = point_on_circle(start, length_vane, 150)
        width = 5
        dynamic_elems.append(draw_line(start, p_right, get_feather_color(), width))
        dynamic_elems.append(draw_line(start, p_left, get_feather_color(), width))
        draw_vanes([start[0], start[1] + 157.5 / 7], rec_depth + 1)


def RC_B_2():
    # create fractal flowers recursively
    if level > 6:
        for i in range(0, 3):
            # calculate the intersection between first feather and vanes
            p = point_on_circle(m_circle, 150, 225 + i * 45)
            p = [p[0], p[1] + 67.5]
            draw_flowers(p, 0)


# creates flowers on left and right vane recursively given the intersection point between feather and vanes
def draw_flowers(start, rec_depth):
    # draw 8 flowers for every feather
    if rec_depth < 8:
        # radius of mid-point
        m_flower = length_vane * 2 / 3
        # find exact mid-point
        p_right = point_on_circle(start, m_flower, 30)
        dynamic_elems.append(draw_circle(p_right, D1 / 2, get_flower_color(), W1))
        # do the same for left flower
        p_left = point_on_circle(start, m_flower, 150)
        dynamic_elems.append(draw_circle(p_left, D1 / 2, get_flower_color(), W1))
        # next vane
        draw_flowers([start[0], start[1] + 157.5 / 7], rec_depth + 1)


def draw_circle(p, r, color, width):
    return canvas.create_oval(p[0] - r, p[1] - r, p[0] + r, p[1] + r, outline=color, width=width)


# creates 6 fractal petals recursively
def RC_B_3():
    if level > 7:
        # iterate through all 3 feathers/starting points again
        for i in range(0, 3):
            p = point_on_circle(m_circle, 150, 225 + i * 45)
            p = [p[0], p[1] + 67.5]
            draw_petals(p, 0)


# calculates intersection points between feather and vanes to draw petals
def draw_petals(start, rec_depth):
    if rec_depth < 8:
        # again calculate the mid-points of the flowers
        m_flower = length_vane * 2 / 3
        p_right = point_on_circle(start, m_flower, 30)
        # draw petals on the right flower
        draw_petal(p_right, 0)
        p_left = point_on_circle(start, m_flower, 150)
        # do same for left
        draw_petal(p_left, 0)
        # next vane
        draw_petals([start[0], start[1] + 157.5 / 7], rec_depth + 1)


# draws 6 petals around point p
def draw_petal(p, rec_depth):
    if rec_depth < 6:
        D2 = D1 * 0.5
        r = D2 / 2
        W2 = W1 - 2
        # increase angle according to recursion depth
        m_petal = point_on_circle(p, D2, 60 * rec_depth)
        # draw petal
        draw_circle(m_petal, r, get_flower_color(), W2)
        # next petal
        draw_petal(p, rec_depth + 1)


# main method
if __name__ == '__main__':
    RC_C()

    root.mainloop()
