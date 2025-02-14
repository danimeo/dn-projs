#include<iostream>
#include<stdlib.h>
#define I int
#define M(x) (I*)calloc(x,sizeof(I))
using namespace std;I N,C,*E,*P,*Q,i=0,*d;I c(I n){for(i=0;i<C;i++)if(E[i]==n)return i;return -1;}void l(I n, I h){I a;if((a=c(n))>=0){l(P[a],d[P[a]]=++h);l(Q[a],d[Q[a]]=h);}}main(){cin>>N>>C;E=M(C),P=M(C),Q=M(C),d=M(N+1);for(;i<C;)cin>>E[i]>>P[i]>>Q[i++];l(1,d[1]=1);for(i=1;i<N;)cout<<d[i++]<<endl;}