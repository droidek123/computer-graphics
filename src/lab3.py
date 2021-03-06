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
    return (5 + 1 * math.cos(2*math.pi*v)) * math.cos(2*math.pi*u)

def calculate_y_torus(u,v):
    return (5 + 1 * math.cos(2*math.pi*v)) * math.sin(2*math.pi*u)

def calculate_z_torus(v):
    return 1 * math.sin(2*math.pi*v)


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
            # pierwszu trojkat
            glColor(colors[idx[0]][idx[1]])
            glVertex3f(model[idx[0]][idx[1]][0], model[idx[0]][idx[1]][1] ,model[idx[0]][idx[1]][2])
            glColor(colors[idx[0]][idx[1]+1])
            glVertex3f(model[idx[0]][idx[1]+1][0], model[idx[0]][idx[1]+1][1] ,model[idx[0]][idx[1]+1][2])
            glColor(colors[idx[0]+1][idx[1]])
            glVertex3f(model[idx[0]+1][idx[1]][0], model[idx[0]+1][idx[1]][1] ,model[idx[0]+1][idx[1]][2])
            # drugi trojkat
            glColor(colors[idx[0]][idx[1]+1])
            glVertex3f(model[idx[0]][idx[1]+1][0], model[idx[0]][idx[1]+1][1] ,model[idx[0]][idx[1]+1][2])
            glColor(colors[idx[0]+1][idx[1]+1])
            glVertex3f(model[idx[0]+1][idx[1]+1][0], model[idx[0]+1][idx[1]+1][1] ,model[idx[0]+1][idx[1]+1][2])
            glColor(colors[idx[0]+1][idx[1]])
            glVertex3f(model[idx[0]+1][idx[1]][0], model[idx[0]+1][idx[1]][1] ,model[idx[0]+1][idx[1]][2])
    glEnd()

# zadanie na 4,5
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
        for j in range(0,n):
            glColor(colors[i][j])
            glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
            glColor(colors[i+1][j])
            glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2])

    glEnd()

# zadanie na 5
def torus(n,colors):
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

    # pierwsza obr??cz
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(n-1):
        if i == (n-1):
            glColor(colors[0][0])
            glVertex3f(model[i][0][0], model[i][0][1] ,model[i][0][2])
            glColor(colors[0+1][0])
            glVertex3f(model[i+1][0][0], model[i+1][0][1] ,model[i+1][0][2])
        else:
            glColor(colors[i][0])
            glVertex3f(model[i][0][0], model[i][0][1] ,model[i][0][2])
            glColor(colors[i+1][0])
            glVertex3f(model[i+1][0][0], model[i+1][0][1] ,model[i+1][0][2])
        for j in range(1,n):
            if i == (n-1) and j == (n - 1):
                glColor(colors[0][j])
                glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
                glColor(colors[0+1][j])
                glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2])
            elif j == (n - 1):
                glColor(colors[i][0])
                glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
                glColor(colors[i+1][0])
                glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2])
            else:
                glColor(colors[i][j])
                glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
                glColor(colors[i+1][j])
                glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2]) 
    glEnd()

    # nast??pne
    for k in range(3):
        if k % 2 == 0:
            glRotatef(90.0, 1.0, 0.0, 0.0)
            glRotatef(-10.0, 0.0, 0.0, 1.0)
            glTranslatef(7.5,0.0,0.0)
            
        else:
            glRotatef(270.0, 1.0, 0.0, 0.0)
            glRotatef(10.0, 0.0, 1.0, 0.0)
            glTranslatef(7.5,0.0,0.0)
        glBegin(GL_TRIANGLE_STRIP)

        for i in range(n-1):
            if i == (n-2):
                glColor(colors[0][0])
                glVertex3f(model[i][0][0], model[i][0][1] ,model[i][0][2])
                glColor(colors[0+1][0])
                glVertex3f(model[i+1][0][0], model[i+1][0][1] ,model[i+1][0][2])
            else:
                glColor(colors[i][0])
                glVertex3f(model[i][0][0], model[i][0][1] ,model[i][0][2])
                glColor(colors[i+1][0])
                glVertex3f(model[i+1][0][0], model[i+1][0][1] ,model[i+1][0][2])
            for j in range(1,n):
                if i == (n-2) and j == (n - 1):
                    glColor(colors[0][j])
                    glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
                    glColor(colors[0+1][j])
                    glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2])
                elif j == (n - 1):
                    glColor(colors[i][0])
                    glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
                    glColor(colors[i+1][0])
                    glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2])
                else:
                    glColor(colors[i][j])
                    glVertex3f(model[i][j][0], model[i][j][1] ,model[i][j][2])
                    glColor(colors[i+1][j])
                    glVertex3f(model[i+1][j][0], model[i+1][j][1] ,model[i+1][j][2]) 
        glEnd()


def startup(zad):
    update_viewport(None, 400, 400, zad)
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


def render(time, colors,n, zad):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()
    if zad == 1: egg_model_points(n)
    elif zad == 2 : egg_model_lines(n)
    elif zad == 3 : egg_model_triangles(n,colors)
    elif zad == 4 : egg_model_triangle_stripes(n,colors)
    elif zad == 5 : torus(n,colors)
    glFlush()


def update_viewport(window, width, height, zad):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if zad == 5:
        if width <= height:
            glOrtho(-25.5, 25.5, -25.5 / aspect_ratio, 25.5 / aspect_ratio, 25.5, -25.5)
        else:
            glOrtho(-25.5 * aspect_ratio, 25.5 * aspect_ratio, -25.5, 25.5, 25.5, -25.5)
    else:
        if width <= height:
            glOrtho(-8.5, 8.5, -8.5 / aspect_ratio, 8.5 / aspect_ratio, 8.5, -8.5)
        else:
            glOrtho(-8.5 * aspect_ratio, 8.5 * aspect_ratio, -8.5, 8.5, 8.5, -8.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    zad = int(input('Podaj zadanie: '))
    n = int(input('Podaj N: '))
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

    startup(zad)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(),colors, n, zad)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
