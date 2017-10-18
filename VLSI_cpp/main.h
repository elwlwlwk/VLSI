#pragma once
#include <fstream>
#include <memory>
#include <sstream>
#include <string>
#include <math.h>
#include <vector>
#include <array>
#include <iostream>

using namespace std;

vector<vector<float>> calc_cost_mat(vector<array<int, 3>>* data) {
	vector<vector<float>> cost_mat(data->size(), vector<float>(data->size()));
	array<int, 3> p1;
	array<int, 3> p2;
	for (auto i = 0; i < cost_mat.size(); i++) {
		for (auto j = 0; j < cost_mat.size(); j++) {
			p1 = data->at(i);
			p2 = data->at(j);
			float distance = sqrt(pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2));
			cost_mat.at(p1[0] - 1).at(p2[0] - 1) = cost_mat.at(p2[0] - 1).at(p1[0] - 1) = distance;
		}
	}
	return cost_mat;
}

float calc_score(vector<int> path, vector<vector<float>> &cost_mat) {
	float cost = 0;
	for (auto i = 0; i < path.size() - 1; i++) {
		cost += cost_mat.at(path.at(i) - 1).at(path.at(i + 1) - 1);
	}
	return cost;
}

float calc_score(int* path, int len, float** cost_mat) {
	float cost = 0;
	for (auto i = 0; i < len - 1; i++) {
		cost += cost_mat[path[i] - 1][path[i + 1] - 1];
	}
	return cost;
}

float calc_prob(float best_score, float trial_score, float temperature) {
	if (best_score> trial_score) {
		return 1;
	}
	else {
		return pow(2.71828, (best_score - trial_score) / temperature);
	}
}

float get_inter_cost(vector<vector<int>> paths, vector<vector<float>> cost_mat) {
	float inter_cost = 0;
	float last_point = -1;
	float first_point = -1;
	for (auto idx = 0; idx < paths.size() - 1; idx++) {
		if (paths[idx].size() != 0) {
			last_point = paths.at(idx).back();
		}
		if (paths[idx + 1].size() != 0) {
			first_point = paths.at(idx + 1).at(0) - 1;
		}
		if (last_point != -1 && first_point != -1) {
			inter_cost += static_cast<float>(cost_mat.at(first_point).at(last_point));
			last_point = -1;
			first_point = -1;
		}
	}
	return inter_cost;
}


vector<int> gen_trial_path_2opt(vector<int> path, float** cost_mat) {
	vector<int>best_path(path);
	float best_score = 999999999;

	int max_iter = 30000;
	int path_len = path.size();
	for (int i = 0; i < max_iter; i++) {
		int idx0= min(path_len, static_cast<int>(floor((float)rand() / (RAND_MAX+1)*(path_len +1))));
		int idx1= min(path_len, static_cast<int>(floor((float)rand() / (RAND_MAX+1)*(path_len +1))));
		if (idx0 > idx1) {
			idx0 += idx1;
			idx1 = idx0 - idx1;
			idx0 -= idx1;
		}
		else if (idx0 == idx1) {
			continue;
		}

		vector<int> rev_sub_path(best_path.rbegin() + path_len-idx1, best_path.rbegin() + path_len-idx0);

		int* np = new int[path_len];

		int* bp = &best_path[0];
		int* rp = &rev_sub_path[0];

		memcpy(np, bp, sizeof(int)*idx0);
		memcpy(np + idx0, rp, sizeof(int)*(idx1 - idx0));
		memcpy(np + idx1, bp + idx1, sizeof(int)*(path_len - idx1));

		float new_score = calc_score(np, path_len, cost_mat);
		if (new_score < best_score) {
			best_path.clear();
			best_path.assign(np, np + path_len);
			best_score = new_score;
		}
		delete[] np;
	}

	return best_path;
}

float** setupHMM(vector<vector<float> > &vals, int N, int M)
{
	float** temp;
	temp = new float*[N];
	for (unsigned i = 0; (i < N); i++)
	{
		temp[i] = new float[M];
		for (unsigned j = 0; (j < M); j++)
		{
			temp[i][j] = vals[i][j];
		}
	}
	return temp;
}

