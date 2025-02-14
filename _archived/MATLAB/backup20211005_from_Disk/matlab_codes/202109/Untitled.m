syms x y;
tic;
y = sin(x^2 + 1/x) + x / exp(x)^2;
d = diff(y, x);
disp(d);
toc;