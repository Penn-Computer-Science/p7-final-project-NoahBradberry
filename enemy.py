import random
import math

class Enemy:
    def __init__(self, canvas, x, y, length, color, health, speed, type):
        self.canvas = canvas
        self.health = health
        self.speed = speed
        self.type = type
        self.length = length
        self.id = canvas.create_rectangle(x, y, x + length, y + length, fill = color)

    def move_towards_player(self, player_x, player_y):
        ex1, ey1, ex2, ey2 = self.canvas.coords(self.id)

        center_x = (ex1 + ex2) / 2
        center_y = (ey1 + ey2) / 2

        dx = player_x - center_x
        dy = player_y - center_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return
        
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        self.canvas.move(self.id, move_x, move_y)
    
    def take_damage(self, enemies):
        self.health -= 1

        if self.health <= 0:
            self.die(enemies)
    
    def die(self, enemies):
        self.canvas.delete(self.id)

        if self in enemies:
            enemies.remove(self)

class TankEnemy(Enemy):
    def __init__(self, canvas, x, y, length):

        super().__init__(canvas, x, y, length, "#7F1D1D", 3, 2, "tank")

    def take_damage(self, enemies):
        self.health -= 1
        
        if self.health == 2:
            self.itemconfig(self.id, fill = "#DC2626")
        elif self.health == 1:
            self.itemconfig(self.id, fill = "#F87171")
        elif self.health == 0:
            self.canvas.delete(self.id)
            if self in enemies:
                enemies.remove(self)


class SplitterEnemy(Enemy):
    def __init__(self, canvas, x, y, length):

        super().__init__(canvas, x, y, length, "green", 2, 3, "splitter")

    def die(self, enemies):
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        self.canvas.delete(self.id)

        if self in enemies:
            enemies.remove(self)

        enemy1 = Enemy(self.canvas, x1, y1, self.length, "lightgreen", 1, 4, "mini_splitter")
        enemy2 = Enemy(self.canvas, x1 + self.length, y1, self.length, "lightgreen", 1, 4, "mini_splitter")
        enemies.append(enemy1)
        enemies.append(enemy2)

