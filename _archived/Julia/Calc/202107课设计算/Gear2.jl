m = 3
z = 120
α = 20
d = m * z
ha_star = 1.0
c_star = 0.25

ha = ha_star * m
hf = (ha_star + c_star) * m
h = ha + hf
da = d + 2ha
df = d - 2hf
db = d * cos(deg2rad(α))
p = π * m
s = e = p / 2
θ = p / (π * d) * 360


