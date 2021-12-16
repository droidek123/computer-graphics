import math
import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

color_r = random.random()
color_g = random.random()
color_b = random.random()
color_a = random.random()
d = random.random()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    # create_triangle()
    # create_rectangle(-25,-25,50,50)
    # create_random_rectangle(-25, -25, 50, 50, d)
    # create_fractal(-50, -30, 100, 60, 3)
    koch_snowflake(-75, 40, 75, 40, 0, -90, 4)
    glFlush()


# -------------Zad 3.0-------------
def create_triangle():
    glBegin(GL_TRIANGLES)
    glColor(1.0, 0.0, 0.0)
    glVertex2f(75.0, 40.0)
    glColor(0.0, 1.0, 0.0)
    glVertex2f(0.0, -90.0)
    glColor(0.0, 0.0, 1.0)
    glVertex2f(-75.0, 40.0)
    glEnd()


# -------------Zad 3.5-------------
def create_rectangle(x, y, a, b):
    glColor(1, 0, 0, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)

    glVertex2f(x + a, y + b)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)
    glEnd()


# -------------Zad 4.0-------------
def create_random_rectangle(x, y, a, b, d):
    glBegin(GL_TRIANGLES)

    glColor(color_r, color_g, color_b, color_a)
    glVertex2f(x, y)
    glVertex2f(x + a * d, y)
    glVertex2f(x - a * d, y + b * d)

    glVertex2f(x + a, y + b)
    glVertex2f(x + a * d, y)
    glVertex2f(x - a * d, y + b * d)
    glEnd()


# -------------Zad 4.5-------------
def create_fractal(x, y, width, height, depth):
    glColor(1, 0, 0, 1)
    glBegin(GL_POLYGON)

    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    calculate_points(x, y, width, height, depth)


def calculate_points(x, y, width, height, depth):
    w = width / 3
    h = height / 3

    glColor(1, 1, 1, 1)
    glBegin(GL_POLYGON)
    glVertex2f(x + w, y + h)
    glVertex2f(x + w, y + 2 * h)
    glVertex2f(x + 2 * w, y + 2 * h)
    glVertex2f(x + 2 * w, y + h)
    glEnd()
    if depth > 0:
        calculate_points(x, y, w, h, depth - 1)
        calculate_points(x + w, y, w, h, depth - 1)
        calculate_points(x + 2 * w, y, w, h, depth - 1)
        calculate_points(x, y + h, w, h, depth - 1)
        calculate_points(x, y + 2 * h, w, h, depth - 1)
        calculate_points(x + w, y + 2 * h, w, h, depth - 1)
        calculate_points(x + 2 * w, y + 2 * h, w, h, depth - 1)
        calculate_points(x + 2 * w, y + h, w, h, depth - 1)


# -------------Zad 5.0-------------
def koch_snowflake(x1, y1, x2, y2, x3, y3, depth):
    koch_curve(x1, y1, x2, y2, depth)
    koch_curve(x3, y3, x1, y1, depth)
    koch_curve(x2, y2, x3, y3, depth)


def koch_curve(x1, y1, x5, y5, depth):
    l = math.sqrt((x1 - x5) ** 2 + (y1 - y5) ** 2) / 3
    rad = -60 * math.pi / 180

    x2 = (2 * x1 + x5) / 3
    y2 = (2 * y1 + y5) / 3

    x4 = (x1 + 2 * x5) / 3
    y4 = (y1 + 2 * y5) / 3

    x3 = x2 + (x4 - x2) * math.cos(rad) + (y4 - y2) * math.sin(rad)
    y3 = y2 - (x4 - x2) * math.sin(rad) + (y4 - y2) * math.cos(rad)

    if depth == 0:
        glColor(1, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)

        glVertex2f(x2, y2)
        glVertex2f(x3, y3)

        glVertex2f(x3, y3)
        glVertex2f(x4, y4)

        glVertex2f(x4, y4)
        glVertex2f(x5, y5)
        glEnd()

    else:
        koch_curve(x1, y1, x2, y2, depth - 1)
        koch_curve(x2, y2, x3, y3, depth - 1)
        koch_curve(x3, y3, x4, y4, depth - 1)
        koch_curve(x4, y4, x5, y5, depth - 1)


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
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
