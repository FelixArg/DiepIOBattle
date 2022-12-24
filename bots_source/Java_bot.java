import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Java_bot {
    public static void main(String[] args) throws FileNotFoundException {
        InputStream inputStream = System.in;
        OutputStream outputStream = System.out;
        InputReader in = new InputReader(inputStream);
        PrintWriter out = new PrintWriter(outputStream);
        solve(in, out);
        out.close();
    }

    static class Tank {
        double x = -1;
        double y = -1;
        double r = -1;
        double angle = -1;

        double health = -1;
        double max_health = -1;
        double speed = -1;

        double damage = -1;
        double bullet_speed = -1;
    }

    ;

    static class Bullet {
        double x = -1;
        double y = -1;
        double r = -1;
    }

    ;

    static class BonusMark {
        double x = -1;
        double y = -1;
        double r = -1;
        double h = -1;
    }

/* create jar file:
javac Java_bot.java
jar cmvf MANIFEST.MF myJar.jar *.class
# запустить
java -jar myJar.jar
* */
    static void solve(InputReader in, PrintWriter out) {

        String s;
        s = in.next();
        if (s.equals("Defeat")) {
            return;
        }
        int tick = Integer.parseInt(s);
        double my_score = in.nextDouble();

        Tank my_tank = new Tank();
        my_tank.x = in.nextDouble();
        my_tank.y = in.nextDouble();
        my_tank.r = in.nextDouble();
        my_tank.angle = in.nextDouble();
        my_tank.health = in.nextDouble();
        my_tank.max_health = in.nextDouble();
        my_tank.speed = in.nextDouble();
        my_tank.bullet_speed = in.nextDouble();
        my_tank.damage = in.nextDouble();


        int my_bullets_count = in.nextInt();
        List<Bullet> my_bullets = new ArrayList<Bullet>(my_bullets_count);
        for (int i = 0; i < my_bullets_count; i++) {
            Bullet bullet = new Bullet();
            bullet.x = in.nextDouble();
            bullet.y = in.nextDouble();
            bullet.r = in.nextDouble();
            my_bullets.add(bullet);
        }

        int enemies_count = in.nextInt();

        List<Integer> enemies_score = new ArrayList<>(enemies_count);
        List<Integer> enemies_uid = new ArrayList<>(enemies_count);
        List<Tank> enemies_tank = new ArrayList<>(enemies_count);
        List<Bullet> enemies_bullets = new ArrayList<>(enemies_count);

        for (int i = 0; i < enemies_count; i++) {
            int is_enemy_alive = in.nextInt();
            enemies_score.add(in.nextInt());
            enemies_uid.add(in.nextInt());

            if (is_enemy_alive == 1) {
                Tank enemy_tank = new Tank();
                enemy_tank.health = in.nextDouble();
                enemy_tank.x = in.nextDouble();
                enemy_tank.y = in.nextDouble();
                enemy_tank.r = in.nextDouble();
                enemy_tank.angle = in.nextDouble();
                enemies_tank.add(enemy_tank);
            }

            int enemy_bullets_count = in.nextInt();

            for (int j = 0; j < enemy_bullets_count; j++) {
                Bullet bullet = new Bullet();
                bullet.x = in.nextDouble();
                bullet.y = in.nextDouble();
                bullet.r = in.nextDouble();
                enemies_bullets.add(bullet);
            }
        }

        int bonus_mark_count = in.nextInt();

        List<BonusMark> bonus_marks = new ArrayList<>(bonus_mark_count);

        for (int i = 0; i < enemies_count; i++) {
            BonusMark bonus_mark = new BonusMark();
            bonus_mark.h = in.nextDouble();
            bonus_mark.x = in.nextDouble();
            bonus_mark.y = in.nextDouble();
            bonus_mark.r = in.nextDouble();
        }

        String memory_string = in.nextLine();

        int uid_mn = (int) 1e9;
        double x = 0, y = 0;

        for (int i = 0; i < enemies_count; i++) {
            if (enemies_tank.get(i).x == -1) {
                continue;
            }
            if (enemies_uid.get(i) < uid_mn) {
                uid_mn = enemies_uid.get(i);
                x = enemies_tank.get(i).x;
                y = enemies_tank.get(i).y;
            }
        }
        out.print("move ");
        out.print(x);
        out.print(' ');
        out.print(y);
        out.print('\n');
        out.print("shoot\n");
    }

    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;

        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 32768);
            tokenizer = null;
        }

        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }

        public String nextLine() {
            try {
                return reader.readLine();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        int nextInt() {
            return Integer.parseInt(next());
        }

        double nextDouble() {
            return Double.parseDouble(next());
        }

        long nextLong() {
            return Long.parseLong(next());
        }
    }
}