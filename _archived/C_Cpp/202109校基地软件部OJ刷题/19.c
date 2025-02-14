#include <stdio.h>
#include <stdlib.h>

int main() {
	int *a, *b, m, n, size, i, j;
	scanf("%d %d", &n, &m);
	size = n * m;
	a = (int *) calloc(size, sizeof(int));
	b = (int *) calloc(size, sizeof(int));
	for (i = 0; i < size; i++)
		scanf("%d", a + i);
	
	if(size == 1){
		printf("%d", a[0]);
		return 0;
	}

	int d = 0, e, next;
	for (i = 0; ;) {
		for (e = (j = d) % 4; j < d + 4; e = ++j % 4) {
			if (!e && (next = i + 1) < i / n * n + n && !*(b + next)) break;
			if (e == 1 && (next = i + n) < size && !*(b + next)) break;
			if (e == 2 && (next = i - 1) >= i / n * n && !*(b + next)) break;
			if (e == 3 && (next = i - n) >= 0 && !*(b + next)) break;
		}
		if (j == d + 4) break;
		printf("%d:%d ", i, a[i]);
		d = e;
		*(b + i) = 1;
		i = next;
	}

	return 0;
}
