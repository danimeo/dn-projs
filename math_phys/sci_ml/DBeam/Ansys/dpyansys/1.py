import numpy as np
import matplotlib.pyplot as plt

hflux = np.zeros((27, 7))


def fnc(a, b, lst):
    for i in range(hflux.shape[-1]):
        hflux[b, i] = lst[i]


'''fnc(0,0,[0.0, -999, 0, 0, 0, 0, 0])
fnc(2,0,[0.0, 0, 0, 0, 0, 0, 0])
fnc(3,0,[0.0, 0, 0, 0, 0, 0, 0])
fnc(4,0,[0.0, 0, 0, 0, 0, 0, 0])
fnc(5,0,[0.0, 0, 0, 0, 0, 0, 0])
fnc(6,0,[0.0, 0, 0, 0, 0, 0, 0])'''
fnc(0,1,[1.0, -1, 0, 0, 0, 0, 0])
fnc(0,2,[0.0, -2, 0, 1, 0, 0, -1])
fnc(0,3,[  0, -3, 0, 1, -1, 2, -2])
fnc(0,4,[0.0, -1, 0, 3, 0, 0, -3])
fnc(0,5,[0.0, -2, 0, 1, -3, 3, -1])
fnc(0,6,[0.0, -1, 0, 0.03, 0, 0, 3])
fnc(0,7,[0.0, -3, 0, 1, 3, 2, -1])
fnc(0,8,[0.0, -1, 0, 2, 0, 0, -3])
fnc(0,9,[0.0, -4, 0, 1, -3, 17, -1])
fnc(0,10,[0.0, -1, 0, 0.02, 0, 0, 2])
fnc(0,11,[0.0, -3, 0, 1, 2, 2, -1])
fnc(0,12,[0.0, -1, 0, 0.02, 0, 0, 1])
fnc(0,13,[0.0, -5, 0, 1, -1, 3, 1])
fnc(0,14,[0.0, -1, 0, 1, -3, 2, -5])
fnc(0,15,[0.0, -3, 0, 2, 0, 0, -1])
fnc(0,16,[0.0, -5, 0, 1, -1, 17, -3])
fnc(0,17,[0.0, -1, 0, 1, -4, 1, -5])
fnc(0,18,[0.0, -3, 0, 1, -2, 3, -1])
fnc(0,19,[0.0, -1, 0, 0.005, 0, 0, 0])
fnc(0,20,[0.0, -2, 0, 2, 0, 0, -1])
fnc(0,21,[0.0, -4, 0, 1, -1, 17, -2])
fnc(0,22,[0.0, -1, 0, 1, -3, 4, -4])
fnc(0,23,[0.0, -1, 7, 1, -1, 0, 0])
fnc(0,24,[0.0, -2, 0, 4e7, 0, 0, -1])
fnc(0,25,[0.0, -3, 0, 1, -2, 3, -1])
fnc(0,26,[0.0, 99, 0, 1, -3, 0, 0])

print(hflux)

hf = np.zeros((27, 7))

for x in np.arange(0, 26):
    for y in np.arange(0, 6):
        pass


plt.imshow(hflux, interpolation='bicubic', cmap='bone', origin='lower')

plt.show()
