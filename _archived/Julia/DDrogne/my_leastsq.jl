using Plots: plot

f(x) = 2x^3 - x^2 + x + 8

x = -5:0.1:5
y = f.(x) + randn(Float64, size(x))
println(y)

plot(x, y)
