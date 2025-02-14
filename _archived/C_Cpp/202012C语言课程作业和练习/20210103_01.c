//作者：luodajunxixi (2021.1.3 16:37)
#include <stdio.h>

void print_arr(int *arr, int n, char *name) { //首先送你一个自定义的用来输出nxn整型数组内容的函数，可以帮助你分析本程序的运算过程
	int i, j;
	printf("%s", name);
	printf(" = {");
	for(i=0; i<n; i++) {
		printf("{");
		for(j=0; j<n; j++) {
			printf("%d", *(arr+i*n+j));
			if(j<n-1)
				printf(" ");
		}
		printf("}");
		if(i<n-1)
			printf(", ");
	}
	printf("}\n");
}

void copy_nxn(int *b, int *a, int n) {  //将一个nxn的整型数组a中的值复制进nxn整型数组b
	int i, j;
	for(i=0; i<n; i++)
		for(j=0; j<n; j++)
			*(b + i*n + j) = *(a + i*n + j);
}

void reverse(int *arr, int *m, int n) { //利用异或位运算符（^），如果假定某个人说谎，则将他的说法全部取反，0取反为1，1取反为0，其他数（如2）不变
	int i, j;
	for(i=0; i<n; i++)
		for(j=0; j<n; j++) {
			int v = *(arr + i*n + j);
			if(v==0 || v==1)
				*(arr + i*n + j) ^= m[i];
		}
}

void condition_process(int *a, int n) {  //根据“只有一人为窃贼”的已知信息，将一组数据中除1以外的元素全部置为0
	int f, g;
	for(f=0; f<n; f++) {
		int nn1=0;
		for(g=0; g<n; g++)
			if(*(a + f*n + g)==1) {
				nn1=1;
				break;
			}

		for(g=0; g<n; g++)
			if(nn1==1 && *(a + f*n + g)!=1)
				*(a + f*n + g) = 0;
	}
}

int is_paradox(int *arr, int n) { //检测一组假设是否自相矛盾，存在矛盾则返回1，否则返回0
	int i, j;
	for(j=0; j<n; j++) {
		int temp = *(arr + j);
		for(i=1; i<n; i++) {
			int m = *(arr + i*n + j);
			if(m != temp && ((m==0&&temp==1) || (m==1&&temp==0)))
				return 1;
		}
	}
	return 0;
}

int main() {
	int a[4][4] = {{2,0,2,1}, {2,0,1,2}, {0,1,2,2}, {2,2,2,0}};  //4x4数组，用于存放输入数据。第二维存放的是某人的说法，0表示此人称一个人不是窃贼，1表示为窃贼，2表示未提及
	int result[16][4], length = 0;  //存放列举出的4个人每人是否说谎的16种假设

	int m[4];  //4重循环，m的各元素取值均为0或1，即数组m是4个人说谎与否的所有可能的组合。共有2的4次方即16种可能。
	for(m[0]=0; m[0]<2; m[0]++)
		for(m[1]=0; m[1]<2; m[1]++)
			for(m[2]=0; m[2]<2; m[2]++)
				for(m[3]=0; m[3]<2; m[3]++) {

					int b[4][4];
					copy_nxn(b, a, 4);
					reverse(b, m, 4);
					if(is_paradox(b, 4))
						continue;
					int i;
					for(i=0; i<4; i++)
						result[length][i] = m[i];
					length++;

				}

	int k, thief=-1;
	for(k=0; k<length; k++) {

		int c[4][4];  //定义结果数组
		copy_nxn(c, a, 4);  //将输入数组a复制进数组c
		reverse(c, result[k], 4);  //根据前面得到的组合result[k]，调整结果数组c
		condition_process(c, 4);  //根据“只有一人为窃贼”的已知信息，处理结果数组c

		//如果result[k]对应的结果数组c没有自相矛盾，则可判断序号为k的嫌疑人为窃贼
		if(!is_paradox(c, 4))
			thief = k;
		if(thief!=-1) {
			char *names[4] = {"甲", "乙", "丙", "丁"};
			printf("嫌疑人%s为窃贼。\n", names[k]);
		}
	}
	if(thief==-1)
		printf("无法确定谁是窃贼。\n");
	return 0;
}
