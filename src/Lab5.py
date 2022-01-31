#!/usr/bin/env python3
import sys
import math
import numpy as np

from glfw.GLFW import *

from os import system

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 15.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

x_s = 0.0
y_s = 0.0
z_s = 0.0
R = 10.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0
normal = 1

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light_ambient1 = [0.0, 0.0, 0.0, 1.0]
light_diffuse1 = [0.0, 0.0, 1.0, 1.0]
light_specular1 = [0.0, 0.0, 0.0, 1.0]
light_position1 = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

mode = 0
choose = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    info()


def shutdown():
    pass


def render(time, n, array, normalVector):
    global theta
    global phi
    global x_s
    global y_s
    global z_s
    global R
    global light_position1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    if right_mouse_button_pressed == 1:
        theta += delta_x * pix2angle
        glRotate(theta, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed == 1:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
        x_s = R * math.cos(theta * (math.pi / 180)) * math.cos(phi * (math.pi / 180))
        y_s = R * math.sin(phi * (math.pi / 180))
        z_s = R * math.sin(theta * (math.pi / 180)) * math.cos(phi * (math.pi / 180))

        light_position1 = [-x_s, -y_s, z_s, 1.0]

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)

    glTranslatef(0.0, -5.0, 0.0)
    strip_egg(array, n, normalVector)
    if normal == 1:
        vectors(array, n, normalVector)

    glTranslatef(-x_s, -y_s, z_s)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def vectors(array, n, normalVector):
    for i in range(n):
        glBegin(GL_LINES)
        if i < (n - 1):
            for j in range(n):
                if j < (n - 1):
                    glVertex3f(array[i][j][0], array[i][j][1], array[i][j][2])
                    glVertex3f(array[i][j][0] + normalVector[i][j][0], array[i][j][1] + normalVector[i][j][1],
                               array[i][j][2] + normalVector[i][j][2])

                    glVertex3f(array[i + 1][j][0], array[i + 1][j][1], array[i + 1][j][2])
                    glVertex3f(array[i + 1][j][0] + normalVector[i + 1][j][0],
                               array[i + 1][j][1] + normalVector[i + 1][j][1],
                               array[i + 1][j][2] + normalVector[i + 1][j][2])

                    glVertex3f(array[i][j + 1][0], array[i][j + 1][1], array[i][j + 1][2])
                    glVertex3f(array[i][j + 1][0] + normalVector[i][j + 1][0],
                               array[i][j + 1][1] + normalVector[i][j + 1][1],
                               array[i][j + 1][2] + normalVector[i][j + 1][2])

                    glVertex3f(array[i + 1][j + 1][0], array[i + 1][j + 1][1], array[i + 1][j + 1][2])
                    glVertex3f(array[i + 1][j + 1][0] + normalVector[i + 1][j + 1][0],
                               array[i + 1][j + 1][1] + normalVector[i + 1][j + 1][1],
                               array[i + 1][j + 1][2] + normalVector[i + 1][j + 1][2])
        glEnd()


def strip_egg(array, n, normalVector):
    for i in range(n):
        glBegin(GL_TRIANGLE_STRIP)
        if i < (n - 1):
            for j in range(n):
                if j < (n - 1):
                    glNormal3f(normalVector[i][j][0], normalVector[i][j][1], normalVector[i][j][2])
                    glVertex3f(array[i][j][0], array[i][j][1], array[i][j][2])

                    glNormal3f(normalVector[i + 1][j][0], normalVector[i + 1][j][1], normalVector[i + 1][j][2])
                    glVertex3f(array[i + 1][j][0], array[i + 1][j][1], array[i + 1][j][2])

                    glNormal3f(normalVector[i][j + 1][0], normalVector[i][j + 1][1], normalVector[i][j + 1][2])
                    glVertex3f(array[i][j + 1][0], array[i][j + 1][1], array[i][j + 1][2])

                    glNormal3f(normalVector[i + 1][j + 1][0], normalVector[i + 1][j + 1][1],
                               normalVector[i + 1][j + 1][2])
                    glVertex3f(array[i + 1][j + 1][0], array[i + 1][j + 1][1], array[i + 1][j + 1][2])
        glEnd()


