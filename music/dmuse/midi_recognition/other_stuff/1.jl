using LinearAlgebra
using Plots

println.(1:100);
x = -5:0.1:5
y = sin.(x)


a = reshape(1:9, 3, 3)
println(collect(a))
collect(a')

plot(x, y)
