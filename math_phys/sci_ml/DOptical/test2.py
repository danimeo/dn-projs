from tkinter import *
import PIL as pl
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

def spatial_sin(x, dim_x, f):
    return np.fromiter((sin_x(i%dim_x, dim_x, f) for i, xi in enumerate(x)), x.dtype)

def sin_x(x, dim_x, f):
    return (0.5*(np.sin(2*np.pi*x*f/dim_x)+1))

def spatial_sin_exp(x, dim_x, f0):
    return np.fromiter((sin_x_fx(i%dim_x, dim_x, f0) for i, xi in enumerate(x)), x.dtype)

def sin_x_fx(x, dim_x, f0):
    f = f0*np.exp(2*x/(dim_x-1))
    return 0.5*(np.sin(2*np.pi*x*f/(dim_x-1))+1)

def spatial_sin_exp_contrast(x, dim_x, dim_y, f0, cmin, cmax):
    return np.fromiter((sin_x_fx_cy(i%dim_x, dim_x, f0, np.floor(i/dim_x), dim_y, cmin, cmax) for i, xi in enumerate(x)), x.dtype)

def sin_x_fx_cy(x, dim_x, f0, y, dim_y, cmin, cmax, inc_f = 2.1, inc_c = 2):
    f = f0*np.exp(inc_f*x/(dim_x))
    #c = np.minimum(cmax,np.maximum(cmin,np.exp(inc_c*(y-(dim_y-1))/(dim_y-1))))
    c = cmax*np.exp(np.log(cmin/cmax)*((dim_y)-y)/(dim_y))
    return 0.5*(np.sin(2*np.pi*x*f/(dim_x-1))+1)*c+(1-c)/2

def norm_L(L1, L2):
    return (L1/(L1+L2)), (L2/(L1+L2))



root = Tk()
root_panel = Frame(root)
root_panel.pack(side="bottom", fill="both", expand="yes")

x = 1024
y = 768
img_arr = np.ones(shape = (x*y), dtype = np.float32)
# print([np.exp(i/(x-1)) for i, xi in enumerate(img_arr[0:512])])
img_arr = spatial_sin_exp_contrast(img_arr, x, y, 2, 0.1, 0.7)
#img_arr = spatial_sin_exp(img_arr, x,2)
img_arr = np.reshape(img_arr, (y,x))
contr = []
for row in img_arr:
    contr.append((np.max(row)-np.min(row))/(np.max(row)+np.min(row)))
plt.plot(contr)
plt.show()
img = pl.Image.fromarray(np.uint8(img_arr*255), mode = "L")


img_tk = ImageTk.PhotoImage(img)
img_panel = Label(root_panel)
img_panel.configure(image=img_tk)
img_panel.pack(side="bottom", fill="both", expand="yes")

root.mainloop()
