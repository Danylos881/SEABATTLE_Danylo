import random

class BoardOutException(Exception):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Ship:
    def __init__(self, length, direction, bow):
        self.length = length
        self.direction = direction
        self.bow = bow
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            x, y = self.bow.x, self.bow.y
            if self.direction == 'horizontal':
                x += i
            elif self.direction == 'vertical':
                y += i
            ship_dots.append(Dot(x, y))
        return ship_dots

    def shoot_at(self, shot):
        if shot in self.dots():
            self.lives -= 1
            return True
        return False

    def is_sunk(self):
        return self.lives == 0

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.shots = set()
        self.ships = []
        self.living_ships = 0

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or not self.contour(dot):
                raise BoardOutException()
        for existing_ship in self.ships:
            for dot in existing_ship.dots():
                if not self.contour(dot):
                    raise BoardOutException()
        self.ships.append(ship)
        self.living_ships += 1
        for dot in ship.dots():
            self.grid[dot.x][dot.y] = '■'

    def contour(self, point):
        x, y = point.x, point.y
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (0 <= x + i < self.size) and (0 <= y + j < self.size) and self.grid[x + i][y + j] == '■':
                    return False
        return True

    def out(self, point):
        return not (0 <= point.x < self.size and 0 <= point.y < self.size)

    def shoot_at(self, point):
        if self.out(point):
            raise BoardOutException()
        if point in self.shots:
            return False
        x, y = point.x, point.y
        self.shots.add(point)
        if self.grid[x][y] == ' ':
            self.grid[x][y] = 'T'
            return False
        for ship in self.ships:
            if not ship.is_sunk():
                if ship.shoot_at(point):
                    self.grid[x][y] = 'X'
                    if ship.is_sunk():
                        self.living_ships -= 1
                    return True
        return False

    def print_board(self, hide=False):
        header = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        print(header)
        for i in range(self.size):
            row = [str(i + 1)]
            for j in range(self.size):
                if hide and self.grid[i][j] == '■':
                    row.append(' ')
                else:
                    row.append(self.grid[i][j])
            print(" | ".join(row) + " |")

class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board
        self.shots = set()

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                if target in self.shots:
                    print("Вы уже стреляли в эту клетку. Попробуйте ещё раз.")
                    continue
                self.shots.add(target)
                success = self.enemy_board.shoot_at(target)
                self.enemy_board.print_board()
                if success:
                    print("Попадание!")
                    if self.enemy_board.living_ships == 0:
                        print("Победа!")
                        return
                else:
                    print("Промах!")
            except BoardOutException:
                print("Недопустимый ход. Попробуйте ещё раз.")

class AI(Player):
    def ask(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)

class User(Player):
    def ask(self):
        try:
            x, y = map(int, input("Ваш ход (введите координаты x и y через пробел): ").split())
            return Dot(x - 1, y - 1)
        except (ValueError, IndexError):
            raise BoardOutException()

class Game:
    def __init__(self):
        self.own_board_user = Board(6)
        self.enemy_board_user = Board(6)
        self.own_board_ai = Board(6)
        self.enemy_board_ai = Board(6)
        self.user = User(self.own_board_user, self.enemy_board_ai)
        self.ai = AI(self.own_board_ai, self.enemy_board_user)

    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Формат ввода координат: x y (например, '1 2')")
        print("Поле представлено в формате 6x6.")

    def loop(self):
        while True:
            print("Доска игрока:")
            self.own_board_user.print_board()
            print("Доска компьютера:")
            self.enemy_board_user.print_board(hide=True)
            self.user.move()
            if self.enemy_board_user.living_ships == 0:
                print("Игрок победил!")
                break
            self.ai.move()
            if self.enemy_board_ai.living_ships == 0:
                print("Компьютер победил!")
                break

    def start(self):
        self.greet()
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()