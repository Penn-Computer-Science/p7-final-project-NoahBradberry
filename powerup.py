import random
import math
import time

class Powerup:
    def __init__(self, canvas, x, y, radius, speed, color, type):
        self.canvas = canvas
        self.speed = speed
        self.type = type
        self.radius = radius
        self.target_x = random.randint(0, 1920)
        self.target_y = random.randint(0, 1080)
        self.id = canvas.create_oval(x, y, x + radius, y + radius, fill = color)

    def move(self):
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        center_x = (x2 + x1) / 2
        center_y = (y2 + y1) / 2

        dx = self.target_x - center_x
        dy = self.target_y - center_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance < 2:
            self.target_x = random.randint(0, 1920)
            self.target_y = random.randint(0, 1080)
        
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        self.canvas.move(self.id, move_x, move_y)

    def collect(self, powerups):
        self.canvas.delete(self.id)

        if self in powerups:
            powerups.remove(self)
    
class SpreadShot(Powerup):
    def __init__(self, canvas, x, y, radius, speed):

        super().__init__(canvas, x, y, radius, speed, "#F97316", "spread_shot")
    
    def activate(spread_shot, active_powerups):
        spread_shot = True
        active_powerups["spread_shot"] = time.time() + 5

        return(spread_shot, active_powerups)

class HealthPowerup(Powerup):
    def __init__(self, canvas, x, y, radius, speed):

        super().__init__(canvas, x, y, radius, speed, "#32CD32", "health")

    def activate(health):
        if health + 50 > 500:
            health = 500
        else:
            health += 50
        
        return(health)

class BiggerBullets(Powerup):
    def __init__(self, canvas, x, y, radius, speed):

        super().__init__(canvas, x, y, radius, speed, "#DC2626", "bigger_bullets")

    def activate(bigger_bullets, active_powerups):
        bigger_bullets = True
        active_powerups["bigger_bullets"] = time.time() + 5

        return(bigger_bullets, active_powerups)

class PiercingBullets(Powerup):
    def __init__(self, canvas, x, y, radius, speed):

        super().__init__(canvas, x, y, radius, speed, "#7E22CE", "piercing_bullets")

    def activate(piercing, active_powerups):
        piercing = True
        active_powerups["piercing_bullets"] = time.time() + 5       

