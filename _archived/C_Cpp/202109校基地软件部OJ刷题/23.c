#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
	int *a, m, n, size, i;
	scanf("%d %d", &n, &m);
	size = n * m;
	a = (int *) calloc(size, sizeof(int));
	for (i = 0; i < size; i++)
		scanf("%d", a + i);

	if (size == 1) {
		printf("%d", a[0]);
		return 0;
	}

	int x=0, y=0, *p=&x, *q=&y, *u, v=n, w=m, *s=&n, *t=&v, c=0;
	for(i=1; c<size; c++,(*p)++){
		printf("%d ", *(a+abs(y)*n+abs(x)));
		if(*p==(*p>0 ? *t-1 : *t-*s)&&(x||y)){
			u=p,p=q,q=u;
			t=(t==&v?&w:&v), s=(t==&v?&n:&m);
			*t-=(i++>2);
			*q=-*q;
		}
	}
		
	/*
	Input for testing:
4 4
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
    
    Output for testing:
    printf("x=%d, y=%d, a[x][y]=%d, v=%d, w=%d, *t-*s=%d\n", x, y, *(a+abs(y)*n+abs(x)), v, w, *t-*s);
	*/
	
	return 0;
}
