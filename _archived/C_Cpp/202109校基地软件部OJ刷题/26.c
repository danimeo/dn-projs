#include <stdio.h>

typedef struct Bl {
	char *s;
	int len, t;
} Block;

int T;

Block *append(Block *bl_arr, int *n_bl, char *s, int len, int t) {
	Block *new_bl;
	new_bl = bl_arr + (*n_bl)++;
	new_bl->s = s;
	if (s != NULL)
		new_bl->len = len;
	else
		new_bl->len = 0;
	new_bl->t = t;
}

void insert(Block *bl_arr, int *n_bl, char *s, int len, int t) {
	int i;
	for (i = 0; i < *n_bl; i++)
		if (t >= bl_arr[i].t + T)
			bl_arr[i].s = NULL;

	for (i = 0; i < *n_bl; i++)
		if (bl_arr[i].len >= len && bl_arr[i].s == NULL) {
			bl_arr[i].s = s;
			bl_arr[i].t = t;
			return;
		}
	append(bl_arr, n_bl, s, len, t);
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
	int n, i, j, k, a[1000][3];
	char s[1000][1000];
	scanf("%d %d", &n, &T);
	for (i = 0; i < n; i++) {
		scanf("%d %d %s", &a[i][0], &a[i][1], &s[i][0]);
		a[i][2] = i;
	}

	sort(a, 0, n - 1);

	Block blocks[1000];
	int n_bl = 0;
	for (i = 0; i < n; i++)
		insert(blocks, &n_bl, &s[i][0], a[i][0], a[i][1]);

	char c;
	for (k = 0; k < n_bl; k++) {
		if (blocks[k].s != NULL)
			printf("%s", blocks[k].s);
		for (i = 0; blocks[k].s != NULL && *(blocks[k].s + i) != '\0'; i++);
		for (j = i; j < blocks[k].len; j++)
			printf("%c", '*');
	}
	return 0;
}