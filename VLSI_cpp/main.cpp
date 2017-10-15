#include "main.h"

using namespace std;

int main() {
	clock_t begin, end;
	auto temp = fixedStartCluster(readFile("pbd984.tsp"));
	begin = clock();
	for (auto iter = temp.begin(); iter < temp.end(); ++iter) {
		cout << *iter << " ";
	}
	end = clock();
	cout << "\n수행 시간 : " << static_cast<double>(end - begin) / CLOCKS_PER_SEC<<endl;
	int a;
	cin >> a;

	return 0;
}