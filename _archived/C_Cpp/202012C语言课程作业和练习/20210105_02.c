#include <stdio.h>

int main(){
	int a[3],i,j,*p=a;
	for(i=0;i<3;i++)
	    scanf("%d", p+i);
	for(i=0;i<3;i++)
	    for(j=i+1;j<3;j++)
	        if(*(p+i)<*(p+j))
	            *(p+i)^=*(p+j)^=*(p+i)^=*(p+j);
	for(;p-a<3;p++)
	    printf("%3d", *p);
	printf("\n");
	return 0;
}
