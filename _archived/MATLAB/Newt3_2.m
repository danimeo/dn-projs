function y_ = Newt3(x, y, x_)

n = length(x);
% m = zeros(1, n);

function m = m_d(x, y, n, k, i)
    if k == n
        a = y(i);
        b = y(1 + i);
    else
        a = m_d(x, y, n, k+1, i);
        b = m_d(x, y, n, k+1, i+1);
    end
    
    c = (b - a) / (xb - xa);
    fprintf('%f ', a);
    if k == n
        fprintf('\n');
    end
end


m = m_d(x, y, n, 1, 1);
y_ = 0;

end