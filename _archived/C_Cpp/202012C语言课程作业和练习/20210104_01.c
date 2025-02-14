#include <stdio.h>

int main(){
	int a[10], i, *p;
	for(i=0;i<10;i++)
	    scanf("%d", &a[i]);
	for(i=0,p=a;i<5;i++)
		*(p+9-i)^=*(p+i)^=*(p+9-i)^=*(p+i);
	for(i=0;i<10;i++)
	    printf("%2d", a[i]);
    printf("\n");
	return 0;
}
