#include <iostream>
using namespace std;

int main() {
	int a, b, c;
	cin >> a >> b;
	if (a >= b)
		c = b - a + 24;
	else
		c = b - a;
	cout << "I juan le " << c << " hours";
	return 0;
}