#include <bits/stdc++.h>

using namespace std;
mt19937 rng(chrono::high_resolution_clock().now().time_since_epoch().count());

const int world_width = 1500;
const int world_height = 950;
const double eps = 1;

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

vector<string> split(const string& s){
	vector<string> res;
	string token = "";
	for (int i = 0; i < s.size(); i++){
		if (s[i] == ' '){
			if (!token.empty()){
				res.emplace_back(token);
			}
			token = "";
		}
		token += s[i];
	}

	if (!token.empty()){
		res.emplace_back(token);
	}
	return res;
}

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

	auto mem = split(memory_string);

	pair<double, double> move_point = {rng() % world_width, rng() % world_height};
	pair<int,int> agressive = {rng() % 51 + 30, rng() % 201 + 50};

	if (mem.size() >= 2){
		double x = atof(mem[0].c_str());
		double y = atof(mem[1].c_str());

		if (fabs(my_tank.x - x) > eps || fabs(my_tank.y - y) > eps){
			move_point = {x, y};
		}

		int speed = atoi(mem[2].c_str());
		int damage = atoi(mem[3].c_str());
		agressive = {speed, damage};
	}

	double dist = 1e9;
	pair<double, double> target = {0, 0};

	for (const auto& bonus_mark : bonus_marks){
		double dist_cur = sqrt((bonus_mark.x - my_tank.x) * (bonus_mark.x - my_tank.x)
		+ (bonus_mark.y - my_tank.y) * (bonus_mark.y - my_tank.y));
		if (dist_cur < dist){
			dist = dist_cur;
			target = {bonus_mark.x, bonus_mark.y};
		}
	}

	if (my_tank.speed >= agressive.first && my_tank.damage >= agressive.second){
		dist = 1e9;
		for (int i = 0; i < enemies_count; i++){
			auto& [enemy_score, enemy_uid, enemy_tank, enemy_bullets] = enemies[i];
			if (enemy_tank.x == -1){
				continue;
			}

			double dist_cur = sqrt((enemy_tank.x - my_tank.x) * (enemy_tank.x - my_tank.x)
			+ (enemy_tank.y - my_tank.y) * (enemy_tank.y - my_tank.y));
			if (dist_cur < dist){
				dist = dist_cur;
				target = {enemy_tank.x, enemy_tank.y};
				move_point = {enemy_tank.x, enemy_tank.y};
				if (dist < 10){
					move_point = {rng() % world_width, rng() % world_height};
				}
			}
		}
	}

	pair<double, double> vec = {target.first - my_tank.x, target.second - my_tank.y};

	double angle = atan2(vec.second, vec.first);
	double pi = acos(-1);
	if (angle < 0){
		angle += 2 * pi;
	}

	double d_angle = angle - my_tank.angle;

	cout << "move " << move_point.first << ' ' << move_point.second << '\n';
	cout << "turn " << d_angle << '\n';
	cout << "shoot\n";
	if (my_tank.speed < agressive.first){
		cout << "upgrade speed\n";
	}
	else{
		cout << "upgrade damage\n";
	}
	cout << "memory " << move_point.first << ' ' << move_point.second <<
	' ' << agressive.first << ' ' << agressive.second << '\n';

    return 0;
}