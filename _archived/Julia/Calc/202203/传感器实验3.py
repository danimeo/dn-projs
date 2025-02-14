from math import sqrt, atan, degrees

# M = float(input('M: '))
# _V_0 = [float(s) for s in input('V_0: ').split()]
# _V_1 = [float(s) for s in input('V_1: ').split()]
# _V_2 = [float(s) for s in input('V_2: ').split()]
# _V_3 = [float(s) for s in input('V_3: ').split()]

M = 4.959
_V_0 = [0.156, 0.200, 0.417]
_V_1 = [0.299, 3.076, 9.210]
_V_2 = [0.506, 3.206, 9.550]
_V_3 = [0.498, 3.440, 12.233]

for V_0, V_1, V_2, V_3 in zip(_V_0, _V_1, _V_2, _V_3):
    K2 = (V_1**2+V_2**2+V_3**2+3*V_0**2) / (3*M**2)
    m_x = (V_1**2-V_2**2) / (2*M*K2) - 1/2*M
    m_y = 1/(2*sqrt(3)*M*K2)*(V_2**2+V_3**2)
    m = sqrt(m_x**2 + m_y**2)
    alpha = degrees(atan(m_y/m_x))
    print(f'K2={K2}, m_x={m_x}, m_y={m_y}, m={m}, α={alpha}°')
