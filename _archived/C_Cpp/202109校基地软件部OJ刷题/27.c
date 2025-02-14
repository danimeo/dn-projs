#include <stdio.h>
#define N sizeof(int)*8

int main() {
	int ppl[N] = {};
	int n;

	for (n = 0; ; n++) {
		printf("%cµÄÉù³Æ£º", 97 + n);
		int j = 0, k = 0;
		char c[N];
		for (; (c[j] = getchar()) != '\n'; j++) {
			if (48 <= c[j] && c[j] <= 57 && j) {
				int a, b;
				a = c[j - 1] - 97;
				b = ppl[n] >> a;
				ppl[n] = ((b ^ (c[j] != 48)) << a) ^ (b?ppl[n] % b:0);
				printf("%d %d\n", ppl[n], (c[j] != 48));
				k++;
			}
		}

		if (!j)
			break;
	}

	int i, j;
	for (i = 0; i < n; i++) {
		printf("%c: ", i + 48);
		for (j = N; j >= 0; )
			printf("%d", (ppl[i] >> --j) % 2);
	}

	return 0;
}