#include <stdio.h>
#include <stdlib.h>

int main() {
	int i, j, n, *a, count = 1;
	scanf("%d", &n);
	a = (int *) calloc(n * n, sizeof(int));
	
	for (i = 0, j = 0; i > 0, j > 0;) {
	int p, q;
	for (p = 0; p < n; p++) {
		printf("%d\n", count);
		*(a + p * n) = count++;
	}
	p -= 1;
	i++;
	for (q = i; q < p; q++) {
		printf("%d\n", count);
		*(a + p * n + q) = count++;
	}

	}
	printf("\n\n");
	int k;
	for (k = 0; k < n * n; k++) {
		printf("%d\n", *(a + k));
	}
	return 0;
}