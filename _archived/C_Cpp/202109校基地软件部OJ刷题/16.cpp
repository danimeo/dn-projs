#include <iostream>
#include <vector>
using namespace std;

int main() {
	int n, i, j=-1;
	vector<char> students;
	char c, juanwang;
	
	for (n = 0; cin.get(c), c != '\n'; n++)
	    students.push_back(c);
	if(n<3) return 0;
	juanwang = students[n-1];
	students.pop_back();
	students.pop_back();
	n -= 2;
	
	for (i = 0; i < n; i++)
		if (students[i] == juanwang && j<0) j=i;
	if(j<0)
		for (i = 0; i < n; i++) cout << students[i];
	else{
		for (i = j; i >= 0; i--) cout << students[i];
		for (i = j+1; i < n; i++) cout << students[i];
	}
	vector<char>(students).swap(students);
	return 0;
}