def arrays(n, array, normalVector):
    u = np.linspace(0.0, 1.0, n)
    v = np.linspace(0.0, 1.0, n)

    for i in range(n):
        for j in range(n):
            array[i][j][0] = (-90 * pow(u[i], 5) + 225 * pow(u[i], 4) - 270 * pow(u[i], 3) + 180 * pow(u[i], 2) - 45 *
                              u[i]) * math.cos(math.pi * v[j])
            array[i][j][1] = 160 * pow(u[i], 4) - 320 * pow(u[i], 3) + 160 * pow(u[i], 2)
            array[i][j][2] = (-90 * pow(u[i], 5) + 225 * pow(u[i], 4) - 270 * pow(u[i], 3) + 180 * pow(u[i], 2) - 45 *
                              u[i]) * math.sin(math.pi * v[j])

            Xu = (-450 * pow(u[i], 4) + 900 * pow(u[i], 3) - 810 * pow(u[i], 2) + 360 * u[i] - 45) * math.cos(
                math.pi * v[j])
            Xv = math.pi * (90 * pow(u[i], 5) - 225 * pow(u[i], 4) + 270 * pow(u[i], 3) - 180 * pow(u[i], 2) + 45 * u[
                i]) * math.sin(math.pi * v[j])
            Yu = 640 * pow(u[i], 3) - 960 * pow(u[i], 2) + 320 * u[i]
            Yv = 0
            Zu = (-450 * pow(u[i], 4) + 900 * pow(u[i], 3) - 810 * pow(u[i], 2) + 360 * u[i] - 45) * math.sin(
                math.pi * v[j])
            Zv = -math.pi * (90 * pow(u[i], 5) - 225 * pow(u[i], 4) + 270 * pow(u[i], 3) - 180 * pow(u[i], 2) + 45 * u[
                i]) * math.cos(math.pi * v[j])

            vectorX = Yu * Zv - Zu * Yv
            vectorY = Zu * Xv - Xu * Zv
            vectorZ = Xu * Yv - Yu * Xv

            length = math.sqrt(pow(vectorX, 2) + pow(vectorY, 2) + pow(vectorZ, 2))

            if i < n/2:
                normalVector[i][j][0] = vectorX / length
                normalVector[i][j][1] = vectorY / length
                normalVector[i][j][2] = vectorZ / length
            else:
                normalVector[i][j][0] = -vectorX / length
                normalVector[i][j][1] = -vectorY / length
                normalVector[i][j][2] = -vectorZ / length


def info():
    system('cls')
    print("Light ambient: ")
    print(light_ambient1)
    print("Light diffuse: ")
    print(light_diffuse1)
    print("Light specular: ")
    print(light_specular1)
    print("Mode: ")
    print(mode)
    print("i: ")
    print(choose)


def keyboard_key_callback(window, key, scancode, action, mods):
    global mode
    global choose
    global normal
    global light_ambient1
    global light_specular1
    global light_diffuse1

    if key == GLFW_KEY_N and action == GLFW_PRESS:
        if normal == 0:
            normal = 1
        else:
            normal = 0

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        mode = 0

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        mode = 2

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        mode = 1

    if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
        if choose > 0:
            choose -= 1

    if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
        if choose < 3:
            choose += 1

    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        if mode == 0:
            if light_ambient1[choose] < 1.0:
                light_ambient1[choose] += 0.1

        if mode == 1:
            if light_specular1[choose] < 1.0:
                light_specular1[choose] += 0.1

        if mode == 2:
            if light_diffuse1[choose] < 1.0:
                light_diffuse1[choose] += 0.1

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        if mode == 0:
            if light_ambient1[choose] > 0.0:
                light_ambient1[choose] -= 0.1

        if mode == 1:
            if light_specular1[choose] > 0.0:
                light_specular1[choose] -= 0.1

        if mode == 2:
            if light_diffuse1[choose] > 0.0:
                light_diffuse1[choose] -= 0.1

    info()


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    n = 20
    array = np.zeros([n, n, 3])
    normalVector = np.zeros([n, n, 3])
    arrays(n, array, normalVector)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), n, array, normalVector)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
