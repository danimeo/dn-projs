#include <stdio.h>
#define N 4

int main(){
	void convert(int *, int);
	void print_arr(int *, int, char *);
	
	printf("请输入%dx%d的矩阵的各个元素：\n", N, N);
	int a[N][N],i,j;
	for(i=0;i<N;i++)
		for(j=0;j<N;j++)
		    scanf("%d", &a[i][j]);
	printf("\n");
	
	print_arr(a, N, "转置前：a");
	
	convert(a, N);
	
	print_arr(a, N, "转置后：a");
	
	printf("\n");
	return 0;
}

void convert(int *a, int n){
	int i, j;
	for(i=0;i<n;i++)
		for(j=0;j<i;j++)
	    	*(a+i*n+j)^=*(a+j*n+i)^=*(a+i*n+j)^=*(a+j*n+i);
}

void print_arr(int *arr, int n, char *name){
	int i, j;
	printf("%s", name);
	printf(" = {");
	for(i=0; i<n; i++) {
	    printf("{");
		for(j=0; j<n; j++) {
			printf("%d", *(arr+i*n+j));
			if(j<n-1){
				printf(" ");
			}
		}
		printf("}");
		if(i<n-1){
			printf(", ");
		}
	}
	printf("}\n");
}
