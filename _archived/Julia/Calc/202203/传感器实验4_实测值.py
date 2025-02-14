from math import log, sqrt, pi

while True:
    n = float(input('n: '))
    M_i = float(input('M_i: '))
    M_in = float(input('M_i+n: '))
    f_d = float(input('f_d: '))


    xi = log(M_i / M_in) / (2*pi*n)
    omega_n = (2*pi) * f_d / sqrt(1 - xi**2)
    f_n = omega_n / (2*pi)
    print(f'ξ={xi}\nω_n={omega_n}\nf_n={f_n}')
