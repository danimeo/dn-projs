#include <stdio.h>
#include <stdlib.h>

void display_arr(int *arr, int n, char *name) {
	int i, j;
	printf("%s", name);
	printf(" = {");
	for(i=0; i<n; i++) {
		printf("{");
		for(j=0; j<n; j++) {
			printf("%d", *(arr+i*n+j));
			if(j<n-1) {
				printf(" ");
			}
		}
		printf("}");
		if(i<n-1) {
			printf(", ");
		}
	}
	printf("}\n");
}

void copy_nxn(int *b, int *a, int n) {
	int i, j;
	for(i=0; i<n; i++) {
		for(j=0; j<n; j++) {
			*(b + i*n + j) = *(a + i*n + j);
		}
	}
}

void iterate(int *layers, int layer_num, int layer_count, int range, void (*func)(int *, int, int *, int, int *), int **combinations, int *combinations_length, int *result) {
	if(layer_count==layer_num) {
		return;
	}
	int i;
	for(i=0; i<range; i++) {
		layers[layer_count] = i;
		if(layer_count<layer_num-1) {
			iterate(layers, layer_num, layer_count+1, range, func, combinations, combinations_length, result);
		} else {
			func(layers, layer_num, combinations, *combinations_length, result);
		}
	}
}

void reverse(int *result, int m, int n) {
	int i, j;
	for(i=0; i<n; i++) {
		if(m) {
			
			for(j=0; j<n; j++) {
				if(m==0||m==1) {
					if(*(result + j)==0||*(result + j)==1) {
						*(result + j) ^= m;
					}
				}
			}
		}else{
			
		}
	}
}

void loop(int *m, int n, int *combinations, int combinations_length, int *result) {
	int i;
	for(i=0; i<n; i++) {

	}
}

int judge(int *a, int n) {
	int *b = (int *) malloc(sizeof(int)*n*n);
	int *combis = NULL, length = 0;

	copy_nxn(b, a, n);

	free(b);
	if(combis!=NULL) {
		free(combis);
	}
	return -1;
}

int main() {
	int a[4][4] = {{4,0,4,1}, {4,0,1,4}, {0,1,4,4}, {4,4,4,0}};
	judge(a, 4);
	return 0;
}
