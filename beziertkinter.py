import tkinter as tk
import numpy as np

# empty window
root = tk.Tk()
root.title("Bezier Curve")

canvas = tk.Canvas(root, width=500, height=700)
canvas.pack()

# empty global array to store starting points
start = []

# generate t values
ts = [t / 50 for t in range(101)]

lines = []

# this function calculates the points on the Bézier curve recursively for any parameter t and returns them
def calc_point(p1, p2, p3, p4, t):
    # transform vectors to numpy arrays for easier scalar operations
    np1 = np.array(p1)
    np2 = np.array(p2)
    np3 = np.array(p3)
    np4 = np.array(p4)
    # t is equivalent to the distance traveled on the Bézier curve from control point P1 to P4
    if t < 0.01:
        # if t is smaller than this threshold we can just return P1 as changes are likely not noticeable for the
        # given screen resolutions
        return p1
    else:
        # calculate mid points
        p12 = (np1 + np2) / 2
        p23 = (np2 + np3) / 2
        p34 = (np3 + np4) / 2

        p123 = (p12 + p23) / 2
        p234 = (p23 + p34) / 2

        q = (p123 + p234) / 2

        # calculate point on the Bézier curve according to the formula in the lecture and transform back to python array
        return ((1 - t) ** 3 * np1 + 3 * t * (1 - t) ** 2 * p12 + 3 * t ** 2 * (1 - t) * p123 + t ** 3 * q).tolist()


# calculates and returns an array with points on the Bézier curve
def bezier(p1, p2, p3, p4, ts):
    # empty array to store points on the Bézier curve
    points = []
    # iterate through t values and calculate the point on the curve
    for t in ts:
        # add the calculated points to the empty array
        points.append(calc_point(p1, p2, p3, p4, t))
    return points


# helper method to extract starting points from rectangles
def get_p_from_rect():
    # explicitly assign points for easy access
    p1 = canvas.coords(start[0])
    p2 = canvas.coords(start[1])
    p3 = canvas.coords(start[2])
    p4 = canvas.coords(start[3])
    return [get_center(p1), get_center(p2), get_center(p3), get_center(p4)]


def get_center(p):
    return [(p[2] + p[0]) / 2, (p[3] + p[1]) / 2]


def store_bezier_in_array():
    p1, p2, p3, p4 = get_p_from_rect()
    global points
    points = bezier(p1, p2, p3, p4, ts)


def draw_bezier():
    global lines
    # iterate through calculated points and draw a line between them
    for x in range(len(points) - 1):
        l = canvas.create_line(points[x][0], points[x][1], points[x + 1][0], points[x + 1][1], fill="black")
        lines.append(l)


def on_click(event):
    rect = get_closest_rect(event.x, event.y)
    global drag_point
    drag_point = rect


def on_drag(event):
    if drag_point is not None:
        x, y = get_center(canvas.coords(drag_point))
        for l in lines:
            canvas.delete(l)
        canvas.move(drag_point, event.x - x, event.y - y)
        store_bezier_in_array()
        draw_bezier()

def get_closest_rect(x, y):
    for r in start:
        center = get_center(canvas.coords(r))
        if abs(x - center[0]) < 8 and abs(y - center[1]) < 8:
            return r

def place_points(event):
    global start
    if len(start) <= 4:
        rect = canvas.create_rectangle(event.x - 4, event.y - 4, event.x + 4, event.y + 4, fill="black")
        start.append(rect)
        if (len(start) == 4):
            canvas.unbind("<Button-1>")
            for p in start:
                canvas.tag_bind(p, "<Button-1>", on_click)
                canvas.tag_bind(p, "<B1-Motion>", on_drag)
            store_bezier_in_array()
            draw_bezier()


if __name__ == '__main__':
    canvas.bind("<Button-1>", place_points)

    root.mainloop()
