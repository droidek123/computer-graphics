#!/usr/bin/env python3
import sys
import numpy as np
import math
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


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

def calculate_x_torus(u,v):
    return (5 + 2 * math.cos(2*math.pi*v)) * math.cos(2*math.pi*u)

def calculate_y_torus(u,v):
    return (5 + 2 * math.cos(2*math.pi*v)) * math.sin(2*math.pi*u)

def calculate_z_torus(v):
    return 2 * math.sin(2*math.pi*v)


# Zadanie na 3.0
def egg_model_points(n):
    u = [None] * n
    v = [None] * n
    last_val = 0
    for i in range(n):
        u[i] = last_val
        v[i] = last_val
        last_val += 1/(n-1)

    model = np.zeros((n,n,3))
    for idx, _ in np.ndenumerate(model):
        if idx[2] == 0: model[idx[0]][idx[1]][idx[2]] = calculate_x(u[idx[0]],v[idx[1]])
        elif idx[2] == 1: model[idx[0]][idx[1]][idx[2]] = calculate_y(u[idx[0]])
        else: model[idx[0]][idx[1]][idx[2]] = calculate_z(u[idx[0]],v[idx[1]])

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    for idx, _ in np.ndenumerate(model):
        # glVertex3fv(model[idx[0]][idx[1]])
        glVertex3f(model[idx[0]][idx[1]][0], model[idx[0]][idx[1]][1] ,model[idx[0]][idx[1]][2])
    glEnd()

# Zadanie na 3.5
def egg_model_lines(n):
    u = [None] * n
    v = [None] * n
    last_val = 0
    for i in range(n):
        u[i] = last_val
        v[i] = last_val
        last_val += 1/(n-1)

    model = np.zeros((n,n,3))
    for idx, _ in np.ndenumerate(model):
        if idx[2] == 0: model[idx[0]][idx[1]][idx[2]] = calculate_x(u[idx[0]],v[idx[1]])
        elif idx[2] == 1: model[idx[0]][idx[1]][idx[2]] = calculate_y(u[idx[0]])
        else: model[idx[0]][idx[1]][idx[2]] = calculate_z(u[idx[0]],v[idx[1]])

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    for idx, _ in np.ndenumerate(model):
        # linie poziome
        if idx[0] != (n-1) and idx[1] != (n-1):
            glVertex3f(model[idx[0]][idx[1]][0], model[idx[0]][idx[1]][1] ,model[idx[0]][idx[1]][2])
            glVertex3f(model[idx[0]][idx[1]+1][0], model[idx[0]][idx[1]+1][1] ,model[idx[0]][idx[1]+1][2])
        #linie pionowe
        if idx[0] != (n-1):
            glVertex3f(model[idx[0]][idx[1]][0], model[idx[0]][idx[1]][1] ,model[idx[0]][idx[1]][2])
            glVertex3f(model[idx[0]+1][idx[1]][0], model[idx[0]+1][idx[1]][1] ,model[idx[0]+1][idx[1]][2])  
    glEnd()

