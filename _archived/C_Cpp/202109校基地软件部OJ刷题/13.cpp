#include <iostream>
using namespace std;

int main() {
	int n, *students, juanwang, i;
	cin >> n;
	students = new int[n];
	for (i = 0; i < n; i++) cin >> students[i];
	cin >> juanwang;

	for (i = 0; i < n; i++)
		if (students[i] == juanwang) break;
	if(i == n)
		for (i = 0; i < n; i++) cout << students[i];
	else
		for (n = i; n >= 0; n--) cout << students[n];
	return 0;
}