#include <stdio.h>

int main(){
	int a[2][4]={{1,2,3,4}, {5,6,7,8}};
	printf("%d\n", **a);
	char z[2][4]={"MAT", "LAB"};
	printf("%c\n", *(*z+2));
	return 0;
}
