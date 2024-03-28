import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def rotate_cube(vertices, point1, point2, angle):
    direction = np.array(point2) - np.array(point1)
    axis = direction / np.linalg.norm(direction)
    theta = np.radians(angle)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    rotation_matrix = np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                                [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                                [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
    rotated_vertices = np.dot(vertices - point1, rotation_matrix) + point1
    return rotated_vertices


def draw_cube(vertices):
    plt.close('all')
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='b')

    # Drawing edges
    for i in range(4):
        ax.plot(vertices[[i, (i + 1) % 4], 0], vertices[[i, (i + 1) % 4], 1], vertices[[i, (i + 1) % 4], 2], color='r')
        ax.plot(vertices[[i + 4, (i + 1) % 4 + 4], 0], vertices[[i + 4, (i + 1) % 4 + 4], 1],
                vertices[[i + 4, (i + 1) % 4 + 4], 2], color='r')
        ax.plot(vertices[[i, i + 4], 0], vertices[[i, i + 4], 1], vertices[[i, i + 4], 2], color='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return fig


def update_cube():
    p1 = [float(p1x_entry.get()), float(p1y_entry.get()), float(p1z_entry.get())]
    p2 = [float(p2x_entry.get()), float(p2y_entry.get()), float(p2z_entry.get())]
    angle = angle_slider.get()

    rotated_vertices = rotate_cube(vertices, p1, p2, angle)

    for widget in canvas_frame.winfo_children():
        widget.destroy()
    fig = draw_cube(rotated_vertices)
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


vertices = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
])

# GUI setup
root = tk.Tk()
root.title("Cube Rotator")

# Поля для ввода точек
p1x_entry = ttk.Entry(root)
p1x_entry.grid(row=0, column=1)
p1y_entry = ttk.Entry(root)
p1y_entry.grid(row=0, column=2)
p1z_entry = ttk.Entry(root)
p1z_entry.grid(row=0, column=3)
ttk.Label(root, text="Point 1 (x, y, z):").grid(row=0, column=0)

p1x_entry.insert(0, "0")
p1y_entry.insert(0, "0")
p1z_entry.insert(0, "0")

p2x_entry = ttk.Entry(root)
p2x_entry.grid(row=1, column=1)
p2y_entry = ttk.Entry(root)
p2y_entry.grid(row=1, column=2)
p2z_entry = ttk.Entry(root)
p2z_entry.grid(row=1, column=3)
ttk.Label(root, text="Point 2 (x, y, z):").grid(row=1, column=0)

p2x_entry.insert(0, "1")
p2y_entry.insert(0, "1")
p2z_entry.insert(0, "1")

# Ползунок
angle_slider = ttk.Scale(root, from_=0, to=360, orient='horizontal', command=lambda event: update_cube())
angle_slider.grid(row=2, column=1, columnspan=3, sticky="ew")

# Обновление канваса
canvas_frame = ttk.Frame(root)
canvas_frame.grid(row=3, column=0, columnspan=4)

root.mainloop()
