x = input('x: ');
if x < 0 && x ~= -3
    y = x^2 + x - 6;
else
    if 0 <= x && x < 10 && x ~= 2
        y = x^2 - 5*x + 6;
    else
        y = x^2 - x - 1;
    end
end
disp(y);