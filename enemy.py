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
    
    def take_damage(self, enemies, player = None, damage_player = None):
        self.health -= 1

        if self.health <= 0:
            self.die(enemies, player, damage_player)
    
    def die(self, enemies, player = None, damage_player = None):
        self.canvas.delete(self.id)

        if self in enemies:
            enemies.remove(self)

class NormalEnemy(Enemy):
    def __init__(self, canvas, x, y, length):

        super().__init__(canvas, x, y, length, "purple", 1, 3, "normal")

class TankEnemy(Enemy):
    def __init__(self, canvas, x, y, length):

        super().__init__(canvas, x, y, length, "#7F1D1D", 3, 2, "tank")

    def take_damage(self, enemies, player = None, take_damage = None):
        self.health -= 1
        
        if self.health == 2:
            self.canvas.itemconfig(self.id, fill = "#DC2626")
        elif self.health == 1:
            self.canvas.itemconfig(self.id, fill = "#F87171")
        elif self.health == 0:
            self.canvas.delete(self.id)
            if self in enemies:
                enemies.remove(self)

class SpeedyEnemy(Enemy):
    def __init__(self, canvas, x, y, length):
        
        super().__init__(canvas, x, y, length, "#E0115F", 1, 6, "speedy")


class SplitterEnemy(Enemy):
    def __init__(self, canvas, x, y, length):

        super().__init__(canvas, x, y, length, "green", 1, 3, "splitter")

    def die(self, enemies, player = None, damage_player = None):
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        self.canvas.delete(self.id)

        if self in enemies:
            enemies.remove(self)

        enemy1 = Enemy(self.canvas, x1, y1, self.length, "lightgreen", 1, 4, "mini_splitter")
        enemy2 = Enemy(self.canvas, x1 + self.length, y1, self.length, "lightgreen", 1, 4, "mini_splitter")
        enemies.append(enemy1)
        enemies.append(enemy2)

class KamikazeEnemy(Enemy):
    def __init__(self, canvas, x, y, length):

        super().__init__(canvas, x, y, length, "#D0571C", 1, 3, "kamikaze")

    def die(self, enemies, player = None, damage_player = None):
        ex1, ey1, ex2, ey2 = self.canvas.coords(self.id)

        explosion_radius = 100

        explosion = self.canvas.create_oval(ex1 - explosion_radius, ey1 - explosion_radius, ex2 + explosion_radius, ey2 + explosion_radius, fill = "red")

        x1, y1, x2, y2 = self.canvas.coords(explosion)

        for enemy in enemies[:]:
            if enemy == self:
                continue

            bbox = self.canvas.bbox(enemy.id)

            if bbox == None:
                continue

            ex1_o, ey1_o, ex2_o, ey2_o = bbox

            if x1 < ex2_o and x2 > ex1_o and y1 < ey2_o and y2 > ey1_o:
                enemy.canvas.delete(enemy.id)

                if enemy in enemies:
                    enemies.remove(enemy)
            
        self.canvas.after(100, lambda: self.canvas.delete(explosion))
        self.canvas.delete(self.id)
        if self in enemies:
            enemies.remove(self)
            
        if player is not None and damage_player is not None:
            px1, py1, px2, py2, = self.canvas.coords(player)
            if x1 < px2 and x2 > px1 and y1 < py2 and y2 > py1:
                    damage_player(50)

            

