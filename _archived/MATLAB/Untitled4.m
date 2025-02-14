t = linspace(0, 2*pi, 50);

y1 = sin(2*t - 0.3);
y2 = 3 * cos(t + 0.5);

plot(t, y1, 'r-.o', 'linewidth', 2, 'markersize', 3);
hold on
plot(t, y2, 'b-', 'linewidth', 5, 'markersize', 5);
