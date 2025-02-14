clc, clear, close all

% 输入X0，Y0，Xe，Ye
x0=input('x0=');
y0=input('y0=');
xe=input('xe=');
ye=input('ye=');

plot([x0, xe], [y0, ye], 'LineWidth', 2);  % 先画出待插补的直线
hold on;  % 使后面每一次plot画在同一张图中
grid on;  % 显示网格
set(gca,'XLim',[-10 10]);  % X轴的显示范围
set(gca,'XTick',-10:1:10);  % 设置要显示的坐标刻度
set(gca,'YLim',[-10 10]);  % Y轴的显示范围
set(gca,'YTick',-10:1:10);  % 设置要显示的坐标刻度

F = 0;  % 偏差F初始值为0
x = x0;  % x初始值为输入的x0
y = y0;  % y初始值为输入的y0
Dx = (xe-x0>=0)*2-1;  % 等价于if xe-x0>=0 Dx=1 else Dx=-1 end
Dy = (ye-y0>=0)*2-1;  % 原理同上
Xe = abs(xe-x0);  % 为了适用于所有象限，用绝对值|xe-x0|计算，而不是直接用输入的xe
Ye = abs(ye-y0);  % 原理同上

% 终点判别：|xe-x0|+|ye-y0|=0时结束while循环
while abs(xe - x) + abs(ye - y) ~= 0
    if F >= 0  % 当偏差大于等于0，即走到直线上方或在直线上时：
        dx = Dx;  % 此时ΔX就是上面的Dx，取值为1或-1
        dy = 0;  % 此时ΔY为0
        x = x + Dx;  % 沿X轴方向进给ΔX（ΔX可能为正也可能为负）
        F = F - Ye;  % 计算下一步的偏差
    else  % 当偏差小于0，即走到直线下方时：
        dx = 0;  % 此时ΔX为0
        dy = Dy;  % 此时ΔY就是上面的Dy，取值为1或-1
        y = y + Dy;  % 沿Y轴方向进给ΔY（ΔY可能为正也可能为负）
        F = F + Xe;  % 计算下一步的偏差
    end
    plot([x-dx, x], [y-dy, y], 'LineWidth', 2);  % 画出刚刚进给的这一步
    fprintf('x=%d, y=%d, dx=%d, dy=%d, f=%d\n', x, y, dx, dy, F);  % 输出
    pause(0.25);  % 循环走到这里暂停0.25秒，即每步间隔0.25秒
end