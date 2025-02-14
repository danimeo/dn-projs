function y = lagr(x0, y0, x)

j = 1:length(x0);
% L = zeros(length(x0));
for i = j
    L(i) = y0(i) .* prod((x - x0(j(j~=i))) ./ (x0(i) - x0(j(j~=i))));
end

y = sum(L);

