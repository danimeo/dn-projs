#include <stdio.h>

int main(){
	int array[10], i, *p=array, max, min;
	for(i=0;i<10;i++)
	    scanf("%d", &array[i]);
	max=min=*p;
	for(i=1;i<10;i++)
		if(*(p+i)>max)
		    max=*(p+i);
		else if(*(p+i)<min)
		    min=*(p+i);
	printf("max=%d,min=%d",max,min);
	return 0;
}
