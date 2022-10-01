import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import random
import numpy as np
import time
import math

width, height = 800, 800
size = 0.5
left = 1
right = 2
bot = 4
top = 8
drawer = None
point_1 = [0, 0]
point_2 = [0, 0]
c = 0
shapes = []
scale = 1

#


def get_random_color():
    return [
        random.uniform(0, 1),
        random.uniform(0, 1),
        random.uniform(0, 1),
        1
    ]

color = get_random_color()
def key_callback(window, key, scancode, action, mods):
    global scale
    if (action == glfw.REPEAT or action == glfw.PRESS):
        if key == glfw.KEY_UP:
            scale += 0.05
        if key == glfw.KEY_DOWN:
            scale -= 0.05
        if key == glfw.KEY_C:
            color = get_random_color()


def mouse_button_callback(window, button, action, mods):
    global point_1, point_2, c
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        pos = glfw.get_cursor_pos(window)
        coords = [(pos[0] - width / 2) / (width / 2), (height / 2 - pos[1]) / (height / 2)]
        if c == 0:
            point_1 = coords
            print('p1', point_1)
            c += 1
        elif c == 1:
            point_2 = coords
            print('p2', point_2)
            c = 0

class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self):
        glBegin(GL_LINES)  # ?
        glVertex2f(*self.point_1)
        glVertex2f(*self.point_2)
        glEnd()


class Drawer:
    def __init__(self, size):
        self.min_x = -size / 2
        self.max_x = size / 2
        self.min_y = -size / 2
        self.max_y = size / 2
        self.points = [
            (self.min_x, self.min_y),
            (self.max_x, self.min_y),
            (self.max_x, self.max_y),
            (self.min_x, self.max_y)
        ]

    def draw(self):
        glBegin(GL_POLYGON)
        for point in self.points:
            glColor3f(0, 0, 1)
            glVertex2f(*point)
        glEnd()


def vcode(point, drawer):
    code = 0
    if point[0] < drawer.min_x:
        code += left
    if point[0] > drawer.max_x:
        code += right
    if point[1] < drawer.min_y:
        code += bot
    if point[1] > drawer.max_y:
        code += top
    return code


def cohen_sutherland(drawer, first, second):
    code_first = vcode(first, drawer)
    code_second = vcode(second, drawer)
    code = 0

    while code_first | code_second:
        if code_first & code_second:
            return -1

        if code_first:
            code = code_first
            c = first
        else:
            code = code_second
            c = second

        if code & left:
            c[1] += (first[1] - second[1]) * (drawer.min_x - c[0]) / \
                    (first[0] - second[0])
            c[0] = drawer.min_x
        elif code & right:
            c[1] += (first[1] - second[1]) * (drawer.max_x - c[0]) / \
                    (first[0] - second[0])
            c[0] = drawer.max_x
        elif code & bot:
            c[0] += (first[0] - second[0]) * (drawer.min_y - c[1]) / \
                    (first[1] - second[1])
            c[1] = drawer.min_y
        elif code & top:
            c[0] += (first[0] - second[0]) * (drawer.max_y - c[1]) / \
                    (first[1] - second[1])
            c[1] = drawer.max_y

        if code == code_first:
            code_first = vcode(first, drawer)
        else:
            code_second = vcode(second, drawer)

    return 0


def display(window):
    global size, color
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glScale(scale, scale, scale)

    drawer.draw()

    line = Line(point_1, point_2)
    glColor3f(*color)
    line.draw()

    line_inner = Line(point_1.copy(), point_2.copy())
    glColor3f(0, 1, 0)
    if cohen_sutherland(drawer, line_inner.point_1, line_inner.point_2) != -1:
        line_inner.draw()

    glfw.swap_buffers(window)
    glfw.poll_events()


def main():
    global drawer, lines, width, height
    if not glfw.init():
        return
    window = glfw.create_window(width, height, "Lab5", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    drawer = Drawer(size)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


main()