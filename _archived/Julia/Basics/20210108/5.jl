println("Hello:")
a = readline(stdin)
println(a)

neurons = Dict{Int32, Expr}

macro f(x)
    :(x ^ 2)
end

for i = 1:100
    global f
    neurons[i] = Expr(:f, :*, :2)
end

for i = 1:10
    println(neurons[i])
end
