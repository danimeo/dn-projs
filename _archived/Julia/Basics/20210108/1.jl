using Base.MathConstants

f(x) = x + 5x + sin(pi / 6)

g(x) = (3 // 5)x - 1 // 2

h = [f g]

for a = h
    println("这是我的第一个Julia程序。\n代入运算结果为：", a(2//3))
end

#for n = 1:100000000
#    println(n)
#end
