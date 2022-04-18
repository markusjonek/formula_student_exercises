import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider


class Animator(FuncAnimation):
    """ Inherites the capabilities of FuncAnimation with extra features.
    Buttons for start, stop and save figure.
    Slider for quick scroll through x-values.
    Button to save the figure with custom name. """
    def __init__(self, fig, plot_function, x_min, x_max):
        self.fig = fig
        self.plot_function = plot_function
        self.x_min = x_min
        self.x_max = x_max
        self.i = x_min
        self.runs = True

        widget_y_pos = 0.9
        button_width = 0.08
        widget_height = 0.05

        # start button
        startax = plt.axes([0.13, widget_y_pos, button_width, widget_height])
        self.start_button = Button(startax, label='$\u25B6$')
        self.start_button.on_clicked(self.start)

        # stop button
        stopax = plt.axes([0.22, widget_y_pos, button_width, widget_height])
        self.stop_button = Button(stopax, label='$\u25A0$')
        self.stop_button.on_clicked(self.stop)

        # slider
        slideax = plt.axes([0.33, widget_y_pos, 0.3, widget_height])
        self.slider = Slider(slideax, '', self.x_min, self.x_max, valinit=self.i)
        self.slider.on_changed(self.set_pos)

        FuncAnimation.__init__(self, self.fig, self.update_slider, frames=self.frame_updater(), interval=15)

    def frame_updater(self):
        """ Responsible for what happens between frames. Stops the slider if it reaches x_max. """
        while self.runs:
            if self.i >= self.x_max:
                self.stop()
            yield self.i
            self.i += 1

    def start(self, event=None):
        """ Starts the plot. Replays from start if the plot has reached the end. """
        if self.i < self.x_max:
            self.runs=True
            self.event_source.start()
        if self.i == self.x_max:
            self.i = self.x_min

    def stop(self, event=None):
        """ Stops the plot """
        self.runs = False
        self.event_source.stop()

    def set_pos(self, i):
        """ Gives the command to the given plot_funtion to plot up until the slider value. """
        self.i = int(self.slider.val)
        self.plot_function(self.i)

    def update_slider(self, i):
        """ Updates the slider position as the animation is running. """
        self.slider.set_val(i)


class Plot:
    """ Class for plotting a function """
    def __init__(self, dim, grid_button=True, save_button=True):
        self.x_min = dim[0]
        self.x_max = dim[1]
        self.y_min = dim[2]
        self.y_max = dim[3]

        self.fig, self.ax = plt.subplots()
        self.point, = self.ax.plot([], [])
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        if grid_button:
            self.add_grid_button()

        if save_button:
            self.add_save_button()

    def add_grid_button(self):
        """ Adds grid on/off button. """
        gridax = plt.axes([0.72, 0.9, 0.08, 0.05])
        self.grid_button = Button(gridax, label='#')
        self.grid_button.on_clicked(self.grid)
        self.n = 1

    def grid(self, event=None):
        """ Adds/turns off grid"""
        self.fig.canvas.draw_idle()
        if self.n % 2:
            self.ax.grid(True)
        else:
            self.ax.grid(False)
        self.n += 1

    def add_save_button(self):
        """ Adds save button. """
        saveax = plt.axes([0.82, 0.9, 0.08, 0.05])
        self.save_button = Button(saveax, label='Save')
        self.save_button.on_clicked(self.save_figure)
        self.file_index = 1

    def save_figure(self, event=None):
        """ Saves the current figure (image) with a unique index, ex. "figure5". """
        file_names = os.listdir('./')
        indexes = []
        for file_name in file_names:
            if file_name[0:6] == "figure":
                indexes.append(int(file_name[6]))
        if len(indexes) == 0:
            index = "1"
        else:
            index = str(max(indexes) + 1)

        plt.savefig("figure" + index + ".png")

    def color_bar(self):
        """ Adds color-picker-bar """
        blueax = plt.axes([0.25, 0.06, 0.08, 0.05])
        self.blue_button = Button(blueax, label="", color="blue", hovercolor="blue")
        self.blue_button.on_clicked(self.blue_line)

        greenax = plt.axes([0.45, 0.06, 0.08, 0.05])
        self.green_button = Button(greenax, label='', color="green", hovercolor="green")
        self.green_button.on_clicked(self.green_line)

        redax = plt.axes([0.65, 0.06, 0.08, 0.05])
        self.red_button = Button(redax, label='', color="red", hovercolor="red")
        self.red_button.on_clicked(self.red_line)

    def blue_line(self, event=None):
        """ changes line to blue"""
        self.fig.canvas.draw_idle()
        self.ax.plot(self.x_simple, self.y_simple, color="blue")

    def green_line(self, event=None):
        """ changes line to green """
        self.fig.canvas.draw_idle()
        self.ax.plot(self.x_simple, self.y_simple, color="green")

    def red_line(self, event=None):
        """ changes line to red """
        self.fig.canvas.draw_idle()
        self.ax.plot(self.x_simple, self.y_simple, color="red")

    def plot_function(self, i):
        """ The function to run at each update in the animation """
        x_values = np.linspace(self.x_min, i, abs(i * 100) + 2000)
        y_values = self.math_func(x_values)  # *pi/180 for plot in degrees
        self.point.set_data(x_values, y_values)

    def live_animate(self, math_func, line_color="blue"):
        """ Animates the plot_funtion """
        self.math_func = math_func
        self.point, = self.ax.plot([], [], color=line_color)
        animation = Animator(self.fig, self.plot_function, self.x_min, self.x_max)
        plt.show()

    def simple_plot(self, math_func, line_color="blue"):
        """ plots the whole function at once, also adds the color bar"""
        self.x_simple = np.linspace(self.x_min, self.x_max, 2000 + (self.x_max - self.x_min) * 100)
        self.y_simple = math_func(self.x_simple)
        self.ax.plot(self.x_simple, self.y_simple, color=line_color)
        plt.subplots_adjust(bottom=0.2)
        self.color_bar()
        plt.show()


def h(t):
    return 3 * np.pi * np.exp(-5 * np.sin(2 * np.pi * t * np.pi / 180))


def g(t):
    return 200 * np.sin(t / 20) + t


def main():
    plot = Plot([-500, 1000, -500, 2000], grid_button=True, save_button=True)
    functions = {"simple": plot.simple_plot, "live": plot.live_animate}
    try:
        functions[sys.argv[1]](h, sys.argv[2])
    except (KeyError, ValueError, IndexError):
        print('Choose "live" or "simple" as function and a valid matplotlib-color.')


main()
