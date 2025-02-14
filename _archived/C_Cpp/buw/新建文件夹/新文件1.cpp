#include<iostream>
main(){int m=0,n,i;for(std::cin>>i>>n;i<=n;m+=(i%2||i==1)*i++);std::cout<<m;}