#include <stdio.h>

typedef struct Bl {
	char *s;
	int len;
	int t;
	struct Bl *next;
} Block;

int T;

Block *append(Block *bl_arr, int *n_bl, char *s, int len, int t) {
	Block *new_bl;
	new_bl = bl_arr + (*n_bl)++;
	if (s != NULL) {
		new_bl->len = len;
		new_bl->s = s;
	} else {
		new_bl->s = NULL;
		new_bl->len = 0;
	}
	new_bl->t = t;
	new_bl->next = NULL;
	return new_bl;
}

void insert(Block *bl_arr, int *n_bl, char *s, int len, int t) {
	Block *p, *prev, *next;
	p = bl_arr, prev = NULL;
	for (p = bl_arr; p != NULL; p = p->next)
		if (t >= p->t + T) p->s = NULL;
		
	for (p = bl_arr; p != NULL; ) {
		if (p->len >= len && p->s == NULL) {
			p->s = s;
			p->t = t;
			return;
		}
		if(p->next!=NULL)
			p = p->next;
	    else{
			p->next = append(bl_arr, n_bl, s, len, t);
			return;
		}
	}
	//for(p=bl_arr;p<bl_arr+10;p++) printf("%s ", p->s);
	//printf("\n");
}

void sort(int a[][3], int l, int r) {
	if (l < r) {
		int i, j, pivot;
		i = l, j = r, pivot = a[i][2];
		while (i < j) {
			for (; i < j && a[j][2] >= pivot; j--);
			if (i < j)
				a[i++][2] = a[j][2];
			for (; i < j && a[i][2] < pivot; i++);
			if (i < j)
				a[j--][2] = a[i][2];
		}
		a[i][2] = pivot;
		sort(a, l, i - 1);
		sort(a, i + 1, r);
	}
}

/*
3
2
3 1 abc
5 2 dddcc
3 3 efg
*/

int main() {
	int n, i, j, a[1000][3];
	char s[1000][1000];
	scanf("%d %d", &n, &T);
	for (i = 0; i < n; i++) {
		scanf("%d %d %s", &a[i][0], &a[i][1], &s[i][0]);
		a[i][2] = i;
	}

	sort(a, 0, n - 1);

	Block blocks[1000];
	int n_bl = 1;
	for (i = 0; i < n; i++)
		insert(blocks, &n_bl, &s[i][0], a[i][0], a[i][1]);

	printf("sss\n");
	Block *p;
	char c;
	for(p = blocks; p != NULL; p = p->next) {
		if (p->s != NULL)
			printf("%s", p->s);
		for (i = 0; p->s != NULL && *(p->s + i) != '\0'; i++);
		for (j = i; j < p->len; j++)
			printf("%c", '*');
	}
	printf("\nend\n");

	return 0;
}