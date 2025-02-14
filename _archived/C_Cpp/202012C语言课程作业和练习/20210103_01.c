//���ߣ�luodajunxixi (2021.1.3 16:37)
#include <stdio.h>

void print_arr(int *arr, int n, char *name) { //��������һ���Զ�����������nxn�����������ݵĺ��������԰����������������������
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

void copy_nxn(int *b, int *a, int n) {  //��һ��nxn����������a�е�ֵ���ƽ�nxn��������b
	int i, j;
	for(i=0; i<n; i++)
		for(j=0; j<n; j++)
			*(b + i*n + j) = *(a + i*n + j);
}

void reverse(int *arr, int *m, int n) { //�������λ�������^��������ٶ�ĳ����˵�ѣ�������˵��ȫ��ȡ����0ȡ��Ϊ1��1ȡ��Ϊ0������������2������
	int i, j;
	for(i=0; i<n; i++)
		for(j=0; j<n; j++) {
			int v = *(arr + i*n + j);
			if(v==0 || v==1)
				*(arr + i*n + j) ^= m[i];
		}
}

void condition_process(int *a, int n) {  //���ݡ�ֻ��һ��Ϊ����������֪��Ϣ����һ�������г�1�����Ԫ��ȫ����Ϊ0
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

int is_paradox(int *arr, int n) { //���һ������Ƿ�����ì�ܣ�����ì���򷵻�1�����򷵻�0
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
	int a[4][4] = {{2,0,2,1}, {2,0,1,2}, {0,1,2,2}, {2,2,2,0}};  //4x4���飬���ڴ���������ݡ��ڶ�ά��ŵ���ĳ�˵�˵����0��ʾ���˳�һ���˲���������1��ʾΪ������2��ʾδ�ἰ
	int result[16][4], length = 0;  //����оٳ���4����ÿ���Ƿ�˵�ѵ�16�ּ���

	int m[4];  //4��ѭ����m�ĸ�Ԫ��ȡֵ��Ϊ0��1��������m��4����˵���������п��ܵ���ϡ�����2��4�η���16�ֿ��ܡ�
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

		int c[4][4];  //����������
		copy_nxn(c, a, 4);  //����������a���ƽ�����c
		reverse(c, result[k], 4);  //����ǰ��õ������result[k]�������������c
		condition_process(c, 4);  //���ݡ�ֻ��һ��Ϊ����������֪��Ϣ������������c

		//���result[k]��Ӧ�Ľ������cû������ì�ܣ�����ж����Ϊk��������Ϊ����
		if(!is_paradox(c, 4))
			thief = k;
		if(thief!=-1) {
			char *names[4] = {"��", "��", "��", "��"};
			printf("������%sΪ������\n", names[k]);
		}
	}
	if(thief==-1)
		printf("�޷�ȷ��˭��������\n");
	return 0;
}
