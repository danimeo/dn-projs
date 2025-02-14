#include <iostream>
using namespace std;

int main() {
	string a[2];
	cin >> a[0] >> a[1];
	int result[2] = {0, 0}, i;

	for (i = 0; i < 2; i++) {
		int sign = 1, num = 0, num_exists = 0, is_imag = 0, j;
		char c;
		for (j = 0; (c = a[i][j]) != '\0'; j++)
			if (c == '+' || c == '-') {
				result[is_imag] += num_exists ? sign * num : sign * is_imag;
				is_imag = num_exists = num = 0;
				sign = (c == '+') ? 1 : -1;
			} else if (48 <= c && c <= 57) {
				num = num * 10 + (c - 48);
				num_exists = 1;
			} else is_imag = 1;
		result[is_imag] += num_exists ? sign * num : sign * is_imag;
	}
	
	if(result[0]){
		cout << result[0];
		if(result[1] > 0) cout << "+";
	}
	if(result[1]){
		if(result[1] == -1)
		    cout << "-";
		else if(result[1] != 1)
		    cout << result[1];
		cout << "i";
	}
	if(!result[0] && !result[1]) cout << 0;
	return 0;
}