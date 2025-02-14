import numpy as np

from apdl_wrapper import *

finish()

title('Dajun')

prep7()
rect_anum = blc4(0, 0, 1, 0.2)
for x in np.linspace(0.1, 0.9, 8):
    cyl4(x, 0.1, 0.025)

plate_holes = asba(rect_anum, ALL)
vext(all, 0, 0, 0, 0, 0.1)


et(1, 'SOLID186')
vsweep(ALL)
esize(0.1)
nropt(FULL)


for i in range(1, 11):
    ekill(i)
    esel(S, LIVE)
    # time.sleep(1)

eplot()
    
save_log('output1.mac')

