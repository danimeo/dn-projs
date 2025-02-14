using Plots
x = [j for j = 1:9]
y1 = [j^2 for j = x]
y2 = [sum([a[i]*x[j]^(i-1) for i=1:9]) for j = 1:9]
plot(x,[y1,y2],st=[:scatter :line])
savefig("Lagrange.png")
