import control
from control import tf, series, parallel, feedback, step_response, dcgain
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一(替换sans-serif字体)
plt.rcParams['axes.unicode_minus'] = False   # 原文出自【易百教程】，商业转载请联系作者获得授权，非商业请保留原文链接：

from mpl_toolkits import mplot3d

from pdfo import pdfo, Bounds

from scipy.optimize import minimize, fmin


# (2) ①
Ke=6.0/((math.pi/30)*1e3)
Kt=57.3e-3
Ra=1.00
Jm=0.325e-4
JL=16*Jm
J=JL+Jm

Km=1/Ke
Tm=Ra*J/(Ke*Kt)
M=tf(Km, [Tm, 1])
# t, y = step_response(M)
# plt.plot(t, y)
# plt.show()

# (2) ②
KOmN=1/(math.pi/30)
n0=4000
KV=n0/(Km*KOmN)

V=KV
OmN=KOmN
# sys=V*M*OmN
# t, y = step_response(sys)
# plt.plot(t, y)
# plt.show()

t = np.arange(0, 1.0, 0.000001)
sys = V*M*OmN
t, out = step_response(sys, t)
# step(sys)
ystable = dcgain(sys) # 稳态值
outmax = np.max(out) # 获取最大值的点的数据
if outmax > ystable:
    idx=0
    i_min=0
    while out[idx] < ystable: # 过滤小于稳态值的
        idx=idx+1
else:
    idx=0
    i_min=0
    while out[idx] < outmax*0.9: # 过滤小于90%的
        if out[idx] <= outmax*0.1 and out[idx+1] > outmax*0.1: # 过滤大于10%的
            i_min=idx+1
        idx=idx+1

tropen = t[idx]-t[i_min] # 上升时间
print(f'tropen={tropen}')
# tropen = 0.369758

# (3)
KF=2.0/((math.pi/30)*1e3)
Uf=1.0

# ①确定KA：
KA=Uf/(KF*(n0*(math.pi/30)))

forw=V*M
back=KF*KA
tail=KOmN
ns=n0

t=np.arange(0, 0.1, 0.001)

orig = (10.2, 5.9)
stp = 0.001
span = 5


def func(x):
    kp, ki = x
    global tropen, ns, forw, back, tail, t
    sys=feedback(tf([kp, kp*ki],[1, 0])*forw, back, -1)*tail
    t, out = step_response(sys, t)
    ystable = dcgain(sys) # 稳态值
    outmax = np.max(out) # 获取最大值的点的数据

    idx=0
    i_min=0
    while out[idx] < outmax*0.9: # 过滤小于90%的
        if out[idx] <= outmax*0.1 and out[idx+1] > outmax*0.1: # 过滤大于10%的
            i_min=idx+1
        idx=idx+1
    
    R = t[idx]-t[i_min] # 上升时间
    Z = abs(tropen * 0.1 - R)*1e3
    
    return Z


# fig = plt.figure()

# for i_gen in range(20):
#     if i_gen == 0:
#         Xmin=max(0.00001, orig[0]-stp*span)
#         Xmax=orig[0]+stp*span
#         Ymin=max(0.00001, orig[1]-stp*span)
#         Ymax=orig[1]+stp*span
    
#     X=np.arange(Xmin, Xmax, stp)
#     Y=np.arange(Ymin, Ymax, stp)
#     t=np.arange(0, 0.1, 0.001)
#     z=np.zeros((X.shape[0], Y.shape[0]))
#     rise=np.zeros_like(z)
#     for j in range(len(Y)):
#         for i in range(len(X)):
#             sys=feedback(tf([X[i], X[i]*Y[j]],[1, 0])*VM, KFKA, -1)*OmN
#             t, out = step_response(sys, t)
#             ystable = dcgain(sys) # 稳态值
#             outmax = np.max(out) # 获取最大值的点的数据
#             if outmax > ystable:
#                 idx=0
#                 i_min=0
#                 while out[idx] < ystable: # 过滤小于稳态值的
#                     idx=idx+1
#             else:
#                 idx=0
#                 i_min=0
#                 while out[idx] < outmax*0.9: # 过滤小于90%的
#                     if out[idx] <= outmax*0.1 and out[idx+1] > outmax*0.1: # 过滤大于10%的
#                         i_min=idx+1
#                     idx=idx+1
            
#             rise[i,j] = t[idx]-t[i_min] # 上升时间
#             z[i,j] = abs(tropen * 0.1 - rise[i,j]) + abs(ns - out[-1])/ns
            
x0 = [5, 5]
# bounds = Bounds([0.00001, 0.00001], [np.inf, np.inf])
# res = pdfo(func, x0, bounds=bounds, method='cobyla', options={'maxfev': 100, 'ftarget': 1e-4})
# print(res['x'])

res = minimize(func, x0 , args=(), jac=None, method='Nelder-Mead', options={'disp': True},constraints=None, tol=1e4)
# res = fmin(func, x0)
# args是传递给目标函数和偏导的参数，此例中为1，求min问题。args=-1时是求解max问题
print(res.x)

Kp, Ki = res.x.tolist()

sys=feedback(tf([Kp, Kp*Ki],[1, 0])*V*M, KF*KA, -1)*OmN;
print(sys)
t=np.arange(0, 2, 0.01)
t, out = step_response(sys, t)

ystable = dcgain(sys) # 稳态值
outmax = np.max(out) # 获取最大值的点的数据
if outmax > ystable:
    idx=0
    i_min=0
    while out[idx] < ystable: # 过滤小于稳态值的
        idx=idx+1
else:
    idx=0
    i_min=0
    while out[idx] < outmax*0.9: # 过滤小于90%的
        if out[idx] <= outmax*0.1 and out[idx+1] > outmax*0.1: # 过滤大于10%的
            i_min=idx+1
        idx=idx+1

R = t[idx]-t[i_min] # 上升时间
print(f'rise: {R} error: {tropen*0.1 - R} error(%): {{:.2f}}%'.format(abs(tropen*0.1 - R)*100/(tropen*0.1)))

plt.plot(t, out)
plt.show()

    # p, q = np.where(z==np.min(z))
    # if p and q:
    #     p=p[0]
    #     q=q[0]

    #     Xmin = max(0.00001, X[p] - stp*span)
    #     Xmax = X[p] + stp*span
    #     Ymin = max(0.00001, Y[q] - stp*span)
    #     Ymax = Y[q] + stp*span
    #     print(f'Gen: {i_gen}, Kp={X[p]}, Ki={Y[q]}, rise={rise[p, q]}')
        
    #     sys=feedback(tf([X[p], X[p]*Y[q]],[1, 0])*VM, KFKA, -1)*OmN
    #     print(sys)
    
    #     # t, y = step_response(M)
    #     # plt.plot(t, y)
    #     # plt.show()
        
    #     x, y=np.meshgrid(X, Y)
    #     ax = plt.axes(projection='3d')
    #     print(x.T.shape, y.T.shape, z.shape)
    #     ax.plot_surface(x.T, y.T, z, cmap='viridis', edgecolor='none')
    #     plt.show()