vector<int> simple_sa(vector<int> path, vector<vector<float>> cost_mat) {
	float temperature = 10;
	float delta_temperature = 0.97;

	float** arr_costmat = setupHMM(cost_mat, cost_mat.size(), cost_mat.at(0).size());
	int costmat_size = cost_mat.size();

	vector<int> cur_path(path);

	int* p = &cur_path[0];
	float cur_score = calc_score(p,cur_path.size(), arr_costmat);

	vector<int> best_path(cur_path);
	float best_score = cur_score;



	while (temperature >1) {
		vector<int> temp_path(cur_path.begin()+1, cur_path.end() - 1);
		vector<int> temp_path2(cur_path.begin(), cur_path.begin() + 1);
		vector<int> temp_path3(gen_trial_path_2opt(temp_path, arr_costmat));
		temp_path2.insert(temp_path2.end(),temp_path3.begin(), temp_path3.end());
		temp_path2.insert(temp_path2.end(), cur_path.end() - 1, cur_path.end());
		vector<int> trial_path = temp_path2;
		float trial_score = calc_score(trial_path, cost_mat);
		if ((float)rand()/RAND_MAX < calc_prob(cur_score, trial_score, temperature)) {
			cur_path.clear();
			cur_path.assign(trial_path.begin(), trial_path.end());
			cur_score = trial_score;
		}
		temperature *= delta_temperature;

		if (cur_score < best_score) {
			best_score = cur_score;
			best_path.clear();
			best_path.assign(cur_path.begin(), cur_path.end());
		}
		cout << temperature << endl;
	}

	for (int i = 0; i < costmat_size; i++) {
		delete[] arr_costmat[i];
	}
	delete[] arr_costmat;

	return best_path;
}

auto readFile(string filePath) {
	int index, x, y;
	char input[1000];
	ifstream vlsi(filePath.data());
	auto ret = make_shared<vector<array<int, 3>>>();
	// index x y
	while (!vlsi.eof()) {
		vlsi.getline(input, 20);
		stringstream inputString(input);
		inputString >> index >> x >> y;
		array<int, 3> temp{ index, x, y };
		ret->push_back(temp);
		cout << index << " " << x << " " << y << endl;
	}
	vlsi.close();
	return ret;
}

int getMinNode(const shared_ptr<vector<array<int, 3>>> node, int index) {
	int minValue = INT_MAX;
	for (auto iter = node->begin(); iter < node->cend(); ++iter) {
		if (iter->at(index) < minValue) {
			minValue = iter->at(index);
		}
	}
	return minValue;
}

int getMaxNode(const shared_ptr<vector<array<int, 3>>> node, int index) {
	int maxValue = -1;
	for (auto iter = node->begin(); iter < node->cend(); ++iter) {
		if (iter->at(index) > maxValue) {
			maxValue = iter->at(index);
		}
	}
	return maxValue;
}

vector<int> sorting(vector<float> &arr) {
	vector<int> retArr;
	vector<bool> visited;
	vector<float> sortedArr(arr);

	retArr.assign(arr.size(), -1);
	visited.assign(arr.size(), false);

	sort(sortedArr.begin(), sortedArr.end(), [](const auto &a1, const auto &a2)-> bool {
		return a1 < a2;
	});

	float* asortedArr = &sortedArr[0];
	float* aarr = &arr[0];
	int arr_size = arr.size();
	for (int i = 0; i < arr_size; i++) {
		for (int j = 0; j < arr_size; j++) {
			if (aarr[j] == asortedArr[i] && visited.at(j) != true) {
				retArr.at(i) = j;
				visited.at(j) = true;
				break;
			}
		}
	}
	return retArr;
}

