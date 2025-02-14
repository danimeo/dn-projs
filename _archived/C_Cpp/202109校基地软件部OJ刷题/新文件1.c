#include <stdio.h>

int main() {
	char ch;
	int i;
	ch=getchar();
	while(ch!='?') {
		printf("%d\n", ch);
		ch=getchar();
	}
	return 0;
}