#include<stdio.h>

int main(){
	int a[6] = {}, b[6] = {}, num = 0, i = 0, j, c, sum = 0;
	while(scanf("%c", &c) != EOF && c != '\n'){
		if(c == ' '){
			num = 0;
		}else{
			for(j = 0; j <= i; j++) if(a[j] == c) break;
			b[j] = b[j]*10
			i++;
		}
	}
		if(49 <= i && i <= 54) a[i-49]++;
	for(i = 6;i;) sum += a[--i];
	for(;i < 6; i++) printf("%d = %.3f\n", i + 1, (float)a[i]/sum);
	return 0;
}