import tkinter as tk
import numpy as np

# empty window
root = tk.Tk()
root.title("Bezier Curve")

# empty canvas
canvas = tk.Canvas(root, width=500, height=700)
canvas.pack()

# empty global array to store starting points P1, P2, P3, P4
start = []

# generate t values from 0 to 1 in 0.01 increments
ts = [t / 100 for t in range(101)]

# empty array to hold id for lines
lines = []


# calculates midpoints on the Bézier curve recursively for any parameter t and returns the final midpoint q
def calc_point(p, t):
    if len(p) == 1:
        return p[0]

    new_points = []

    # transform vectors to numpy arrays for easier scalar operation
    npp = np.array(p)
    for i in range(0, len(npp) - 1):
        new_points.append(((1 - t) * npp[i] + t * npp[i + 1]).tolist())

    return calc_point(new_points, t)


# calculates and returns an array with points on the Bézier curve
def bezier(p1, p2, p3, p4, ts):
    # empty array to store points on the Bézier curve
    points = []
    # iterate through t values and calculate the point on the curve
    for t in ts:
        # add the calculated points to the empty array
        points.append(calc_point([p1, p2, p3, p4], t))
    return points


# helper method to extract coordinates from rectangles
def get_p_from_rect():
    # explicitly assign points for easy access
    p1 = canvas.coords(start[0])
    p2 = canvas.coords(start[1])
    p3 = canvas.coords(start[2])
    p4 = canvas.coords(start[3])
    return [get_center(p1), get_center(p2), get_center(p3), get_center(p4)]


# helper method, returns center of the rectangles
def get_center(p):
    return [(p[2] + p[0]) / 2, (p[3] + p[1]) / 2]


# store multimediasystems points in the global points array
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


# select the closest rectangle on click
def on_click(event):
    rect = get_closest_rect(event.x, event.y)
    global drag_point
    drag_point = rect


# when a rectangle is dragged, recalculate and redraw Bézier curve
def on_drag(event):
    if drag_point is not None:
        x, y = get_center(canvas.coords(drag_point))
        global lines
        for l in lines:
            canvas.delete(l)
        lines = []
        canvas.move(drag_point, event.x - x, event.y - y)
        store_bezier_in_array()
        draw_bezier()


# needed for establishing clicked rectangle
def get_closest_rect(x, y):
    for r in start:
        center = get_center(canvas.coords(r))
        if abs(x - center[0]) < 8 and abs(y - center[1]) < 8:
            return r


# register the first 4 clicks to generate rectangles, then bind the click and motion event to dragging rectangles
def place_points(event):
    global start
    if len(start) <= 4:
        rect = canvas.create_rectangle(event.x - 4, event.y - 4, event.x + 4, event.y + 4, fill="black")
        start.append(rect)
        # once 4 clicks have been registered, rebind mouse clicks to start dragging operation
        if len(start) == 4:
            canvas.unbind("<Button-1>")
            for p in start:
                canvas.tag_bind(p, "<Button-1>", on_click)
                canvas.tag_bind(p, "<B1-Motion>", on_drag)
            # at 4 clicks calculate and draw the Bézier curve
            store_bezier_in_array()
            draw_bezier()


# main method
if __name__ == '__main__':
    canvas.bind("<Button-1>", place_points)

    root.mainloop()
