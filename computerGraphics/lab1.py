import glfw

delta = 0.1
angle = 0.0
posx = 0.0
posy = 0.0
size = 0.0
window = None

from OpenGL.GL import *


def main():
    global window

    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display()
    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global angle, delta, posx, posy
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            delta = -3
        if key == 263:
            delta = 3
        if key == glfw.KEY_ENTER:
            delta = 0
        if key == glfw.KEY_UP:
            posy += 0.05
        if key == glfw.KEY_DOWN:
            posy -= 0.05


def display():
    global angle, delta

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPushMatrix()
    glRotatef(angle, 0, 0, 1)
    glBegin(GL_POLYGON)
    glColor3f(0.1, 0.1, 0.1)
    glVertex2f(posx + size, posy + size + 0.5)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(posx + size - 0.6, posy - size + 0.1)
    glColor3f(0.35, 0.0, 0.89)
    glVertex2f(posx - size - 0.5, posy + size + -0.5)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(posx + size + 0.5, posy - size + -0.5)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(posx + size + 0.6, posy - size + 0.1)
    glEnd()
    glPopMatrix()
    angle += delta
    glfw.swap_buffers(window)
    glfw.poll_events()


main()
