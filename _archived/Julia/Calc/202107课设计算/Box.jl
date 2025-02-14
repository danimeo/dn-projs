a = (60.0 + 360.0) / 2
da1, da2 = 66.0, 366.0
ha1, ha2 = 3.0, 3.0
ra1, ra2 = da1 / 2, da2 / 2

δ = 0.025a + 1
δ1_range = 0.8δ, 0.85δ
δ1 = δ1_range[1]
b = 1.5δ
b1 = 1.5δ1
b2 = 2.5δ
df = 0.036a + 12
n = a < 250 ? 4 : (250 <= a <= 500 ? 6 : 8)
d1 = 0.75df
d2_range = 0.5df, 0.6df
d2 = d2_range[1]
l_range = 150, 200
d3 = 0.4df, 0.5df
d4 = 0.3df, 0.4df
d = 0.7d2, 0.8d2
C1 = 22
C2 = 20
R1 = C2
h = missing # 根据低速轴轴承外径确定
l1_range = C1 + C2 + 5, C1 + C2 + 8

Δ1 = 4.0δ
Δ2 = 40
Δ3_range = 10, 12 # 脂润滑时10～12，油润滑时3～5
Δ3 = 4
Δ4_range = 10, 15
Δ4 = Δ4_range[1]
Δ5 = 10
Δ6_range = 30, 50
Δ6 = (Δ6_range[1] + Δ6_range[2]) / 2 # 取40
Δ7_range = δ + 3, δ + 5
Δ7 = δ + 3.25
H = ra2 + Δ6 + Δ7
L1_range = δ + C1 + C2 + 5, δ + C1 + C2 + 8
L1 = L1_range[1]
e = missing
L2 = missing
L3 = missing

Lx = 2(δ + Δ1) + 2a + ha1 + ha2
Ly = 60.0 + 2(δ + Δ2)

param1 = ra1 + Δ1 + δ
param2 = ra2 + Δ1 + δ
