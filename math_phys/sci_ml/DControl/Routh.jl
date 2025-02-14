# p = Float32[1 8 17 16 5]  # 闭环特征方程的系数
# p = Float32[1 2 1 2 1]  # 闭环特征方程的系数
p = Float32[1 2 8 12 20 16 16]  # 闭环特征方程的系数

m = length(p)
n = Int(ceil(length(p) / 2))
routh = zeros(Float32, m, n)
r = [p[1:2:m], p[2:2:m]]
for i in 1:m
    if i < 3
        routh[i, 1:length(r[i])] = r[i]
    else
        for j in 1:n-1
            routh[i, j] = (routh[i-1, j] * routh[i-2, j+1] - routh[i-2, j] * routh[i-1, j+1]) / routh[i-1, j]
            if routh[i, j] == 0
                routh[i, j] = eps(Float32)
            end
        end
    end
    for j in 1:n
        if routh[i, j] != 0 && ! isnan(routh[i, j])
            print(routh[i, j], "\t")
        end
    end
    println()
end

if findfirst(x -> x<0, routh[:, 1]) === nothing
    println("系统稳定")
elseif findfirst(isequal(0), routh[:, 1]) !== nothing
    println("系统处于临界稳定状态")
else
    println("系统不稳定")
end
