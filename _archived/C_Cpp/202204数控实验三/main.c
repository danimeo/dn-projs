#include <stdio.h>
#include <math.h>

void main() {
	int f = 0;
	int x0, y0, xe, ye;
	int x, y, dx, dy;

	printf("X0 Y0: ");
	scanf("%d %d", &x0, &y0);
	printf("Xe Ye: ");
	scanf("%d %d", &xe, &ye);
	x = x0, y = y0;

	while (abs(xe - x) + abs(ye - y) != 0) {
		if (f >= 0) {
			dx = (xe - x >= 0) ? 1 : - 1;
			dy = 0;
			x += dx;
			f -= abs(ye - y0);
		} else {
			dx = 0;
			dy = (ye - y >= 0) ? 1 : - 1;
			y += dy;
			f += abs(xe - x0);
		}
		printf("x=%d, y=%d, dx=%d, dy=%d, f=%d\n", x, y, dx, dy, f);
	}
}