function y = N3_(X, Y, x)

n = length(X);
y = Y(1);
m = zeros(1, n);

for j = 2:n
    a = Y(j-1);
    m(1) = Y(j);
    for i = 2:j
        b = m(i);
        m(i) = (m(i-1) - a) / (X(j) - X(j-i+1));
        a = b;
    end
    p = 1;
    for k = 1:j-1
        p = p .* (x - X(k));
    end
    y = y + m(j) * p;
end

y = simplify(y);
