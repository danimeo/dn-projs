using LinearAlgebra

# readline()
a = [2 5 6]
d = a[1]
gcd(a, b) = b == 0 ? a : gcd(b, a % b)

for i in 2:length(a)
    global d, a
    d = gcd(d, a[i])
end

N = 1:100
n_has_roots = count(N -> N % d == 0, N)

println(a)
println(d)

println(n_has_roots, "/", length(N))
