#include <stdio.h>

int main()
{
	float sum, n, pi=3.14159265, expected = pi*pi/6;
	for(sum=0, n=1; n<=100; sum+=1/(n*n), n+=1)
		printf("n=%.0f，sum=%.2f，与目标值相差%.2f\n", n, sum, expected-sum);
	return 0;
}

