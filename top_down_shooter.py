#TODO Health, damage, game over, shooting rate limit, reload, score, sound?, death animation, health bar and score UI, enemy typrs (faster, tanks, shoot back), waves, gun upgrades (increase limit, spread shot, bigger bullets)

import tkinter as tk
import random
import math

PLAYER_LENGTH = 25
PLAYER_VELO = 5
ENEMY_LENGTH = 25
ENEMY_VELO = 4
BULLET_VELO = 10

root = tk.Tk()
root.title("Top-Down Shooter")
root.attributes("-fullscreen", True)

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

canvas = tk.Canvas(root, bg = "black")
canvas.pack(fill=tk.BOTH, expand=True)

class Bullet:
     def __init__(self, canvas, x1, y1, x2, y2, dx, dy):
        self.canvas = canvas
        self.dx = dx
        self.dy = dy

        self.id = canvas.create_oval(x1, y1, x2, y2, fill = "red")

     def move(self):
        self.canvas.move(self.id, self.dx, self.dy)

def reset(event = None):
    global player, enemies, bullets, health, alive
    alive = True
    enemies = []
    bullets = []
    health = 100
    canvas.delete("all")
    player = canvas.create_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 + PLAYER_LENGTH, SCREEN_HEIGHT // 2 + PLAYER_LENGTH, fill = "cyan")
    if alive == False:
        game_loop()
        make_enemy()

def make_enemy():
    global enemy
    spawn_side = random.randint(1, 4)
    start_x = random.randint(0, SCREEN_WIDTH)
    start_y = random.randint(0, SCREEN_HEIGHT)

    if spawn_side == 1:
        enemy = canvas.create_rectangle(- ENEMY_LENGTH, start_y , 0, start_y + ENEMY_LENGTH, fill = "green" )
        enemies.append(enemy)
    elif spawn_side == 2:
        enemy = canvas.create_rectangle(start_x, SCREEN_HEIGHT , start_x + ENEMY_LENGTH, SCREEN_HEIGHT + ENEMY_LENGTH, fill = "green" )
        enemies.append(enemy)
    elif spawn_side == 3:
        enemy = canvas.create_rectangle(SCREEN_WIDTH, start_y, SCREEN_WIDTH + ENEMY_LENGTH, start_y + ENEMY_LENGTH, fill = "green")
        enemies.append(enemy)
    elif spawn_side == 4:
         enemy = canvas.create_rectangle(start_x, 0 , start_x + ENEMY_LENGTH, 0 - ENEMY_LENGTH, fill = "green")
         enemies.append(enemy)
    
    root.after(2000, make_enemy)

def move_enemies():
    px1, py1, px2, py2 = canvas.coords(player)
    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2

    for enemy in enemies[:]:
        ex1, ey1, ex2, ey2 = canvas.coords(enemy)
        enemy_center_x = (ex2 + ex1) / 2
        enemy_center_y = (ey2 + ey1) / 2

        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            continue  
    
        move_x = (dx / distance) * ENEMY_VELO
        move_y = (dy / distance) * ENEMY_VELO

        canvas.move(enemy, move_x, move_y)

def shoot(event):
    px1, py1, px2, py2 = canvas.coords(player)
    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2
    mouse_x = event.x
    mouse_y = event.y

    distance_x = player_center_x - mouse_x
    distance_y = player_center_y - mouse_y
    relative_distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    dx = (distance_x / relative_distance) * BULLET_VELO
    dy = (distance_y / relative_distance) * BULLET_VELO

    bullets.append(Bullet(canvas, px1 + 5, py1 + 5, px2 - 5, py2 - 5, -dx, -dy))

def check_delete(bullet):
    bx1, by1, bx2, by2 = canvas.coords(bullet.id)
    if bx2 < 0 or bx1 > SCREEN_WIDTH or by1 > SCREEN_HEIGHT or by2 < 0:
        canvas.delete(bullet.id)
        bullets.remove(bullet)

def check_hit(bullet):
    bx1, by1, bx2, by2 = canvas.bbox(bullet.id)

    for enemy in enemies[:]:
        ex1, ey1, ex2, ey2 = canvas.bbox(enemy)

        if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
            canvas.delete(bullet.id, enemy)
            bullets.remove(bullet)
            enemies.remove(enemy)

def check_collision_player(enemy):
    global health
    try:
        px1, py1, px2, py2 = canvas.coords(player)
        ex1, ey1, ex2, ey2 = canvas.coords(enemy)

        if px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1:
            health -= 10
    except:
        return

def game_over():
    global alive
    alive = False
    canvas.delete("all")

    game_over_text = canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text= "Game Over. Press r to Restart", fill = "white", font=("Arial", 12))

keys = {
        "Left": False,
        "Right": False,
        "Up": False,
        "Down": False
}

def key_press(event):
       if event.keysym in keys:
            keys[event.keysym] = True

def key_release(event):
       if event.keysym in keys:
              keys[event.keysym] = False

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)
root.bind("r", reset)
root.bind("<Button-1>", shoot)
root.bind("<Escape>", lambda e: root.destroy())

def game_loop():    
    dx = 0
    dy = 0
    if alive:

        if keys["Left"]:
            dx -= PLAYER_VELO
        elif keys["Right"]:
            dx += PLAYER_VELO
        elif keys["Up"]:
            dy -= PLAYER_VELO
        elif keys["Down"]:
            dy += PLAYER_VELO
        if keys["Left"] and keys["Down"]:
            dx = - math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = math.sqrt(0.5 * (PLAYER_VELO ** 2))
        if keys["Left"] and keys["Up"]:
            dx = - math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = - math.sqrt(0.5 * (PLAYER_VELO ** 2))
        if keys["Right"] and keys["Down"]:
            dx = math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = math.sqrt(0.5 * (PLAYER_VELO ** 2))
        if keys["Right"] and keys["Up"]:
            dx = math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = - math.sqrt(0.5 * (PLAYER_VELO ** 2))

        px1, py1, px2, py2 = canvas.coords(player)

        if 0 <= px1 + dx and px2 + dx <= SCREEN_WIDTH:
            canvas.move(player, dx, 0)

        if 0 <= py1 + dy and py2 + dy <= SCREEN_HEIGHT:
            canvas.move(player, 0, dy)
        
        
        move_enemies()

        for bullet in bullets[:]:
            bullet.move()
            check_delete(bullet)
        
        for bullet in bullets[:]:
            check_hit(bullet)

        
        for enemy in enemies:
            check_collision_player(enemy)
            if health <= 0:
                game_over()
                break

        root.after(16, game_loop)

reset()
game_loop()
make_enemy()
root.mainloop()