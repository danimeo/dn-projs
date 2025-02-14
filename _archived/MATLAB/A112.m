clc; clear all; close all

%次数
n = 3;

% 将已知数据记为
T = (1:8)' * 5;
Y = [1.27 2.16 2.86 3.44 3.87 4.15 4.37 4.51]' * 1e-4;

x = sym('x',[1 length(T)]);

% 取基函数φ
phi = @(x, n) x .^ n;

% 对每个ti，有
phi_ = arrayfun(@(x) phi(x,0:n), x, 'UniformOutput', false);
disp(phi_)

% 设a = [a0 a1 a2 a3]'为各项系数，则拟合多项式为y = sum(...)

% 把每个已知的x代入，将得到的方程组记为矩阵A
A = reshape(cell2sym(phi_), n+1, length(T))';
disp(A)

% AA'=
B = A'*A;
disp(B)

% y_=
size(A')
size(Y)
y_ = A' * Y;
disp(vpa(subs(y_, x, T')))

% 解线性方程组(AA')a=y_
a = eval(subs(B, x, T')) \ eval(subs(y_, x, T'));
disp(a)

% 代入并输出结果
x0 = phi(sym('x'), 0:n);
disp(x0)
y = vpa(sum(a' .* x0));
disp(y)

fplot(y)
hold on
plot(T, Y, 'ro')
