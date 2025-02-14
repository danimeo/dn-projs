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
	printf("���������Ľ�����");
	scanf("%d", &n);
	a=(int *)malloc(sizeof(int)*n*n);
	
	printf("\n������%dx%d����ĸ���Ԫ�أ�\n", n, n);
	int i,j;
	for(i=0;i<n*n;i++)
	    scanf("%d", a+i);
	
	convert(a, n);
	
	printf("\nת�ú�����Ԫ��Ϊ��\n");
	for(i=0;i<n;i++){
	    for(j=0;j<n;j++)
	    	printf("%d ", *(a+i*n+j));
	    printf("\n");
	}
	free(a);
	return 0;
}
