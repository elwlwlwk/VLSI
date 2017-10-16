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

vector<vector<double>> calc_cost_mat(vector<array<int, 3>>* data) {
	vector<vector<double>> cost_mat(data->size(), vector<double>(data->size()));
	array<int, 3> p1;
	array<int, 3> p2;
	for (auto i = 0; i < cost_mat.size(); i++) {
		for (auto j = 0; j < cost_mat.size(); j++) {
			p1 = data->at(i);
			p2 = data->at(j);
			double distance = sqrt(pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2));
			cost_mat.at(p1[0] - 1).at(p2[0] - 1) = cost_mat.at(p2[0] - 1).at(p1[0] - 1) = distance;
		}
	}
	return cost_mat;
}

double calc_score(vector<int> path, vector<vector<double>> &cost_mat) {
	double cost = 0;
	for (auto i = 0; i < path.size() - 1; i++) {
		cost += cost_mat.at(path.at(i) - 1).at(path.at(i + 1) - 1);
	}
	return cost;
}

double calc_prob(double best_score, double trial_score, double temperature) {
	if (best_score> trial_score) {
		return 1;
	}
	else {
		return pow(2.71828, (best_score - trial_score) / temperature);
	}
}

double get_inter_cost(vector<vector<int>> paths, vector<vector<double>> cost_mat) {
	double inter_cost = 0;
	double last_point = -1;
	double first_point = -1;
	for (auto idx = 0; idx < paths.size() - 1; idx++) {
		if (paths[idx].size() != 0) {
			last_point = paths.at(idx).back();
		}
		if (paths[idx + 1].size() != 0) {
			first_point = paths.at(idx + 1).at(0) - 1;
		}
		if (last_point != -1 && first_point != -1) {
			inter_cost += static_cast<double>(cost_mat.at(first_point).at(last_point));
			last_point = -1;
			first_point = -1;
		}
	}
	return inter_cost;
}


vector<int> gen_trial_path_2opt(vector<int> path, vector<vector<double>> cost_mat) {
	vector<int>best_path(path);
	double best_score = 999999999;

	int max_iter = 5000;
	for (int i = 0; i < max_iter; i++) {
		vector<int> idxs;

		idxs.push_back(min((int)path.size() - 1, static_cast<int>(floor((double)rand() / RAND_MAX*(path.size()+1)))));
		idxs.push_back(min((int)path.size() - 1, static_cast<int>(floor((double)rand() / RAND_MAX*(path.size()+1)))));
		sort(idxs.begin(), idxs.end());

		vector<int> new_path;
		vector<int> rev_sub_path(best_path.begin() + idxs.at(0), best_path.begin() + idxs.at(1));
		reverse(rev_sub_path.begin(), rev_sub_path.end());
		new_path.insert(new_path.end(), best_path.begin(), best_path.begin() + idxs.at(0));
		new_path.insert(new_path.end(), rev_sub_path.begin(), rev_sub_path.end());
		new_path.insert(new_path.end(), best_path.begin() + idxs.at(1), best_path.end());

		double new_score = calc_score(new_path, cost_mat);
		if (new_score < best_score) {
			best_path.clear();
			best_path.assign(new_path.begin(), new_path.end());
			best_score = new_score;
		}
	}

	return best_path;
}

vector<int> simple_sa(vector<array<int, 3>> data, vector<vector<double>> cost_mat) {
	double temperature = 10;
	double delta_temperature = 0.97;

	vector<int> cur_path;
	int a = data.size();
	cur_path.assign(a, -1);
	for (auto i = 0; i < cur_path.size(); i++) {
		cur_path[i] = data[i][0];
	}
	double cur_score = calc_score(cur_path, cost_mat);

	vector<int> best_path(cur_path);
	double best_score = cur_score;

	while (temperature >1) {
		vector<int> temp_path(cur_path.begin()+1, cur_path.end() - 1);
		vector<int> temp_path2(cur_path.begin(), cur_path.begin() + 1);
		vector<int> temp_path3(gen_trial_path_2opt(temp_path, cost_mat));
		temp_path2.insert(temp_path2.end(),temp_path3.begin(), temp_path3.end());
		temp_path2.insert(temp_path2.end(), cur_path.end() - 1, cur_path.end());
		vector<int> trial_path = temp_path2;
		double trial_score = calc_score(trial_path, cost_mat);
		if ((double)rand()/RAND_MAX < calc_prob(cur_score, trial_score, temperature)) {
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

auto fixedStartCluster(shared_ptr<vector<array<int, 3>>> node) {
	const int chunk_size = 400;
	const int chunk_num = static_cast<int>(sqrt(node->size() / chunk_size));
	int x_min = getMinNode(node, 1);
	int y_min = getMinNode(node, 2);
	int chunk_x_size = ceil((double)(getMaxNode(node, 1) + 1 - x_min) / chunk_num);
	int chunk_y_size = ceil((double)(getMaxNode(node, 2) + 1 - y_min) / chunk_num);
	auto chunks = make_unique<vector<vector<vector<array<int, 3>>>>>();
	vector<vector<double>> cost_mat = calc_cost_mat(node.get());

	for (int i = 0; i < chunk_num; i++) {
		chunks->push_back(vector<vector<array<int, 3>>>());
		chunks->at(i).assign(chunk_num, vector<array<int, 3>>());
	}

	for (auto i = 0; i < node->size(); i++) {
		int y = static_cast<int>(floor((node->at(i).at(2) - y_min) / chunk_y_size));
		int x = static_cast<int>(floor((node->at(i).at(1) - x_min) / chunk_x_size));
		cout << node->at(i).at(2) << " " << y_min << " " << chunk_y_size << " " << chunk_num<< endl;
		chunks->at(y).at(x).push_back(node->at(i));
		cout << y << " " << x << " " << chunks->at(y).at(x).size() << endl;
	}
	int vectRow, vectCol;
	array<int, 3> last, first;

	for (int row = 0; row<chunks->size(); row++) {
		if (row % 1 == 0) {
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
					first = vect.at(vect.size() - 1);
				}
				vect.erase(find(vect.begin(), vect.end(), last));
				vect.erase(find(vect.begin(), vect.end(), first));
				vect.push_back(last);
				vect.insert(vect.begin(), first);
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
				vect.erase(find(vect.begin(), vect.end(), last));
				vect.erase(find(vect.begin(), vect.end(), first));
				vect.push_back(last);
				vect.insert(vect.begin(), first);
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
			pathes.at(row).at(col) = simple_sa(vect, cost_mat);
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
		if (row % 2 == 0) {
			for (int col = 0; col < pathes.at(row).size(); col++) {
				path.insert(path.end(), pathes.at(row).at(col).begin(), pathes.at(row).at(col).end());
			}
		}
		else {
			vector<int> reversed_path;
			for (int col = 0; col < pathes.at(row).size(); col++) {
				reversed_path.insert(reversed_path.end(), pathes.at(row).at(col).begin(), pathes.at(row).at(col).end());
			}
			reverse(reversed_path.begin(), reversed_path.end());
			path.insert(path.end(), reversed_path.begin(), reversed_path.end());
		}
	}
	double score = calc_score(path, cost_mat);
	cout << score << endl;
	return path;
}