import glfw
import math
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

deltax = 0.0
anglex = 0.0
deltay = 0.0
angley = 0.0
deltaz = 0.0
anglez = 0.0
size = 0.4
posx = 0.0
posy = 0.0
posz = 0.0
dposy = 0.001
dposx = 0.001
dposz = 0.001
window = None

def main():
    global window

    if not glfw.init():
        return
    window = glfw.create_window(740, 740, "Lab3", None, None)
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
    global anglex, deltax, deltay, deltaz
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            deltax += -0.1
        if key == glfw.KEY_LEFT:
            deltax += 0.1
        if key == glfw.KEY_UP:
            deltay += -0.1
        if key == glfw.KEY_DOWN:
            deltay += 0.1
        if key == glfw.KEY_TAB:
            deltaz += -0.1
        if key == glfw.KEY_Q:
            deltaz += 0.1
        if key == glfw.KEY_SPACE:
            # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glEnable(GL_TEXTURE_2D)
        if key == glfw.KEY_ENTER:
            # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glDisable(GL_TEXTURE_2D)

def scroll_callback(window, xoffset, yoffset):
    global size
    if xoffset > 0:
        size -= yoffset / 10
    else:
        size += yoffset / 10

def normal(x1, y1, z1, x2, y2, z2, x3, y3, z3, m):
    i = (-1)**m * ((y2-y1)*(z3-z1) - (y3-y1)*(z2-z1))
    j = (-1)**m * ((x3-x1)*(z2-z1) - (x2-x1)*(z3-z1))
    k = (-1)**m * ((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
    return i, j, k

def display():
    global anglex, angley, anglez, size, dposx, dposy, dposz, posx, posy, posz
    coords = []
    m=[[1, 0, 0, 0],
        [0, 1, 0, 0],
        [-0.5*math.cos(45), -0.5*math.sin(45), -1, 0],
        [0, 0, 0, 1]]
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPushMatrix()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMultMatrixf(m)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(anglex, 0, 1, 0)
    glRotatef(angley, 1, 0, 0)
    glRotatef(anglez, 0, 0, 1)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH)


    glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 70)
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 70)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [-0.5, -0.5, -0.5])

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.5, 0.0, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.0, 0.2, 1.0])

    glColorMaterial(GL_FRONT,GL_AMBIENT)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    image = Image.open("3.bmp")
    w = image.width
    h = image.height
    img_data = image.convert("RGBA").tobytes()
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL) #GL_REPLACE)

    glEnable(GL_NORMALIZE)

    i=0.0
    while i<2*math.pi:
        x1 = posx + 0.5 * size * math.cos(-i)
        z1 = posz + 0.25 * size * math.sin(-i)
        coords.append([x1, posy, z1])
        coords.append([x1, posy + size, z1])
        i+=0.1

    glBegin(GL_POLYGON)
    glColor3f(0.0, 1.0, 0.0)
    x, y, z = normal(coords[0][0], coords[0][1], coords[0][2], coords[(len(coords)-1)//3][0], coords[(len(coords)-1)//3][1], coords[(len(coords)-1)//3][2], coords[2*(len(coords)-1)//3][0], coords[2*(len(coords)-1)//3][1], coords[2*(len(coords)-1)//3][2], 1)
    glNormal3f(x, y, z)
    for i in range(len(coords)-1):
        x = (coords[i][0] - posx)/size + 0.5
        z = (coords[i][2] - posz)/size + 0.5
        glTexCoord2f(x, z)
        glVertex3f(coords[i][0], posy, coords[i][2])
        i+=1
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(0.0, 1.0, 0.0)
    i=1
    u = 0.0
    v = 1.0
    for i in range(len(coords)-1):
        x, y, z = normal(coords[i-1][0], coords[i-1][1], coords[i-1][2], coords[i][0], coords[i][1], coords[i][2], coords[i+1][0], coords[i+1][1], coords[i+1][2], i)
        glNormal3f(x, y, z)
        u1 = u
        u3 = u + 1/len(coords)
        v+=1
        glTexCoord2f(u1, v%2)
        glVertex3f(coords[i-1][0], coords[i-1][1], coords[i-1][2])
        v+=1
        glTexCoord2f(u1, v%2)
        glVertex3f(coords[i][0], coords[i][1], coords[i][2])
        v+=1
        glTexCoord2f(u3, v%2)
        glVertex3f(coords[i+1][0], coords[i+1][1], coords[i+1][2])
        u = u3
    x, y, z = normal(coords[i-1][0], coords[i-1][1], coords[i-1][2], coords[i][0], coords[i][1], coords[i][2], coords[0][0], coords[0][1], coords[0][2], i)
    glNormal3f(x, y, z)
    glTexCoord2f(u, v%2)
    glVertex3f(coords[0][0], coords[0][1], coords[0][2])
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0.0, 1.0, 0.0)
    x, y, z = normal(coords[0][0], coords[0][1], coords[0][2], coords[(len(coords)-1)//3][0], coords[(len(coords)-1)//3][1], coords[(len(coords)-1)//3][2], coords[2*(len(coords)-1)//3][0], coords[2*(len(coords)-1)//3][1], coords[2*(len(coords)-1)//3][2], 0)
    glNormal3f(x, y, z)
    for i in range(len(coords)-1):
        x = (coords[i][0] - posx)/size + 0.5
        z = (coords[i][2] - posz)/size + 0.5
        glTexCoord2f(x, z)
        glVertex3f(coords[i][0], posy + size, coords[i][2])
        i+=1
    glEnd()

    glPopMatrix()
    anglex += deltax
    angley += deltay
    anglez += deltaz

    posx += dposx
    posy += dposy
    posz += dposz
    if not all([-1<i<1 for i, j, k in coords]):
        dposx = -dposx
        posx += 2*dposx
    if not all([-1<j<1 for i, j, k in coords]):
        dposy = -dposy
        posy += 2*dposy
    if not all([-1<k<1 for i, j, k in coords]):
        dposz = -dposz
        posz += 2*dposz

    glfw.swap_buffers(window)
    glfw.poll_events()

main()