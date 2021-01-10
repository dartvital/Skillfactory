from random import randint

class Dot:
    #класс точек
    def __init__(self, x, y):
        self.x = x #Точка на доске по вертикали
        self.y = y #Точка на доске по горизонтали
    
    #Проверка равенства точек, используется магический метод "__eq__". Позволит определить входит ли точка в координаты корабля
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    #Метод позволяет преобразовать представление значения в строку, используется магический метод "__repr__":
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    #Создаем классы исключений
    
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски!"
    
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"
    
class BoardWrongShipException(BoardException):
    pass   

class Ship:
    #класс корабля
    
    def __init__(self, bow, length, orient):
        self.bow = bow       #Нос корабля, точка
        self.length = length #Длина корабля
        self.orient = orient #Если значение 1, то горизонтальное расположение, если 0 - вертикальное
        
        self.lives = length  #Задаем значение от чего будет зависеть количество жизней корабля
        
    #Точки корабля
    @property
    def dots(self):
        ship_dots = []
      
        for i in range(self.length):   #Перебираем точки коробля в пределах длины корабля
            
            cur_x = self.bow.x         #Фиксируем точки коробля
            cur_y = self.bow.y
            
            if self.orient == 0:
                cur_x += i             
            else:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y)) #Добавляем точки коробля в список
            
        return ship_dots
    
    def shooten(self, shot):
        return shot in self.dots    
            
                 
class Board:
    #класс доски
    
    def __init__(self,  hid = False, size = 6):
        self.hid = hid  #Будем импользовать для того, чтобы скрывать доску противника
        self.size = size #Размер доски, по умолчанию задали значение "6х6"
        
        self.count = 0   #счетчик пораженных кораблей на доске
        self.field = [["0"]*size for _ in range(size)] #Создаем поле заданного размера
        self.busy = []
        self.ships = []
         
    #Добавление кораблей
    def add_ship(self, ship):
        
        for d in ship.dots:                        #Вызываем исключение на проверку правильности ввода корабля
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
                
        for d in ship.dots:                        #Устанавливаем символ корабля и добавляем точку в список занятых клеток
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
            
        self.ships.append(ship)                    # 
        self.contour(ship)                         # 

        
    def contour (self, ship, verb = False):                           #Очерчиваем контуры корабля
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                        
                if not(self.out(cur)) and cur not in self.busy:         #Проверка, что точка находится в пределах поля и не занята
                    if verb:                                            #Очерчиваем контуры только в случае полного уничтожения корабля
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)                               #
                    
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 | "                         #Номера столбцов
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " | "            #В цикле нумеруем строки, добавляем разделитель
                       
        if self.hid:
            res = res.replace("■", "O")                               #Скрываем поле c кораблями противника
    
        return res
    
    def out(self, d):                                                 #данным методом определяем принадлежность точек доске
        return not((0<= d.x < self.size) and (0<= d.y < self.size))
    
    def shot(self, d):

        if self.out(d):                                               #Ловим исключения: выстрел за пределы доски и в ту же точку
            raise BoardOutException()
            
        if d in self.busy:
            raise BoardUsedException()
            
        self.busy.append(d)
            
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
            
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
            
    def begin(self):      #Обнуление списка занятых точек                                    
        self.busy = []
    
           
class Player:
    
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
        
    def ask(self):
        raise NotImplemetedError()
        
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat                
            except BoardException as e:
                print(e)
                    
class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0,5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")    #Отображается ход компьютера в консоли
        return d
    
class User(Player):
    def ask(self):
        while True:
            cords = input(" Ваш ход: " ).split()
            
            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue
                
            x, y = cords
            
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue
                
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1) 
        
class Game:
    
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
        
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for lengh in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), lengh, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
    
    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        

    def loop(self):
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
                               
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1 
                
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выйграл!")
                break
                
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выйграл!")
                break
            num += 1
    
    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()
   