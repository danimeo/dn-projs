from math import log, sqrt, pi

while True:
    L = float(input('L: '))
    d = float(input('d: '))
    
    E = 2.1e11
    rho = 7800

    I = pi * d**4 / 64
    S = pi * (d/2)**2
    
    f_gu = 3.515 / (2*pi) *sqrt(E * I / (rho * S * L))
    print(S, I)
    print(f'f固={f_gu}')
