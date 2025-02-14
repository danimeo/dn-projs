#include <stdio.h>
#include <stdlib.h>

void display_arr(int *arr, int n, char *name){
	int i, j;
	printf("%s", name);
	printf(" = {");
	for(i=0; i<n; i++) {
	    printf("{");
		for(j=0; j<n; j++) {
			printf("%d", *(arr+i*n+j));
			if(j<n-1){
				printf(" ");
			}
		}
		printf("}");
		if(i<n-1){
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

void preprocess(int *a, int n) {
	int f, g;
	for(f=0; f<n; f++) {
		int nn1=0;
		for(g=0; g<n; g++) {
			if(*(a + f*n + g)==1) {
				nn1=1;
				break;
			}
		}
		for(g=0; g<n; g++) {
			if(nn1==1&&*(a + f*n + g)!=1) {
				*(a + f*n + g) = 0;
			}
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

void add(int **combinations, int *length, int combination_n, int *combination){
	int combination_length = combination_n * combination_n;
	
	if(*combinations==NULL){
		*combinations = (int *) calloc(1, combination_length * sizeof(int));
		*length = 1;
	}else{
	    (*length)++;
		realloc(*combinations, *length * combination_length * sizeof(int));
	}
	
	copy_nxn(*combinations+(*length-1)*combination_n, combination, combination_n);
}

void reverse(int *arr, int m, int n) {
	int i;
	for(i=0; i<n; i++){
		if(m==0||m==1) {
			if(*(arr + i)==0||*(arr + i)==1) {
			    *(arr + i) ^= m;
			}
		}
	}
}

void unfold(int **combinations, int *length, int n, int range, int *result){
	int i, j;
	for(i=0; i<n; i++){
		int temp_j=-1;
		for(j=0; j<n; j++){
			int *p = result + i*n + j;
			if(*p==4){
				int m;
				for(m=0; m<range; m++){
					*p = m;
					add(combinations, length, n, result);
				}
			}else if(*p==2){
				if(temp_j>-1){
					*(result + i*n + temp_j) = 0;
				}
				*p = 1;
				add(combinations, length, n, result);
			}
		}
	}
	
	
}

void filter(int *result, int n){
	int i, j;
	for(j=0; j<n; j++) {
		int n_1=0;
		for(i=0; i<n; i++) {
			if(*(result + i*n + j)==1){
				n_1++;
			}
		}
		if(n_1!=0&&n_1!=n){
			for(i=0; i<n; i++) {
				*(result + i*n + j) = -1;
			}
		}
	}
}

void loop(int *m, int n, int *combinations, int combinations_length, int *result) {
	int i, j;
	
	for(i=0; i<n; i++){
		reverse(result + i*n, m[i], n);
	}
	filter(result, n);
		
	display_arr(result, n, "result");
	
	printf("\n");
}

int judge(int a[4][4]) {
	int b[4][4], result[4][4];
	int *combis=NULL, length=0;
	display_arr(a, 4, "a");
	
	copy_nxn(b, a, 4);
	preprocess(b, 4);  //对第二维含1的数组，将除1以外的元素置为0
	copy_nxn(result, b, 4);
	unfold(&combis, &length, 4);
	
	int layers[4];
	iterate(layers, 4, 0, 2, loop, &combis, &length, result);

	free(combis);
	return 0;
}

int main() {
	int a[4][4] = {{4,0,4,1}, {4,0,1,4}, {0,1,4,4}, {4,4,4,0}};
	judge(a);
	return 0;
}
