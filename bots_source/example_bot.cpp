#include <bits/stdc++.h>

using namespace std;

struct Tank{
	double x = -1;
	double y = -1;
	double r = -1;
	double angle = -1;

	double health = -1;
	double max_health = -1;
	double speed = -1;

	double damage = -1;
	double bullet_speed = -1;
};

struct Bullet{
	double x = -1;
	double y = -1;
	double r = -1;
};

struct BonusMark{
	double x = -1;
	double y = -1;
	double r = -1;
};

int main() {
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	string s;
	cin >> s;
	if (s == "Defeat"){
		return 0;
	}

	int my_score = atoi(s.c_str());

	Tank my_tank;
	cin >> my_tank.x >> my_tank.y >> my_tank.r >> my_tank.angle;
	cin >> my_tank.health >> my_tank.max_health;
	cin >> my_tank.speed;
	cin >> my_tank.bullet_speed >> my_tank.damage;

	int my_bullets_count;
	cin >> my_bullets_count;
	vector<Bullet> my_bullets(my_bullets_count);
	for (auto& bullet : my_bullets){
		cin >> bullet.x >> bullet.y >> bullet.r;
	}

	int enemies_count;
	cin >> enemies_count;

	vector<tuple<int, int, Tank, vector<Bullet>>> enemies(enemies_count);

	for (int i = 0; i < enemies_count; i++){
		int is_enemy_alive;
		cin >> is_enemy_alive;

		auto& [enemy_score, enemy_uid, enemy_tank, enemy_bullets] = enemies[i];
		cin >> enemy_score >> enemy_uid;

		if (is_enemy_alive){
			cin >> enemy_tank.x >> enemy_tank.y >> enemy_tank.r >> enemy_tank.angle;
		}

		int enemy_bullets_count;
		cin >> enemy_bullets_count;
		enemy_bullets.resize(enemy_bullets_count);

		for (auto& bullet : enemy_bullets){
			cin >> bullet.x >> bullet.y >> bullet.r;
		}
	}

	int bonus_mark_count;
	cin >> bonus_mark_count;

	vector<BonusMark> bonus_marks(bonus_mark_count);
	for (auto& bonus_mark : bonus_marks){
		cin >> bonus_mark.x >> bonus_mark.y >> bonus_mark.r;
	}

	string memory_string;
	cin.ignore();
	getline(cin, memory_string);

	int uid_mn = 1e9;
	pair<double, double> move_point = {0, 0};

	for (int i = 0; i < enemies_count; i++){
		auto& [enemy_score, enemy_uid, enemy_tank, enemy_bullets] = enemies[i];
		if (enemy_tank.x == -1){
			continue;
		}
		if (enemy_uid < uid_mn){
			uid_mn = enemy_uid;
			move_point = {enemy_tank.x, enemy_tank.y};
		}
	}

	cout << "move " << move_point.first << ' ' << move_point.second << '\n';
	cout << "shoot\n";

    return 0;
}