import control
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
axes1 = fig.add_subplot(111)
g = control.tf([1], [1, 1])
t, res = control.step_response(g, np.arange(0, 15, 0.05))
line, = axes1.plot(t, res)


def update(data):
    line.set_xdata(data[0])
    line.set_ydata(data[1])
    return line,


def data_gen():
    for i in np.arange(0, 1.5, 0.05):
        g = control.tf([1], [1, i])
        t, res = control.step_response(g, np.arange(0, 15, 0.05))
        yield t, res


ani = animation.FuncAnimation(fig, update, data_gen, interval=200)
plt.show()
