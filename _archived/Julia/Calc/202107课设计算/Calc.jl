function ceilto05(x)
    floored = floor(x)
    if 0 <= x - floored < 0.5
        return floored + 0.5
    else
        return floored + 1.0
    end
end

F = 4200
D = 380
n = 40
allowed_Δn = 0.05n

vw = π * n * D / (60 * 1000)
Pw = F * vw / 1000
η1, η2, η3, η4, η5 = 0.96, 0.98, 0.99, 0.99, 0.96
η = η1 * η2 * η3^2 * η4 * η5
Pd = Pw / η
P = 4
n0 = 730

i = n0 / n
i2 = 6
i1 = i / i2
nⅠ = n0 / i1
nⅡ = n
nⅢ = nⅡ
PⅠ = P * η1
PⅡ = PⅠ * η2 * η3
PⅢ = PⅡ * η3 * η4 * η5
Td = 9550 * P / n0
TⅠ = Td * i1 * η1
TⅡ = TⅠ * i2 * η2 * η3
TⅢ = TⅡ * η3 * η4 * η5

P0 = 4.00
ΔP0 = 0.22
dp1 = 250
dp2 = dp1 * i1
v = π * dp1 * n0 / (60 * 1000)
a0_range = 0.7(dp1 + dp2), 2(dp2 + dp1)
a0 = 750
L0 = 2a0 + π/2 * (dp1 + dp2) + ((dp2 - dp1)^2) / 4a0
Ld = 3200
a = a0 + (Ld - L0) / 2
a_range = a - 0.015Ld, a + 0.03Ld
α1 = 180 - ((dp2 - dp1) / a) * 57.3
KA = 1.2
Pc = KA * P
Kα = 0.89
KL = 1.07
_P0_ = (P0 + ΔP0) * Kα * KL
z = round(Pc / _P0_)
q = 0.170
F0 = 500 * Pc / (z * v) * (2.5 / Kα - 1) + q * v^2
FQ1 = 2 * z * F0 * sin(deg2rad(α1 / 2))

z1 = 20
z2 = z1 * i2
β = 8
φd = 1.0
K = 1.2
T1 = 9.55 * 10^6 * (PⅠ / nⅠ)
u = z2 / z1
ZE = 189.8
Zβ = cos(deg2rad(β)) ^ (1 / 2)
σH_lim = 710
SH = 1.2
_σH_ = σH_lim / SH
d1_ = 2.32 * (K * T1 / φd * (u + 1) / u * (ZE * Zβ / _σH_)^2) ^ (1 / 3)
m0 = d1_ / z1
m = round(m0)
d1 = m * z1
d2 = m * z2

A0_Ⅰ = 112
dⅠ_ = A0_Ⅰ * (PⅠ / nⅠ) ^ (1 / 3)
# dⅠ = ceilto05(dⅠ_)
dⅠ = 44

A0_Ⅱ = 103
dⅡ_ = A0_Ⅱ * (PⅡ / nⅡ) ^ (1 / 3)
# dⅠ = ceilto05(dⅠ_)
dⅡ = missing

