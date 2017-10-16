#include <ctime>
#include "main.h"

using namespace std;

int main() {
	clock_t begin, end;

	srand(static_cast<unsigned int>(time(NULL)));
	auto temp = fixedStartCluster(readFile("frv4410.tsp"));
	begin = clock();
	for (auto iter = temp.begin(); iter < temp.end(); ++iter) {
		cout << *iter << " ";
	}
	end = clock();
	cout << "\n수행 시간 : " << end <<" "<< begin << endl;
	int a;
	cin >> a;

	return 0;
}