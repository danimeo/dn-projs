function y = lagr(x0, y0, x)

for i = 1:length(x0)
    disp(i);
    L = y0(i) .* prod((x - x0(x0~=i)) ./ (x0(i) - x0(x0~=i)));
end

y = sum(L);

