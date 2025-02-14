from ansys.mapdl.core import launch_mapdl
import matplotlib.pyplot as plt
import numpy as np
import os


os.system('TASKKILL /F /IM ANSYS.exe')

mapdl = launch_mapdl(run_location=r'C:\dev_spa\dbeam\pyansys\202111', override=True)

elem_size = 0.001, 0.00025
duration = 1.0
n_substeps = 5
powd = 0.002
a, b, c = 0.1, 0.06, 0.008

mapdl.prep7()
# mapdl.block(0, 0.1, 0, 0.06, -0.008 - powder_thickness, - powder_thickness)
# mapdl.block(0, 0.1, 0, 0.06, -powder_thickness, 0)

'''keypoints = [
    (0, 0, powd),
    (a, 0, powd),
    (a, b, powd),
    (0, b, powd),
    (0, b, -c),
    (0, 0, -c),
    (a, 0, -c),
    (a, b, -c),
]
for keypoint in keypoints:
    mapdl.k(*keypoint)
mapdl.v(*tuple(range(1, 9)))'''
mapdl.block(0, 0.1, 0, 0.06, -0.008, powd)
mapdl.vsbw(1)
mapdl.vplot()

mapdl.mptemp(1, 300)
mapdl.mpdata('ex', 1, 1, 2.0e11)
mapdl.mp('dens', 1, 7850)
mapdl.mp('alpx', 1, 1.23e-5)
mapdl.mp('nuxy', 1, 0.3)
mapdl.mp('kxx', 1, 33)
mapdl.mp('c', 1, 561)
mapdl.mp('murx', 1, 1)
mapdl.mp('reft', 1, 300)

mapdl.et(1, 'solid70')
mapdl.et(2, 'solid70')

print('正在划分网格……')
mapdl.
mapdl.allsel()

# mapdl.lsclear('all')

# mapdl.esel('s', 'cent', 'z', -elem_size, 0)

mapdl.eplot()
exit()


mapdl.finish()

heat_source_def = """
*DEL,_FNCNAME
*DEL,_FNCMTID
*DEL,_FNCCSYS
*SET,_FNCNAME,'HFLUX'
*SET,_FNCCSYS,0
"""

apply_loads = """
/solu
sfe, all, , hflux, , %HFLUX%
"""

mapdl.run_multiline(heat_source_def)
mapdl.input(r'B:\codes\ds\DBeam\Ansys\ghs.func', '', '', 1)

mapdl.slashsolu()
mapdl.sfe('all', '', 'hflux', '', '%HFLUX%')

mapdl.antype('4')
mapdl.outres('all', 'all')
mapdl.kbc(1)
mapdl.timint('on')
mapdl.tintp(0.005, 0, 0, 1, 0.5, 0.2)
mapdl.autots('off')

mapdl.time(duration)
mapdl.nsubst(n_substeps, n_substeps, n_substeps)
print('正在求解……')
mapdl.solve()
print('求解完成')

mapdl.finish()
mapdl.post1()

imgs = []
ratio = 0.4

for step in range(n_substeps):
    mapdl.set(1, step + 1)
    plotter = mapdl.post_processing.plot_nodal_temperature(return_plotter=True)
    plotter.add_title('Electron Beam Simulation 2021.11', font='arial')
    img = plotter.show(jupyter_backend='matplotlib', return_viewer=True)
    arr = np.array(img)
    width, height = int(arr.shape[1] * ratio), int(arr.shape[0] * ratio)
    imgs.append(np.array(img.resize((width, height))))
    # plt.imshow(img)
    # plt.show()

plt.imshow(imgs[-1])
plt.show()
