import glfw
from OpenGL.GL import *
 
window = None
width = height = 800
PixelBuffer = [1] * width * height * 3
clicks = []
start_pixel = (0, 0)
 
 
def sign(x):
    return 0 if x == 0 else (1 if x > 0 else -1)
 
 
def set_pixel(x, y, rgb=(0, 0, 0)):
    pos = (x + y * width) * 3
    PixelBuffer[pos:pos + 3] = rgb
 
 
def get_color(x, y):
    pos = (x + y * width) * 3
    return PixelBuffer[pos:pos + 3]
 
 
def is_black(x, y):
    return get_color(x, y) != [1, 1, 1]
 
 
def draw_line(x0, y0, x1, y1, smooth=False):
    dx = x1 - x0
    dy = y1 - y0
 
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
 
    dx = abs(dx)
    dy = abs(dy)
 
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0
 
    i = 1
    m = (i * dy) / dx
    e = m / 2
    de = m
    w = i - m
 
    D = 2 * dy - dx
    y = 0
    for x in range(dx + 1):
        if D >= 0:
            y += 1
            e -= w
            D -= 2 * dx
        else:
            e += de
        if smooth:
            set_pixel(x0 + x * xx + y * yx, y0 + x * xy + y * yy, (e, e, e))
        else:
            set_pixel(x0 + x * xx + y * yx, y0 + x * xy + y * yy)
        D += 2 * dy
 
 
def draw_polygon():
    global window, clicks, PixelBuffer
    for i in range(len(clicks) - 1):
        draw_line(*clicks[i], *clicks[i + 1])
    if len(clicks) > 2:
        draw_line(*clicks[-1], *clicks[0])
 
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawPixels(width, height, GL_RGB, GL_FLOAT, (GLfloat * len(PixelBuffer))(*PixelBuffer))
    glfw.swap_buffers(window)
 
 
def smoothing():
    global window, clicks, PixelBuffer
    print(len(clicks))
    for i in range(len(clicks) - 1):
        draw_line(*clicks[i], *clicks[i + 1], smooth=True)
    if len(clicks) > 2:
        draw_line(*clicks[-1], *clicks[0], smooth=True)
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawPixels(width, height, GL_RGB, GL_FLOAT, (GLfloat * len(PixelBuffer))(*PixelBuffer))
    glfw.swap_buffers(window)
 
 
def fill_polygon():
    stack = [start_pixel]
    while len(stack) > 0:
        x, y = stack.pop()
 
        set_pixel(x, y)
        x_left = x - 1
        x_right = x + 1
        while x_left >= 0 and not is_black(x_left, y):
            set_pixel(x_left, y)
            x_left -= 1
        while x_right < width and not is_black(x_right, y):
            set_pixel(x_right, y)
            x_right += 1
 
        x_i = x_left + 1
        if y + 1 < height:
            while x_i < x_right:
                if not is_black(x_i, y + 1):
                    stack.append((x_i, y + 1))
                    while x_i < width and not is_black(x_i, y + 1):
                        x_i += 1
                x_i += 1
 
        x_i = x_left + 1
        if y - 1 >= 0:
            while x_i < x_right:
                if not is_black(x_i, y - 1):
                    stack.append((x_i, y - 1))
                    while x_i < width and not is_black(x_i, y - 1):
                        x_i += 1
                x_i += 1
 
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawPixels(width, height, GL_RGB, GL_FLOAT, (GLfloat * len(PixelBuffer))(*PixelBuffer))
    glfw.swap_buffers(window)
    print("filled")
 
 
def key_callback(window, key, scancode, action, mods):
    global clicks, PixelBuffer
    if action == glfw.PRESS:
        if key == glfw.KEY_ENTER:
            draw_polygon()
            #clicks = []
        if key == glfw.KEY_ESCAPE:
            smoothing()
            print("smoothed")
        if key == glfw.KEY_SPACE:
            PixelBuffer = [1] * width * height * 3
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawPixels(width, height, GL_RGB, GL_FLOAT, (GLfloat * len(PixelBuffer))(*PixelBuffer))
            glfw.swap_buffers(window)
            clicks = []
            print("cleared")
 
 
def mouse_button_callback(window, action, button, mode):
    global start_pixel
    if button == 1:
        x, y = glfw.get_cursor_pos(window)
        x, y = round(2 * x), round(width - 2 * y)
        if action == 0:  # нажатие ЛКМ
            print(f"add {x, y}")
            clicks.append((x, y))
            if len(clicks) > 1:
                draw_line(*clicks[-2], x, y)
                glClear(GL_COLOR_BUFFER_BIT)
                glDrawPixels(width, height, GL_RGB, GL_FLOAT, (GLfloat * len(PixelBuffer))(*PixelBuffer))
                glfw.swap_buffers(window)
        if action == 1:  # нажатие ПКМ
            print(f"start {x, y}")
            start_pixel = (x, y)
            fill_polygon()

def main():
    global window

    if not glfw.init():
        return
    window = glfw.create_window(width // 2, height // 2, "Lab4", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.swap_buffers(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
    glfw.destroy_window(window)
    glfw.terminate()
 
main()