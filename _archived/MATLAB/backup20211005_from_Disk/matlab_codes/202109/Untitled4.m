syms t w s

f = sin(t) + sin(2.5*t);

F = fourier(f, t, w);
L = laplace(f, t, s);

ezplot(F);
ezplot(L);

disp(F)
disp(L)
