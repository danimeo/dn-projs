#include<stdio.h>

int main(){
    int a[4][4] = {{2,0,2,1}, {2,0,1,2}, {0,1,2,2}, {2,2,2,0}}, m[4];
    //int a[4][4] = {{0,0,0,1}, {0,0,1,0}, {0,1,0,0}, {2,2,2,0}}, m[4];
	char *names[4] = {"¼×", "ÒÒ", "±û", "¶¡"};
	
    for(m[0]=0;m[0]<2;m[0]++)
        for(m[1]=0;m[1]<2;m[1]++)
            for(m[2]=0;m[2]<2;m[2]++)
                for(m[3]=0;m[3]<2;m[3]++){
                    int i, j, b[4][4];
                        printf("m=%d %d %d %d\n", m[0], m[1], m[2], m[3]);
                        for(i=0;i<4;i++){
                        	int n1=-1;
                            for(j=0;j<4;j++){
                        	    if(a[i][j]==0||a[i][j]==1)
                                    b[i][j] = a[i][j] ^ m[i];
                                else
                                    b[i][j] = a[i][j];
                                if(b[i][j]==1)
                                    n1=j;
							}
							if(n1>=0)
							    for(j=0;j<4;j++)
							    	if(j!=n1)
							    	    b[i][j]=0;
						}
						
						for(j=0;j<4;j++){
							int sum_0=0, sum_1=0;
							for(i=1;i<4;i++){
								if(b[i][j]==1)
								    sum_1++;
								else if(b[i][j]==0)
								    sum_0++;
							}
							if(sum_0==4||(sum_0<4&&sum_1==0))
							    continue;
							if(sum_0>0&&sum_1>0)
							    break;
						}
						if(j<4)
						    continue;
                        printf("%s\n\n", names[j]);
                        /*for(i=0;i<4;i++){
                            if(a[i][j]==0||a[i][j]==1)
                                n[i] = a[i][j] ^ m[i];
                            else
                                n[i] = a[i][j];
                        	int k;
						    for(k=0;k<4;k++)
                        	    if(k!=j&&a[i][k]<2&&(a[i][k] ^ m[i])==1){
                        	    	printf("i=%d j=%d m[i]=%d k=%d a[i][k]=%d\n", i, j, m[i], k, a[i][k]);
                        	    	break;
								}
                            if(k<4)
                                n[i] = 0;
                            if(n[i]==0)
                                break;
                        }*/
						
                        
                    
                }
    return 0;
}

/*void display_arr(int *arr, int n, char *name){
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
}*/
