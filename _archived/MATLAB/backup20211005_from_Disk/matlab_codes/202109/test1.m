A = 1:16;
A(A<5) = 0;

arr = gpuArray(A);
disp(arr)