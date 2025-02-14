function y = N3(X, Y, x)

n = length(X);
expr = cell(1, n-1);
y = Y(1);
m = zeros(1, n);

fprintf('  X   \t  Y   \t');
for i = 1:n-1
    fprintf('%d阶差商\t', i);
end
fprintf('\n%6.2f\t%6.2f\t\n', X(1), Y(1));

for j = 2:n
    a = Y(j-1);
    m(1) = Y(j);
    fprintf('%6.2f\t%6.2f\t', X(j), Y(j));
    for i = 2:j
        b = m(i);
        m(i) = (m(i-1) - a) / (X(j) - X(j-i+1));
        fprintf('%6.2f\t', m(i));
        a = b;
    end
    fprintf('\n');
    p = 1;
    for k = 1:j-1
        p = p .* (x - X(k));
    end
    y = y + vpa(m(j) * p);
    expr{j-1} = char(y);
end

y = simplify(y);

for i = 1:n-1
    fprintf('\nN%d = %s', i, expr{i});
end
fprintf('\n');