vector<int> nearestNeighbor(shared_ptr<vector<array<int,3>>> node) {
	vector<vector<float>> cost_mat = calc_cost_mat(node.get());
	vector<bool> visited;
	visited.assign(node->size(), false);
	vector<int> path;
	path.assign(node->size(), 0);

	visited.at(0) = true;

	for (int i = 0; i < node->size(); i++) {
		vector<int> indexOfSortedArr = sorting(cost_mat.at(i));
		for (int j = 0; j < node->size(); j++) {
			if (!visited.at(indexOfSortedArr.at(j))) {
				path.at(i + 1) = indexOfSortedArr[j];
				visited.at(indexOfSortedArr.at(j)) = true;
				break;
			}
		}
		cout << i << endl;
	}
	for (int i = 0; i < path.size(); i++) {
		path.at(i) = path.at(i) + 1;
	}
	return path;
}

auto fixedStartCluster(shared_ptr<vector<array<int, 3>>> node) {
	const int chunk_size = 200;
	const int chunk_num = static_cast<int>(sqrt(node->size() / chunk_size));
	int x_min = getMinNode(node, 1);
	int y_min = getMinNode(node, 2);
	int chunk_x_size = ceil((float)(getMaxNode(node, 1) + 1 - x_min) / chunk_num);
	int chunk_y_size = ceil((float)(getMaxNode(node, 2) + 1 - y_min) / chunk_num);
	auto chunks = make_unique<vector<vector<vector<array<int, 3>>>>>();
	vector<vector<float>> cost_mat = calc_cost_mat(node.get());

	for (int i = 0; i < chunk_num; i++) {
		chunks->push_back(vector<vector<array<int, 3>>>());
		chunks->at(i).assign(chunk_num, vector<array<int, 3>>());
	}

	for (auto i = 0; i < node->size(); i++) {
		int y = static_cast<int>(floor((node->at(i).at(2) - y_min) / chunk_y_size));
		int x = static_cast<int>(floor((node->at(i).at(1) - x_min) / chunk_x_size));
		chunks->at(y).at(x).push_back(node->at(i));
	}
	int vectRow, vectCol;
	array<int, 3> last, first;

	for (int row = 0; row<chunks->size(); row++) {
		if (row % 2 == 0) {
			for (int col = 0; col < chunks->at(row).size(); col++) {
				vector<array<int,3>> vect= chunks->at(row).at(col);
				if (col == 0) {
					sort(vect.begin(), vect.end(), [chunk_x_size, chunk_y_size, row, col](const auto &a1, const auto &a2) -> bool {
						return pow((a1[1] - chunk_x_size*col), 2) + pow((a1[2] - chunk_y_size*row), 2) < pow((a2[1] - chunk_x_size*col), 2) + pow((a2[2] - chunk_y_size*row), 2);
					});
					first = vect.at(0);
					last = vect.at(vect.size() - 1);
				}
				else {
					sort(vect.begin(), vect.end(), [chunk_x_size, chunk_y_size, row, col](const auto &a1, const auto &a2) -> bool {
						return pow((a1[1] - chunk_x_size*col), 2) + pow((a1[2] - chunk_y_size*row), 2) < pow((a2[1] - chunk_x_size*col), 2) + pow((a2[2] - chunk_y_size*row), 2);
					});
					last = vect.at(vect.size() - 1);
					sort(vect.begin(), vect.end(), [chunk_x_size, chunk_y_size, row, col](const auto &a1, const auto &a2) -> bool {
						return pow(chunk_x_size*(col+1)-a1[1], 2) + pow((a1[2] - chunk_y_size*row), 2) > pow(chunk_x_size*(col + 1) - a2[1], 2) + pow((a2[2] - chunk_y_size*row), 2);
					});
					first = vect.at(0);
				}
				cout << first[0] <<" " << first[1] << " " << first[2] << " " << last[0] << " " << last[1] << " " << last[2] << endl;
				vect.erase(find(vect.begin(), vect.end(), last));
				vect.erase(find(vect.begin(), vect.end(), first));
				vect.push_back(last);
				vect.insert(vect.begin(), first);
				chunks->at(row).at(col) = vect;
			}
		}
		else {
			for (int col = chunks->at(row).size() - 1; col >= 0; col--) {
				vector<array<int, 3>> vect = chunks->at(row).at(col);
				if (col == chunks->at(row).size()-1) {
					sort(vect.begin(), vect.end(), [chunk_x_size, chunk_y_size, row, col](const auto &a1, const auto &a2) -> bool {
						return pow(chunk_x_size*(col + 1) - a1[1], 2) + pow((a1[2] - chunk_y_size*row), 2) < pow(chunk_x_size*(col + 1) - a2[1], 2) + pow((a2[2] - chunk_y_size*row), 2);
					});
					first = vect.at(0);
					last = vect.at(vect.size() - 1);
				}
				else {
					sort(vect.begin(), vect.end(), [chunk_x_size, chunk_y_size, row, col](const auto &a1, const auto &a2) -> bool {
						return pow((a1[1] - chunk_x_size*col), 2) + pow((a1[2] - chunk_y_size*row), 2) < pow((a2[1] - chunk_x_size*col), 2) + pow((a2[2] - chunk_y_size*row), 2);
					});
					first = vect.at(vect.size() - 1);
					sort(vect.begin(), vect.end(), [chunk_x_size, chunk_y_size, row, col](const auto &a1, const auto &a2) -> bool {
						return pow(chunk_x_size*(col + 1) - a1[1], 2) + pow((a1[2] - chunk_y_size*row), 2) < pow(chunk_x_size*(col + 1) - a2[1], 2) + pow((a2[2] - chunk_y_size*row), 2);
					});
					last = vect.at(vect.size() - 1);
				}
				cout << first[0] << " " << first[1] << " " << first[2] << " " << last[0] << " " << last[1] << " " << last[2] << endl;
				vect.erase(find(vect.begin(), vect.end(), last));
				vect.erase(find(vect.begin(), vect.end(), first));
				vect.push_back(last);
				vect.insert(vect.begin(), first);
				chunks->at(row).at(col) = vect;
			}
		}
	}
	vector<vector<vector<int>>> pathes;
	for (int i = 0; i < chunk_num; i++) {
		pathes.push_back(vector<vector<int>>());
		pathes.at(i).assign(chunk_num, vector<int>());
	}
	for (int row = 0; row < chunks->size(); row++) {
		for (int col = 0; col < chunks->at(row).size(); col++) {
			auto vect = chunks->at(row).at(col);
			vector<int> path;
			for (int i = 0; i < vect.size(); i++) {
				path.push_back(vect.at(i)[0]);
			}
			pathes.at(row).at(col) = simple_sa(path, cost_mat);
		}
	}
	/*
	for (auto outer = pathes.begin(); outer < pathes.cend(); ++outer) {
		for (auto inner = pathes.begin()->begin(); inner < pathes.begin()->cend(); ++inner) {
			auto vect = chunks->at(distance(pathes.begin(), outer)).at(distance(pathes.begin()->begin(), inner));
			cout << "@@@@@@@@@@@@@@@@@@@@" << endl;
			pathes[distance(pathes.begin(), outer)][distance(pathes.begin()->begin(), inner)] = simple_sa(vect, cost_mat);
		}
	}*/
	int part_sum_score = 0;
	vector<int>path;

	for (int row = 0; row < pathes.size(); row++) {
		for (int col = 0; col < pathes.at(row).size(); col++) {
			cout << pathes.at(row).at(col).at(0) <<" " <<pathes.at(row).at(col).at(pathes.at(row).at(col).size()-1) << endl;
		}
	}

	for (int row = 0; row < pathes.size(); row++) {
		if (row % 2 == 0) {
			for (int col = 0; col < pathes.at(row).size(); col++) {
				path.insert(path.end(), pathes.at(row).at(col).begin(), pathes.at(row).at(col).end());
			}
		}
		else {

			for (int col = pathes.at(row).size()-1; col >= 0; col--) {
				path.insert(path.end(), pathes.at(row).at(col).begin(), pathes.at(row).at(col).end());
			}
		}
	}
	float score = calc_score(path, cost_mat);
	cout << score << endl;
	return path;
}