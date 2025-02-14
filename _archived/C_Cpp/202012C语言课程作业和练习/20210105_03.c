#include <stdio.h>

int main(){
	float score[][4]={{60,70,80,90},{56,89,67,88},{34,78,90,66}}, *p;
	int n, i;
	scanf("%d", &n);
	p=score+n;
	for(i=0;i<4;i++)
	    printf("%8.2f", p[i]);
	printf("\n");
	return 0;
}
