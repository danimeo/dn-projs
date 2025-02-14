#include <iostream>
using namespace std;

int main() {
	int a, b, c, d, p;
	cin >> a >> b >> c >> d;
	
	if(a > c || (a == c && b == d)) c += 24;
	p = (c - (a + 1)) * 60 + (60 - b) + d;
	
	cout << "I juan le " << p / 60 << " hours " << p % 60 << " minutes";
	return 0;
}