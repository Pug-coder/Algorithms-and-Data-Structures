from OpenGL.GL import *
import glfw
from PIL import Image
import numpy

G = 9.81
INITIAL_CUBE_VELOCITY = 0
CUBE_HEIGHT_RANGE = (0, 3000)

cube_velocity = INITIAL_CUBE_VELOCITY
cube_height = CUBE_HEIGHT_RANGE[1]
theta = 0

rot = 0
scale = 1
is_texturing_enabled = True

def normalize(x, x_range, normalization_range):
    a, b = normalization_range
    x_min, x_max = x_range
    return (b - a) * ((x - x_min) / (x_max - x_min)) + a


def program():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Sukhanov lab8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    setup()

    while not glfw.window_should_close(window):
        prepare()
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global rot, scale, is_texturing_enabled

    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            rot -= 3
        if key == glfw.KEY_LEFT:
            rot += 3
        if key == glfw.KEY_UP:
            scale += 0.1
        if key == glfw.KEY_DOWN:
            scale -= 0.1
        if key == glfw.KEY_C:
            is_texturing_enabled = not is_texturing_enabled

def enable_texturing():
    global is_texturing_enabled
    if is_texturing_enabled:
        glEnable(GL_TEXTURE_2D)

def disable_texturing():
    global is_texturing_enabled
    if is_texturing_enabled:
        glDisable(GL_TEXTURE_2D)


def setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.1, 0.1, -0.1, 0.1, 0.2, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 0.5])

    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)



    load_texture()

    # Положение вершин не меняется
    # Цвет вершины - такой же как и в массиве цветов
    vertex = create_shader(GL_VERTEX_SHADER, """
    varying vec3 n;
    varying vec3 v;
    varying vec2 uv;
    void main()
    {   
        uv = gl_MultiTexCoord0.xy;
        v = vec3(gl_ModelViewMatrix * gl_Vertex);
        n = normalize(gl_NormalMatrix * gl_Normal);
        gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0;
        gl_Position = ftransform();
    }


    """)

    # Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
    fragment = create_shader(GL_FRAGMENT_SHADER, """
    varying vec3 n;
    varying vec3 v; 
    uniform sampler2D tex;
    void main ()  
    {  
        vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
        vec3 E = normalize(-v);
        vec3 R = normalize(-reflect(L,n));  

        //calculate Ambient Term:  
        vec4 Iamb = gl_FrontLightProduct[0].ambient;    

        //calculate Diffuse Term:  
        vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 0.0);
        Idiff = clamp(Idiff, 0.0, 1.0);     

        // calculate Specular Term:
        vec4 Ispec = gl_LightSource[0].specular 
                        * pow(max(dot(R,E),0.0),0.3);
        Ispec = clamp(Ispec, 0.0, 1.0); 

        vec4 texColor = texture2D(tex, gl_TexCoord[0].st);
        gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
    }
    """)


    program = glCreateProgram()

    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)

    glUseProgram(program)

def load_texture():
    img = Image.open("3.bmp")
    img_data = numpy.array(list(img.getdata()), numpy.int8)

    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)


def prepare():
    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def display():
    global CUBE_HEIGHT_RANGE, cube_velocity, cube_height, theta, rot, scale
    glPushMatrix()
    glRotatef(-60, 1, 0, 0)
    glRotatef(33, 0, 0, 1)
    glTranslatef(2, 3, -2.5)

    glRotatef(rot, 0, 0, 1)
    glScalef(scale, scale, scale)
    

    glPushMatrix()


    if cube_height - cube_velocity > CUBE_HEIGHT_RANGE[0]:
        cube_height -= cube_velocity
        if cube_velocity < 0 and cube_velocity + G > 0:
            cube_velocity = 0
        else:
            cube_velocity += G
    else:
        cube_height = CUBE_HEIGHT_RANGE[0]
        cube_velocity = -cube_velocity


    glRotatef(45, 0, 0, 1)
    glTranslatef(0, 0, normalize(cube_height, CUBE_HEIGHT_RANGE, (0.5, 1)))
    glScalef(0.1, 0.1, 0.1)
    draw_cube()

    glPopMatrix()

    glPushMatrix()
    glRotatef(45, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 0))

    glTranslatef(0, 0, 2)
    glScalef(0.2, 0.2, 0.2)
    glColor3f(1, 1, 1)
    glPopMatrix()

    glPopMatrix()

    theta += 0.9


# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
    # Создаем пустой объект шейдера
    shader = glCreateShader(shader_type)
    # Привязываем текст шейдера к пустому объекту шейдера
    glShaderSource(shader, source)
    # Компилируем шейдер
    glCompileShader(shader)
    # Возвращаем созданный шейдер
    return shader


def draw_cube():
    enable_texturing()
    glBegin(GL_QUADS)


    glNormal3f(1.0, 0.0, 0.0)  
    glTexCoord2f(1.0, 0.0) 
    glVertex3f(1, 1, 1)   
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(1,-1, 1)  
    glTexCoord2f(0.0, 1.0)  
    glVertex3f(1,-1,-1)   
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 1,-1)   

    glNormal3f(0.0, 0.0, -1.0) 
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, 1,-1)   
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(1,-1,-1)   
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-1,-1,-1)   
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(-1, 1,-1)   
  
    glNormal3f(-1.0, 0.0, 0.0) 
    glTexCoord2f(1.0, 0.0) 
    glVertex3f(-1, 1,-1)   
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(-1,-1,-1)   
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-1,-1, 1)   
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(-1, 1, 1)   
  
    glNormal3f(0.0, 0.0, 1.0)  
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-1, 1, 1)   
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(-1,-1, 1)   
    glTexCoord2f(1.0, 0.0) 
    glVertex3f(1,-1, 1)   
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(1, 1, 1)   
  
    glNormal3f(0.0, 1.0, 0.0)   
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-1, 1,-1)   
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(-1, 1, 1)   
    glTexCoord2f(1.0, 0.0) 
    glVertex3f(1, 1, 1)   
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(1, 1,-1)   
  
    glNormal3f(1.0, -1.0, 0.0)  
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-1,-1, 1)   
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(-1,-1,-1)   
    glTexCoord2f(1.0, 0.0) 
    glVertex3f(1,-1,-1)   
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(1,-1, 1)   

    glEnd()
    disable_texturing()

def draw_plane():
    verticies = (
        -1, -1, 0,
        1, -1, 0,
        1, 1, 0,
        -1, 1, 0
    )

    normals = (
        -1, -1, 3,
        1, -1, 3,
        1, 1, 3,
        -1, 1, 3
    )

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, verticies)
    glNormalPointer(GL_FLOAT, 0, normals)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)


program()