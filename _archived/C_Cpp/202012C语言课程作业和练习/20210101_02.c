#include <stdio.h>

long long int pow0(long long int a, long long int n){
	long long int result = 1, i;
	for(i=0; i<n; i++){
		result *= a;
	}
	return result;
}

long long int digi(long long int a, long long int d){
	return a % pow0(10, d);
}

long long int ending_digi(long long int a, long long int n, long long int d){
	long long int n1 = n/2, n2 = n - n1;
	return digi(digi(pow0(a, n1), d) * digi(pow0(a, n2), d), d);
}

int main(){
	long long int a, n, d;
	printf("[计算a的n次方的最后d位数]\n\n请依次输入三个整数a、n和d，以空格分隔：");
	scanf("%lld%lld%lld", &a, &n,&d);
	printf("\n%lld的%lld次方的最后%lld位数是%lld\n", a, n, d, ending_digi(a, n, d));
	return 0;
}
