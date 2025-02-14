M = 10
V_0 = 1
V_1 = 2
V_2 = 3
V_3 = 4

K2 = (V_1^2+V_2^2+V_3^2+3V_0^2) / (3M^2)
m_x = (V_1^2-V_2^2) / (2M*K2) - 1/2*M
m_y = 1/(2*sqrt(3)*M*K2)*(V_2^2+V_3^2)
m = sqrt(m_x^2 + m_y^2)
α = atan(m_y/m_x)
@show K2, m_x, m_y, m, α;
