using Symbolics
using Plots

次数 = 3
X_ = collect(5:5:40)
Y_ = vec([1.27 2.16 2.86 3.44 3.87 4.15 4.37 4.51] * 1e-4)

@variables x[0:length(X_)]
ϕ(n, k) = x[k]^n
A = [ϕ(n, k) for n in 0:次数, k in 1:length(X_)]'
B = A' * A

B0 = substitute(B, Dict(x[i[1]]=>i[2] for i = zip(1:length(X_), X_)))
println(Symbolics.value.(B0))

y0 = A' * Y_
println("\ny0=", Symbolics.value.(substitute(y0, Dict(x[i[1]]=>i[2] for i = zip(1:length(X_), X_)))))

a = B \ y0
a0 = Symbolics.value.(substitute(a, Dict(x[i[1]]=>i[2] for i = zip(1:length(X_), X_))))
println("\na=", a0)

inspectdr()
plot(X_, Y_, shape=:circle, markercolor=:red, linecolor=nothing, title="工程计算方法第三次作业", label="已知点")

X0 = collect(0:0.2:100)
Y0 = vec(sum([a0[i+1] * X0 .^ i for i = 0:次数]))

plot!(X0, Y0, color=:blue, label="拟合多项式曲线")
