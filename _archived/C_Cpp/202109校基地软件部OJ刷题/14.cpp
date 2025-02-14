#include <iostream>
using namespace std;

int main() {
	int m, n, i, j, x=-1, y=-1;
	char *a;
	cin >> m >> n;
	a = new char[m*n];
	for(i=0; i<m; i++)
		for(j=0; j<n; j++){
			cin >> a[i*n + j];
			if(a[i*n + j] == '*') x = i, y = j;
		}
	if(x<0 && y<0) cout << "NotFind";
	else cout << "(" << x << "," << y << ")";
	return 0;
}