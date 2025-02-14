#include<iostream>
main(){int n,x,y;std::cin>>n>>x>>y;std::cout<<((n=(n&&x)*(y?n-y/x-(y%x>0):n))>0)*n;}