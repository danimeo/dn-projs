from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sounddevice as sd
from scipy.signal import resample
import librosa
import queue
from ssqueezepy import ssq_stft

device_id = 19
channel = 2
device_info = sd.query_devices(device_id, 'input')
print(device_info)
sample_rate = device_info['default_samplerate']

app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
# pg.setConfigOptions(antialias=True)
# pg.setConfigOptions(imageAxisOrder='row-major')


p6 = win.addPlot(title="Updating plot")
#curve = p6.plot(pen='y')

imv = pg.ImageView()
colors = [
    (0, 0, 0),
    (45, 5, 61),
    (84, 42, 55),
    (150, 87, 60),
    (208, 171, 141),
    (255, 255, 255)
]
cmap = pg.ColorMap(pos=np.linspace(0., 1., 6), color=colors)
imv.setColorMap(cmap)

q = queue.Queue()


def audio_callback(indata, frames, time, status):
    q.put(indata)


def update():
    global curve, q, p6
    data = librosa.to_mono(resample(q.get_nowait().transpose((1, 0)), 1000))
    dat, _, *_ = ssq_stft(data)
    print(np.abs(dat)[:10, 0])
    imv.setImage(np.abs(dat))
    plot_data = data
    #curve.setData(plot_data)


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


if __name__ == '__main__':
    stream = sd.InputStream(
    device=device_id, channels=channel,
    samplerate=sample_rate, callback=audio_callback)
    with stream:
        pg.exec()
