import glfw
from OpenGL.GL import *
from math import *


angleX = 0.0
angleY = 0.0
angleZ = 0.0
scale = 1
size = 0.5

tetta = pi / 5.1045
phi =  pi / 4


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


def key_callback(window, key, scancode, action, mods):
    global angleZ, angleX, angleY, scale
    if (action == glfw.REPEAT or action == glfw.PRESS):
        if key == glfw.KEY_RIGHT:
            angleZ -= 2
        if key == glfw.KEY_LEFT:
            angleZ += 2
        if key == glfw.KEY_A:
            angleX += 2
        if key == glfw.KEY_D:
            angleX -= 2
        if key == glfw.KEY_W:
            angleY += 2
        if key == glfw.KEY_S:
            angleY -= 2
        if key == glfw.KEY_F:
        	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
       	if key == glfw.KEY_B:
        	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if key == glfw.KEY_EQUAL:
           	scale = scale * 1.05
        if key == glfw.KEY_MINUS:
        	scale = scale * 0.95

def draw_cube():
# Левая грань
    glBegin(GL_POLYGON)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, -size, size)
    glEnd()

# Правая грань
    glBegin(GL_POLYGON)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    glEnd()

# Нижняя грань
    glBegin(GL_POLYGON)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, -size, -size)
    glEnd()

# Верхняя грань
    glBegin(GL_POLYGON)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    glEnd()

# Задняя грань
    glBegin(GL_POLYGON)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)
    glEnd()

# Передняя грань 
    glBegin(GL_POLYGON)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    glEnd()
    

def display(window):
	global size
	glClearColor(1.0, 1.0, 1.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glMultMatrixd(newMatrix)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glRotatef(angleX, 1.0, 0.0, 0.0)
	glRotatef(angleY, 0.0, 1.0, 0.0)
	glRotatef(angleZ, 0.0, 0.0, 1.0)
	glScale(scale, scale, scale)

#Двигающийся куб
	glPushMatrix()
	size = 0.2
	glColor3f(1, 0, 1)
	draw_cube()

#Статичный куб
	
	glLoadIdentity()
	glTranslate(-0.3, 0.8, 0)
	glScale(0.5, 0.5, 0.5)
	glColor3f(1, 0, 0)
	draw_cube()

	glPopMatrix()


	glfw.swap_buffers(window)
	glfw.poll_events()

main()
