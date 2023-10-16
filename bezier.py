from graphics import *
import numpy as np
import time

# empty window
win = GraphWin("Bezier Curve", 500, 700)

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


def rect_clicked(rects, x, y):
    for r in rects:
        if r.getP1().x-20 <= x <= r.getP2().x-20:
            if r.getP2().y-20 <= y <= r.getP1().y+20:
                return r
    return None


# helper method to extract starting points from rectangles
def get_p_from_rect():
    # explicitly assign points for easy access
    p1 = (start[0].getCenter().x, start[0].getCenter().y)
    p2 = (start[1].getCenter().x, start[1].getCenter().y)
    p3 = (start[2].getCenter().x, start[2].getCenter().y)
    p4 = (start[3].getCenter().x, start[3].getCenter().y)
    return p1, p2, p3, p4


def store_bezier_in_array():
    p1, p2, p3, p4 = get_p_from_rect()
    global points
    points = bezier(p1, p2, p3, p4, ts)

def undraw_bezier():
    global lines
    for l in lines:
        l.undraw()
    lines = []


def draw_bezier():
    global lines
    undraw_bezier()
    # iterate through calculated points and draw a line between them
    for x in range(len(points) - 1):
        l = Line(Point(points[x][0], points[x][1]), Point(points[x + 1][0], points[x + 1][1]))
        lines.append(l)
        l.draw(win)


def motion(event):
    if len(start) == 4:
        x, y = event.x, event.y
        clicked_rect = rect_clicked(start, x, y)
        clicked_rect.move(abs(x - clicked_rect.getCenter().x), abs(y - clicked_rect.getCenter().y))
        store_bezier_in_array()
        draw_bezier()
        if clicked_rect is not None:
            #clicked_rect.move(abs(x - clicked_rect.getCenter().x), abs(y - clicked_rect.getCenter().y))
            store_bezier_in_array()
            draw_bezier()


if __name__ == '__main__':
    # Override size and position of the GraphWin.
    w, h = 500, 700  # Width and height.
    x, y = 20, 20  # Screen position.
    win.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
    win.bind('<B1-Motion>', motion)

    # register first 4 clicks to establish the starting points and add them to array
    for x in range(0, 4):
        p = win.getMouse()
        # add offset to the rectangle, so it is centered around the clicked position
        p.x = p.x - 3
        p.y = p.y + 3
        rect = Rectangle(p, Point(p.x + 6, p.y - 6))
        rect.setFill("white")
        rect.draw(win)
        start.append(rect)

    # call bezier function and store them
    store_bezier_in_array()
    draw_bezier()

    # last_frame_time = 0
    # while True:
    #     current_time = time.time()
    #     dt = current_time - last_frame_time
    #     last_frame_time = current_time
    #
    #     sleepTime = 1. / 60 - (current_time - last_frame_time)
    #     if sleepTime > 0:
    #         time.sleep(sleepTime)
    #
    #     points = bezier(p1, p2, p3, p4, ts)

    while True:
        win.getMouse()

    # win.getMouse()
    # win.close()
