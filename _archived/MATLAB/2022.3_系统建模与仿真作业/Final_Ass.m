t=out.tout;
theta2=out.acc(:,1);
dr1=out.acc(:,4);
r1=out.acc(:,5);

subplot(2,1,1);
plot(t, theta2);
title('输入角度随时间变化曲线')
legend('theta2 (rad)')
xlabel('时间（s）')

subplot(2,1,2);
yyaxis left;
plot(t, dr1, 'k-');
ylabel('输出速度（mm/s）');

yyaxis right;
plot(t, r1, 'k--');
ylabel('输出位移（mm）');

title('输出速度和位移随时间变化曲线')
xlabel('时间（s）')
legend('dr1 (mm/s)','r1 (mm)')

% set(gcf,'Position',[100 100 600 800]);