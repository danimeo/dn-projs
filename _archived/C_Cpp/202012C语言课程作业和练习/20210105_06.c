#include <stdio.h>
#include <stdlib.h>

void convert(int *a, int n){
	int i, j;
	for(i=0;i<n;i++)
		for(j=0;j<i;j++)
	    	*(a+i*n+j)^=*(a+j*n+i)^=*(a+i*n+j)^=*(a+j*n+i);
}

int main(){
	int n, *a;
	printf("请输入矩阵的阶数：");
	scanf("%d", &n);
	a=(int *)malloc(sizeof(int)*n*n);
	
	printf("\n请输入%dx%d矩阵的各个元素：\n", n, n);
	int i,j;
	for(i=0;i<n*n;i++)
	    scanf("%d", a+i);
	
	convert(a, n);
	
	printf("\n转置后矩阵各元素为：\n");
	for(i=0;i<n;i++){
	    for(j=0;j<n;j++)
	    	printf("%d ", *(a+i*n+j));
	    printf("\n");
	}
	free(a);
	return 0;
}
