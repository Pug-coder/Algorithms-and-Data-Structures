import glfw
from OpenGL.GL import *
from math import *
import random 

def get_random_color():
    return [
        random.uniform(0, 1),
        random.uniform(0, 1),
        random.uniform(0, 1),
        1
    ]

angleX = 0.0
angleY = 0.0
angleZ = 0.0
scale = 1
size = 0.5

tetta = pi / 5.1045
phi =  pi / 4
color = get_random_color()

newMatrix = [
    cos(tetta), -cos(phi) * sin(tetta), sin(tetta) * sin(phi), 0,
    -sin(tetta), -cos(phi) * cos(tetta), -sin(phi) * cos(tetta), 0,
    0, sin(tetta), cos(phi), 0,
    0, 0, 0, 1
]


def main():
    if not glfw.init():
        return
    window = glfw.create_window(700, 750, "Lab2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

mode = 0

def key_callback(window, key, scancode, action, mods):
    global angleZ, angleX, angleY, scale, mode, resolution, color
    if (action == glfw.REPEAT or action == glfw.PRESS):
        if key == glfw.KEY_LEFT:
            angleZ += 2
        if key == glfw.KEY_RIGHT:
            angleZ -= 2
        if key == glfw.KEY_A:
            if resolution > 3:
                resolution -= 1
        if key == glfw.KEY_D:
                resolution += 1
        if key == glfw.KEY_RIGHT:
            angleZ -= 2
        if key == glfw.KEY_UP:
            angleX += 2
        if key == glfw.KEY_DOWN:
            angleX -= 2
        if key == glfw.KEY_M:
            if mode == 0:
                mode = 1
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                mode = 0 	
        if key == glfw.KEY_EQUAL:
           	scale = scale * 1.05
        if key == glfw.KEY_MINUS:
        	scale = scale * 0.95
        if key == glfw.KEY_C:
            color = get_random_color()

line_verticies = [
    [-0.5, 0, 0.7],
    [-0.25, 0, 0],
    [-0.45, 0, 0.7],
    [-0.2, 0, 0],
    [-0.05, 0, 0],
    [-0.05, 0, -0.4],
    [-0.3, 0, -0.5],
    [-0.35, 0, -0.6],
    [0, 0, -0.6]
]

resolution = 10
# отрисовка осей
def draw_axis():
    glLineWidth(3.0)

    glBegin(GL_LINES)
    glColor3f(1.0, 0, 0)
    glVertex3f(1.0, 0, 0)
    glVertex3f(-1.0, 0, 0)
    
    glColor3f(0, 0.5, 0)
    glVertex3f(0, 1.0, 0)
    glVertex3f(0, -1.0, 0)

    glColor3f(0, 0, 1.0)
    glVertex3f(0, 0, 1.0)
    glVertex3f(0, 0, -1.0)
    glEnd()


def rotate(point, degree):
    rad_angle = -radians(degree)
    x = point[0]
    y = point[1]

    rotated_x = x * cos(rad_angle) - y * sin(rad_angle)
    rotated_y = x * sin(rad_angle) + y * cos(rad_angle)

    return [rotated_x, rotated_y, point[2]]


def display(window):
    global line_verticies, resolution, size, color
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMultMatrixd(newMatrix)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(90, 1.0, 0.0, 0.0)    

    glRotatef(angleX, 1.0, 0.0, 0.0)
    glRotatef(angleY, 0.0, 1.0, 0.0)
    glRotatef(angleZ, 0.0, 0.0, 1.0)
    draw_axis()
    glScale(scale, scale, scale)

    # size = 0.5
    glColor4f(*color)
    angle = 360 / resolution
    # поворот прямых
    for i in range(len(line_verticies) - 1):
        v1 = line_verticies[i]
        v2 = line_verticies[i + 1]
        # объединение в полигоны
        glBegin(GL_QUAD_STRIP)
        for _ in range(resolution + 1):
            glVertex3f(*v1)
            glVertex3f(*v2)
            v1 = rotate(v1, angle)
            v2 = rotate(v2, angle)
        glEnd()

    glfw.swap_buffers(window)
    glfw.poll_events()

main()
