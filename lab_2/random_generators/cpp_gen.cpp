#include <iostream>
#include <random>
#include <vector>
#include <fstream>
#include <string>


using namespace std;

vector<bool> generate_rand_seq(size_t n) {
	vector<bool> v;
	for (int i = 0; i < n; i++) {
		v.push_back(rand() % 2);
	}
	return v;
}


int main() {
	const size_t size = 128;

	vector<bool> v = generate_rand_seq(size);

	const string file = "files\\cpp_gen.txt";

	std::ofstream f_stream(file);

	if (!f_stream) {
		cerr << "Canot open input file: " << file;
		exit(-1);
	}

	for (const auto& val : v) {
		f_stream << val;
	}
	return 0;
}