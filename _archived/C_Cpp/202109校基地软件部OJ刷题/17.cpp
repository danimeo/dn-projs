#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
	int m, n, i, j;
	char *a;
	cin >> m >> n;
	a = new char[m*n];
	vector<int> nums;
	for(i=0; i<m; i++)
		for(j=0; j<n; j++){
			cin >> a[i*n + j];
			if(a[i*n + j] == '*') nums.push_back(i + j);
		}
	if(!nums.size()) cout << "NotFind";
	else{
		sort(nums.begin(), nums.end());
		for(vector<int>::iterator iter=nums.begin(); iter!=nums.end(); ++iter)
		    cout << *iter << " ";
	}
	return 0;
}