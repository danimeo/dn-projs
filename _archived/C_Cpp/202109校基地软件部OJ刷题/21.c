#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
	int *a, *b, m, n, size, i, j;
	scanf("%d %d", &n, &m);
	size = n * m;
	a = (int *) calloc(size, sizeof(int));
	b = (int *) calloc(size, sizeof(int));
	for (i = 0; i < size; i++)
		scanf("%d", a + i);

	if (size == 1) {
		printf("%d", a[0]);
		return 0;
	}

	/*int d = 0, e, next;
	i = 0;
	while (1) {
		for (e = (j = d) % 4; j < d + 4; e = ++j % 4) {
			if (!e && (next = i + 1) < i / n * n + n && !*(b + next)) break;
			if (e == 1 && (next = i + n) < size && !*(b + next)) break;
			if (e == 2 && (next = i - 1) >= i / n * n && !*(b + next)) break;
			if (e == 3 && (next = i - n) >= 0 && !*(b + next)) break;
		}
		printf("%d ", a[i]);
		if (j == d + 4) break;
		d = e;
		*(b + i) = 1;
		i = next;
	}*/

	/*int r = 0, x = 0, y = 0, *p = &x, *q = &y, *s = q, *t = &m;
	for (;r<size;r++) {
		printf("(%d, %d) ", abs(x), abs(y));
		printf("%d\n", *(a+abs(y)*n+abs(x)));
		if (abs(*s + 1) == *t || !*s)
			s = (s == p ? q : p), *t = (*t == n ? m : n), (*t)--;
		*s = (*s + 1 == *t ? -*t + 1 : *s);
		(*s)++;

	}*/
	
	/*int r = 0, x = 0, y = 0;
	for(;r<size;r++){
		printf("%d ", *(a+y*n+x));
		if(r){
			
		}
	}*/
	
	/*int r = 0, x = 0, y = 0, ds = 0, *p = &x, *q = &y, *s = p, *t = &n;
	for (;r<8;) {
		printf("(%d, %d) ", abs(x), abs(y));
		printf("%d n=%d, m=%d, s==q=%d\n", *(a+abs(y)*n+abs(x)), n, m, s==q);
		//if (abs(*s + 1) == *t || !*s || )
		//	s = (s == p ? q : p), *t = (*t == n ? m : n), (*t)--;
		if(*s+1 >= ((r+1&&(r+1)/2%2)?n-(r+1)/2:m-(r+1)/2)){
			printf("%d, %d ", (r+1)/2, ((r+1&&(r+1)/2%2)?n-(r+1)/2:m-(r+1)/2));
			s = (s == p ? q : p);
			if(*t == n) *t=m; else *t=n;
			r++;
		}
		if((r%4)/2) (*s)--; else (*s)++;
	}*/
	
	/*int r = 0, x = 0, y = 0, *p = &x, *q = &y, *t = &n, *s = &m, *u;
	for(;r<size;r++){
	    printf("r=%d, x=%d, y=%d\n", r, x, y);
		//if(*p+1<*t) (*p)++; else if(*q+1<*s) (*q)++; else u=p, *q=1-*q, p=q, q=u;
		if(*p==*t) *p=-*p+1;
		if(!*p%*t||!r) p=(p==&x?&y:&x), q=(q==&y?&x:&y), t=(t==&n?&m:&n);
		else if(*p<*t) (*p)++;
		
	}*/
	
	/*int r=0, x=0, y=0, *p[3], t=n, cnt=0;
	p[0] = &x, p[1] = &y;
	for(;n>0||m>0;r++){
		if(r>0) *p[0]=r; else if(r<0) *p[1]=t-1+r; else if(x||y) *p[0]=r,*p[1]=t-1+r,p[2]=p[0],p[0]=p[1],p[1]=p[2];
	    printf("r=%d, x=%d, y=%d\n", r, x, y);
		if(abs(r)==t-1) r=(2*(r<0)-1)*((t==n?m:n)-1); 
		if(++cnt==size) break;
	}*/
	
	/*
4 4
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
	*/
	
	/*int r=0, x=0, y=-6, *p=&x, t=n, cnt=0;
	printf("r=%d, x=%d, y=%d\n", r, x, y);
	for(;n>0||m>0;){
		//printf("r=%d, x=%d, y=%d\n", r, abs(x), abs(y)<m?abs(y):0);
		if(x<n-1) x++; 
		if(y<m-1) y++; 
		if(abs(x)==n-1) x=(2*(x<0)-1)*(n-1);
		else if(abs(y)==m-1) y=(2*(y<0)-1)*(m-1);
		printf("r=%d, x=%d, y=%d\n", r, x, y);
		if(++cnt==size) break;
	}*/
	
	/*int r=1, x=0, y=-6, *p=&x, *t=&n, cnt=0;
	//printf("r=%d, x=%d, y=%d\n", r, x, y);
	for(;n>0||m>0;){
		if(t==&n&&abs(r)<*t) x=r; if(t==&m&&abs(r)<*t) y=r;
		printf("r=%d, x=%d, y=%d, *t=%d\n", r, x, y, *t);
		if((r+1)==*t) r=-(*t-1)+1, p=(p==&x?&y:&x), t=(t==&n?&m:&n);
		 else if(!r) p=(p==&x?&y:&x), t=(t==&n?&m:&n);
		  else r++;
		if(++cnt==size) break;
	}*/
	
	int x=0, y=0, *p=&x, *q=&y, *u=NULL, v=n, w=m, *s=&n, *t=&v, cnt=0, h=1;
	for(;cnt<size+4;cnt++){
		printf("x=%d, y=%d, a[x][y]=%d, v=%d, w=%d, *t-*s=%d\n", x, y, *(a+abs(y)*n+abs(x)), v, w, *t-*s);
		if(*p==(*p>0 ? *t-1 : *t-*s)&&(x||y)){
			u=p,p=q,q=u;
			t=(t==&v?&w:&v),s=(t==&v?&n:&m);
			*t-=(h>2);
			*q=-*q;
			h++;
		}
		(*p)++;
	}
	
	/*int r=0, x=0, y=0;
	for(;r<size;r++){
		
		x=r;
	}*/

	/*int r, x=n, y=m, s=0, s1=n+m-(n+m)/2, s2=(n+m)/2-n+m;
	for(r=0; r<n+m; ){
		if(!r%x) {
			if(!s){
				r++;
				x--;
			}

		}
		x+=(r%2?1:0);
		x+=(r%2?0:1);
		printf("r=%d, x=%d, y=%d, r/2=%d, n-r/2=%d\n", r, x, y, r/2, n-r/2);
		getchar();
	}*/


	return 0;
}
