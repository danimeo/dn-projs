alpha=0.001;
beta=0.072;
t_end=20;
x0 = [620; 10; 70];

f=@(t,x) [-alpha*x(1)*x(2);
    alpha*x(1)*x(2)-beta*x(2);
    beta*x(2)];

[t,x]=ode45(f, [0 t_end], x0);

plot(t, x(:,1), 'r-', t, x(:,2), 'g-', t, x(:,3), 'b-')
legend('X1', 'X2', 'X3')

xlabel('时间（年）')
ylabel('三种类型人数（人）')
