#include <stdio.h>
#define YES 1
#define NO 0
#define UNKNOWN 2

void asap_2_main(int a[4][4]) {
	int b[4][4], is_lying[4], k, l, conclusions[4][2][4], concls[4][2][4];
	int f, g;
	for(f=0; f<4; f++) {
		int nn1=0;
		for(g=0; g<4; g++) {
			if(a[f][g]==1) {
				nn1=1;
				break;
			}
		}
		for(g=0; g<4; g++) {
			b[f][g] = a[f][g];
			if(nn1==1&&a[f][g]!=1) {
				b[f][g] = 0;
			}
		}
	}
	for(k=0; k<4; k++) {
		for(is_lying[k]=0; is_lying[k]<2; is_lying[k]++) {
			for(l=0; l<4; l++) {
				if(b[k][l]!=0 && b[k][l]!=1) {
					conclusions[k][is_lying[k]][l] = b[k][l];
					continue;
				}
				conclusions[k][is_lying[k]][l] = is_lying[k] ^ b[k][l];
			}
		}
		int m, n;
		for(m=0; m<2; m++) {
			for(n=0; n<4; n++) {
				concls[k][m][n] = conclusions[k][m][n];
				printf("concls[%d][%d][%d]=%d\n", k, m, n, concls[k][m][n]);
			}
		}
		printf("\n");
	}

	int m[4], n;
	for(n=0; n<4; n++) {

		for(m[0]=0; m[0]<2; m[0]++) {
			for(m[1]=0; m[1]<2; m[1]++) {
				for(m[2]=0; m[2]<2; m[2]++) {
					for(m[3]=0; m[3]<2; m[3]++) {
						int u, sum0=0, sum1=0, sum_m=0;
						int v, vv, sum_v0=0, sum_v1=0;
						int vv_=-1;
						printf("如果");
						for(u=0; u<4; u++) {
							if(m[u]) {
								sum_m++;
								printf("嫌疑人%d说谎，", u);
							} else {
								printf("嫌疑人%d没说谎，", u);
							}
							if(concls[u][m[u]][n]==0) {
								sum0++;
							} else if(concls[u][m[u]][n]==1) {
								sum1++;
							}
						}
						int paradox=0, w[4], w_=0;
						for(u=0; u<4; u++) {
							for(vv=0; vv<4; vv++) {
								if(a[u][vv]==1) {
									int w__;
									for(w__=0; w__<w_; w__++) {
										if(w[w__]==vv) {
											printf("w[w__]=%d", w[w__]);
											paradox=1;
											break;
										}
									}
									w[w_++]=vv;
									printf("vv=%d", vv);
									break;
								}
							}
							if(paradox==1) {
								break;
							}
						}
						if(paradox==1) {
							printf("则该假设错误。\n");
							continue;
						}
						if(sum0==0&&sum1>0) {
							printf("则嫌疑人%d就是小偷。<-----", n);
							if(sum_m==4) {
								printf("（即所有人都说谎的结果）");
							} else if(sum_m==0) {
								printf("（即所有人都没说谎的结果）");
							} else {
								printf("\n");
							}
						} else if(sum0==4) {
							printf("则嫌疑人%d不是小偷。", n);
						} else if(sum1==0&&sum0<4) {
							printf("则无法确定嫌疑人%d是小偷。", n);
						} else if(sum0>0&&sum1>0) {
							printf("则产生矛盾。");
						} else {
							printf("存在例外情况。");
						}
						printf("\n\n");
					}
				}
			}
		}
	}
}

int main() {
	int a[4][4] = {{4,0,4,1}, {4,0,1,4}, {0,1,4,4}, {4,4,4,0}};
	asap_2_main(a);
	return 0;
}
