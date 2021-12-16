import math
import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *



def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()
    
    # egg_model_points(20)
    # egg_model_lines(20)
    egg_model_triangles(20)


def calculate_x(u, v):
    return (
        -90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u
    ) * math.cos(math.pi * v)


def calculate_y(u):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2


def calculate_z(u, v):
    return (
        -90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u
    ) * math.sin(math.pi * v)


def egg_model_points(n):
    list_u = [0.0]
    list_v = [0.0]
    step = 1 / n
    for i in range(n):
        list_u.append(list_u[i] + step)
        list_v.append(list_u[i] + step)

    list = []
    for i in range(n):
        list.append([])
        for j in range(n):
            list[i].append([])
            list[i][j].append(calculate_x(list_u[i], list_v[j]))
            list[i][j].append(calculate_y(list_u[i]))
            list[i][j].append(calculate_z(list_u[i], list_v[j]))

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    for i in range(n):
        list.append([])
        for j in range(n):
            glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])

    glEnd()


def egg_model_lines(n):
    list_u = [0.0]
    list_v = [0.0]
    step = 1 / n
    for i in range(n):
        list_u.append(list_u[i] + step)
        list_v.append(list_u[i] + step)


    list = []
    for i in range(n):
        list.append([])
        for j in range(n):
            list[i].append([])
            list[i][j].append(calculate_x(list_u[i], list_v[j]))
            list[i][j].append(calculate_y(list_u[i]))
            list[i][j].append(calculate_z(list_u[i], list_v[j]))

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for i in range(n):
        for j in range(n-1):
            glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])
            glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
            if(i > 0 and i != (n-1) and j == (n-2)):
                glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
                glVertex3f(list[n-i][0][0], list[n-i][0][1], list[n-i][0][2])
            if(i == (n-1) and j == (n-2)):
                glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
                glVertex3f(list[1][0][0], list[1][0][1], list[1][0][2])
    
    for i in range(n):
        for j in range(n):
            if i != (n-1):
                glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])
                glVertex3f(list[i+1][j][0], list[i+1][j][1], list[i+1][j][2])
            else:
                glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])
                glVertex3f(list[0][j][0], list[0][j][1], list[0][j][2])

    glEnd()


def egg_model_triangles(n):
    list_u = [0.0]
    list_v = [0.0]
    step = 1 / n
    for i in range(n):
        list_u.append(list_u[i] + step)
        list_v.append(list_u[i] + step)

    list = []
    for i in range(n):
        list.append([])
        for j in range(n):
            list[i].append([])
            list[i][j].append(calculate_x(list_u[i], list_v[j]))
            list[i][j].append(calculate_y(list_u[i]))
            list[i][j].append(calculate_z(list_u[i], list_v[j]))
    

    glBegin(GL_TRIANGLES)
    for i in range(n):
        for j in range(n):
            if i != (n-1) and j != (n-1):
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])
                glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
                glVertex3f(list[i+1][j][0], list[i+1][j][1], list[i+1][j][2])
                
                glColor3f(1.0, 1.0, 0.0)
                glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
                glVertex3f(list[i+1][j][0], list[i+1][j][1], list[i+1][j][2])
                glVertex3f(list[i+1][j+1][0], list[i+1][j+1][1], list[i+1][j+1][2])

            if i == (n-1) and j != (n-1):
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])
                glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
                glVertex3f(list[0][j][0], list[0][j][1], list[0][j][2])
                
                glColor3f(1.0, 1.0, 0.0)
                glVertex3f(list[i][j+1][0], list[i][j+1][1], list[i][j+1][2])
                glVertex3f(list[0][j][0], list[0][j][1], list[0][j][2])
                glVertex3f(list[0][j+1][0], list[0][j+1][1], list[0][j+1][2])

            if i != (n-1) and j == (n-1) and i > 1:
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(list[i][j][0], list[i][j][1], list[i][j][2])
                glVertex3f(list[n-i][0][0], list[n-i][0][1], list[n-i][0][2])
                glVertex3f(list[i+1][j][0], list[i+1][j][1], list[i+1][j][2])
                
                glColor3f(1.0, 0.0, 1.0)
                glVertex3f(list[i+1][j][0], list[i+1][j][1], list[i+1][j][2])
                glVertex3f(list[n-i][0][0], list[n-i][0][1], list[n-i][0][2])
                glVertex3f(list[n-i+1][0][0], list[n-i+1][0][1], list[n-i+1][0][2])
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == "__main__":
    main()
