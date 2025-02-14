syms a1 a2 a3 x1 x2 x3 d1 d2 d3 t1 t2 t3 k1 k2 k3 N

a = [a1 a2 a3];
x = [x1 x2 x3];
d = [d1 d2 d3];
t = [t1 t2 t3];
k = [k1 k2 k3];

a_len = length(a);

tail = N;
for i = a_len:-1:1
    x(i) = tail / a(i) - k(i);
    if i > 1
        t(i) = a(i) * k(i) / d(i-1);
        tail = t(i) * d(i-1);
        k(i-1) = tail / a(i);
    end
end
disp(x);

n = 10;
a0 = [2 5 6];
d0 = zeros(1, length(a0));
d0(1) = gcd(a0(1), a0(2));
for i = 3:length(a0)
    d0(i-1) = gcd(d0(i-2), a0(i));
end
d0(length(a0)) = gcd(a0(length(a0)), n);

% disp(x)
% x = subs(x, {t1, x1}, {a2*N/d1*p, a2*q});
% disp(x)

x0 = subs(x, {a1, a2, a3, d1, d2, d3, N}, {a0(1), a0(2), a0(3), d0(1), d0(2), d0(3), n});

% disp(x0);
j_ = 0:15; k_ = 0:15;
results = zeros(length(j_), length(k_), length(x0));
% results = sym('results', [length(j_) length(x0)]);
for i = 1:length(x0)
    for j = j_
        for k = k_
            disp(subs(x0(i), {k2, k3}, {j, k}));
            results(j+1, k+1, i) = subs(x0(i), {k2, k3}, {j, k});
        end
    end
end

% disp(results)
% disp(a0(1)*results(:, :, 1) + a0(2)*results(:, :, 2) + a0(3)*results(:, :, 3) - n)

disp(a0(1)*x(1) + a0(2)*x(2) + a0(3)*x(3) - n)
disp(x0)

