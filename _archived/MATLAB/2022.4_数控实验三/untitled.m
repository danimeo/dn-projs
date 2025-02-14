clc, clear, close all

p0 = num2cell(input('[X0, Y0]: '));
pe = num2cell(input('[Xe, Ye]: '));
[x0, y0] = deal(p0{:});
[xe, ye] = deal(pe{:});

plot([x0, xe], [y0, ye], 'LineWidth', 2);
hold on;
grid on;
set(gca,'XLim',[-10 10]);  % X轴的数据显示范围
set(gca,'XTick',-10:1:10);  % 设置要显示的坐标刻度
set(gca,'YLim',[-10 10]);  % Y轴的数据显示范围
set(gca,'YTick',-10:1:10);  % 设置要显示的坐标刻度

F = 0; 
x = x0;
y = y0;
Dx = (xe-x0>=0)*2-1;
Dy = (ye-y0>=0)*2-1;
Xe = abs(xe-x0);
Ye = abs(ye-y0);

while abs(xe - x) + abs(ye - y) ~= 0
    if F >= 0
        dx = Dx;
        dy = 0;
        x = x + Dx;
        F = F - Ye;
    else
        dx = 0;
        dy = Dy;
        y = y + Dy;
        F = F + Xe;
    end
    plot([x-dx, x], [y-dy, y], 'LineWidth', 2);
    fprintf('x=%d, y=%d, dx=%d, dy=%d, f=%d\n', x, y, dx, dy, F);
    pause(0.25);
end