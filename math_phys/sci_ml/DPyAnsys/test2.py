import time
import numpy as np
from ansys.mapdl.core import launch_mapdl
from threading import Thread

mapdl = launch_mapdl()
print(mapdl)
mapdl.title('Dajun')

mapdl.prep7()
rect_anum = mapdl.blc4(width=1, height=0.2)
for x in np.linspace(0.1, 0.9, 8):
    mapdl.cyl4(x, 0.1, 0.025)
# mapdl.lplot(color_lines=True, cpos='xy')
plate_holes = mapdl.asba(rect_anum, 'all')
mapdl.vext(plate_holes, dz=0.1)
# mapdl.vplot()

mapdl.et(1, 'SOLID186')
mapdl.vsweep('ALL')
mapdl.esize(0.1)
mapdl.nropt('FULL')


def loop():
    for i in range(1, 11):
        mapdl.ekill(i)
        mapdl.esel('s', 'live')
        time.sleep(1)
    mapdl.eplot()


thread = Thread(target=loop, args=())
thread.start()
thread.join()
# mapdl.eplot()