# Zadanie na 4.0
def egg_model_triangles(n,colors):
    u = [None] * n
    v = [None] * n
    last_val = 0
    for i in range(n):
        u[i] = last_val
        v[i] = last_val
        last_val += 1/(n-1)

    model = np.zeros((n,n,3))
    for idx, _ in np.ndenumerate(model):
        if idx[2] == 0: model[idx[0]][idx[1]][idx[2]] = calculate_x(u[idx[0]],v[idx[1]])
        elif idx[2] == 1: model[idx[0]][idx[1]][idx[2]] = calculate_y(u[idx[0]])
        else: model[idx[0]][idx[1]][idx[2]] = calculate_z(u[idx[0]],v[idx[1]])

    glBegin(GL_TRIANGLES)
    for idx, _ in np.ndenumerate(model):
        if idx[0] != (n-1) and idx[1] != (n-1):
            glColor(colors[idx[0]][idx[1]])
            glVertex3f(model[idx[0]][idx[1]][0], model[idx[0]][idx[1]][1] ,model[idx[0]][idx[1]][2])
            glColor(colors[idx[0]][idx[1]+1])
            glVertex3f(model[idx[0]][idx[1]+1][0], model[idx[0]][idx[1]+1][1] ,model[idx[0]][idx[1]+1][2])
            glColor(colors[idx[0]+1][idx[1]])
            glVertex3f(model[idx[0]+1][idx[1]][0], model[idx[0]+1][idx[1]][1] ,model[idx[0]+1][idx[1]][2])

            glColor(colors[idx[0]][idx[1]+1])
            glVertex3f(model[idx[0]][idx[1]+1][0], model[idx[0]][idx[1]+1][1] ,model[idx[0]][idx[1]+1][2])
            glColor(colors[idx[0]+1][idx[1]+1])
            glVertex3f(model[idx[0]+1][idx[1]+1][0], model[idx[0]+1][idx[1]+1][1] ,model[idx[0]+1][idx[1]+1][2])
            glColor(colors[idx[0]+1][idx[1]])
            glVertex3f(model[idx[0]+1][idx[1]][0], model[idx[0]+1][idx[1]][1] ,model[idx[0]+1][idx[1]][2])
    glEnd()


def egg_model_triangle_stripes(n,colors):
    u = [None] * n
    v = [None] * n
    last_val = 0
    for i in range(n):
        u[i] = last_val
        v[i] = last_val
        last_val += 1/(n-1)

    model = np.zeros((n,n,3))
    for idx, _ in np.ndenumerate(model):
        if idx[2] == 0: model[idx[0]][idx[1]][idx[2]] = calculate_x(u[idx[0]],v[idx[1]])
        elif idx[2] == 1: model[idx[0]][idx[1]][idx[2]] = calculate_y(u[idx[0]])
        else: model[idx[0]][idx[1]][idx[2]] = calculate_z(u[idx[0]],v[idx[1]])

    glBegin(GL_TRIANGLE_STRIP)
    for i in range(n-1):
        glColor(colors[i][0])
        glVertex3f(model[i][0][0], model[i][0][1] ,model[i][0][2])
        glColor(colors[i+1][0])
        glVertex3f(model[i+1][0][0], model[i+1][0][1] ,model[i+1][0][2])
        for j in range(1,n):
            glColor(colors[i][j])
            glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
            glColor(colors[i+1][j])
            glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2])

    glEnd()


def torus(n):
    u = [None] * n
    v = [None] * n
    last_val = 0
    for i in range(n):
        u[i] = last_val
        v[i] = last_val
        last_val += 1/(n-1)

    model = np.zeros((n,n,3))
    for idx, _ in np.ndenumerate(model):
        if idx[2] == 0: model[idx[0]][idx[1]][idx[2]] = calculate_x_torus(u[idx[0]],v[idx[1]])
        elif idx[2] == 1: model[idx[0]][idx[1]][idx[2]] = calculate_y_torus(u[idx[0]],v[idx[1]])
        else: model[idx[0]][idx[1]][idx[2]] = calculate_z_torus(v[idx[1]])

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    for idx, _ in np.ndenumerate(model):
        glVertex3f(model[idx[0]][idx[1]][0], model[idx[0]][idx[1]][1] ,model[idx[0]][idx[1]][2])
    glEnd()



def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


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

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time, colors):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()
    # egg_model_points(20)
    # egg_model_lines(20)
    # egg_model_triangles(20,colors)
    # egg_model_triangle_stripes(20,colors)
    torus(20)
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
    # n = input('Podaj N:')
    colors = np.zeros((20,20,3))

    for idx, val in np.ndenumerate(colors):
        colors[idx[0]][idx[1]][idx[2]] = random.random()

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
        render(glfwGetTime(),colors)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
