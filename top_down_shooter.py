#TODO death animation, enemy types (shoot back, kamikaze), waves, gun upgrades ( spread shot, bigger bullets, piercing bullets, ricochet, slow down, charge shot)

import tkinter as tk
import random
import math

PLAYER_LENGTH = 25
PLAYER_VELO = 5
ENEMY_LENGTH = 25
BULLET_SPEED = 10
MAX_HEALTH = 500

root = tk.Tk()
root.title("Top-Down Shooter")
root.attributes("-fullscreen", True)

SCREEN_WIDTH = root.winfo_screenwidth() #1920
SCREEN_HEIGHT = root.winfo_screenheight() #1080

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

class Bulky_Enemy:
    def __init__(self, canvas, x1, y1, x2, y2, dx, dy):
        self.canvas = canvas
        self.dx = dx
        self.dy = dy

        self.id = canvas.create_oval(x1, y1, x2, y2, fill = "red")


def reset(event = None):
    global player, enemies, bullets, health, alive, health_bar, health_bar_width, score, score_text, enemy_refresh_rate
    enemies = []
    bullets = []
    alive = True
    health = MAX_HEALTH
    canvas.delete("all")
    player = canvas.create_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 + PLAYER_LENGTH, SCREEN_HEIGHT // 2 + PLAYER_LENGTH, fill = "cyan")
    canvas.create_rectangle(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20, fill = "gray")
    health_bar = canvas.create_rectangle(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20, fill = "green")
    health_bar_width = canvas.coords(health_bar)[2] - canvas.coords(health_bar)[0]
    score = 0
    score_text = canvas.create_text(SCREEN_WIDTH - 100, 40, text = f"Score: {score}", fill = "white", font = ("Arial", 30))
    enemy_refresh_rate = 1000

def revive(event = None):
    reset()
    game_loop()
    make_enemy()

def spawn_enemy(color):
    spawn_side = random.randint(1, 4)
    start_x = random.randint(0, SCREEN_WIDTH)
    start_y = random.randint(0, SCREEN_HEIGHT)
    if spawn_side == 1:
        enemy = canvas.create_rectangle(- ENEMY_LENGTH, start_y , 0, start_y + ENEMY_LENGTH, fill = color)
    elif spawn_side == 2:
        enemy = canvas.create_rectangle(start_x, SCREEN_HEIGHT , start_x + ENEMY_LENGTH, SCREEN_HEIGHT + ENEMY_LENGTH, fill = color)
    elif spawn_side == 3:
        enemy = canvas.create_rectangle(SCREEN_WIDTH, start_y, SCREEN_WIDTH + ENEMY_LENGTH, start_y + ENEMY_LENGTH, fill = color)
    elif spawn_side == 4:
        enemy = canvas.create_rectangle(start_x, 0 , start_x + ENEMY_LENGTH, 0 - ENEMY_LENGTH, fill = color)
    return enemy

def normal_enemy():
    color = "purple"
    health = 1
    speed = 3
    enemy = spawn_enemy(color)
    enemies.append({"id": enemy, "health": health, "type": "normal", "speed": speed})

def tank_enemy():
    color = "#7F1D1D"
    health = 3
    speed = 2
    enemy = spawn_enemy(color)
    enemies.append({"id": enemy, "health": health, "type": "tank", "speed": speed})

def speedy_enemy():
    color = "#E0115F"
    health = 1
    speed = 6
    enemy = spawn_enemy(color)
    enemies.append({"id": enemy, "health": health, "type": "speedy", "speed": speed})

def splitter_enemy():
    color = "green"
    health = 2
    speed = 3
    enemy = spawn_enemy(color)
    enemies.append({"id": enemy, "health": health, "type": "splitter", "speed": speed})

def kamikaze_enemy():
    color = "#D0571C"
    health = 1
    speed = 3
    enemy = spawn_enemy(color)
    enemies.append({"id": enemy, "health": health, "type": "kamikaze", "speed": speed})

def make_enemy():
    global enemy_refresh_rate
    enemy_type = random.choice(["normal", "tank", "speedy", "splitter", "kamikaze"])
    if enemy_type == "normal":
        normal_enemy()
    elif enemy_type == "tank":
        tank_enemy()
    elif enemy_type == "speedy":
        speedy_enemy()
    elif enemy_type == "splitter":
        splitter_enemy()
    elif enemy_type == "kamikaze":
        kamikaze_enemy()
    
    enemy_refresh_rate -= 10
    
    root.after(max(enemy_refresh_rate, 100), make_enemy)

def move_enemies():
    px1, py1, px2, py2 = canvas.coords(player)
    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2

    for enemy in enemies[:]:
        coords = canvas.coords(enemy["id"])
        if not coords:
            enemies.remove(enemy)
            continue
        ex1, ey1, ex2, ey2 = canvas.coords(enemy["id"])
        enemy_center_x = (ex2 + ex1) / 2
        enemy_center_y = (ey2 + ey1) / 2

        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            continue  
    
        move_x = (dx / distance) * enemy["speed"]
        move_y = (dy / distance) * enemy["speed"]

        canvas.move(enemy["id"], move_x, move_y)

def shoot(event):
    px1, py1, px2, py2 = canvas.coords(player)
    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2
    mouse_x = event.x
    mouse_y = event.y

    distance_x = player_center_x - mouse_x
    distance_y = player_center_y - mouse_y
    relative_distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    dx = (distance_x / relative_distance) * BULLET_SPEED
    dy = (distance_y / relative_distance) * BULLET_SPEED

    bullets.append(Bullet(canvas, px1 + 5, py1 + 5, px2 - 5, py2 - 5, -dx, -dy))

def check_delete(bullet):
    bx1, by1, bx2, by2 = canvas.coords(bullet.id)
    if bx2 < 0 or bx1 > SCREEN_WIDTH or by1 > SCREEN_HEIGHT or by2 < 0:
        canvas.delete(bullet.id)
        bullets.remove(bullet)

def check_hit(bullet):
    global score
    bbox = canvas.bbox(bullet.id)
    if bbox is None:
        return

    bx1, by1, bx2, by2 = bbox

    for enemy in enemies[:]:
        enemy_bbox = canvas.bbox(enemy["id"])
        if enemy_bbox is None:
            if enemy in enemies:
                enemies.remove(enemy)
                continue

        try: ex1, ey1, ex2, ey2 = enemy_bbox
        except: continue

        if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
            canvas.delete(bullet.id)
            if bullet in bullets:
                bullets.remove(bullet)
            
            enemy["health"] -= 1

            if enemy["type"] == "kamikaze":
                explosion_radius = 500
                explosion = canvas.create_oval(ex1 - explosion_radius, ey1 - explosion_radius, ex2 + explosion_radius, ey2 + explosion_radius, fill = "red")
                x1, y1, x2, y2 = canvas.coords(explosion)
                for other_enemy in enemies[:]:
                    bbox = canvas.bbox(other_enemy["id"])
                    if bbox is None:
                        continue
                    ex1_o, ey1_o, ex2_o, ey2_o = canvas.bbox(other_enemy["id"])
                    if x1 < ex2_o and x2 > ex1_o and y1 < ey2_o and y2 > ey1_o:
                        if other_enemy in enemies:
                            canvas.delete(other_enemy["id"])
                            enemies.remove(other_enemy)
                            score += 1
                            canvas.itemconfig(score_text, text = f"Score: {score}")
                canvas.after(100, lambda: canvas.delete(explosion))
        

            if enemy["health"] == 0:
                canvas.delete(enemy["id"])
                if enemy in enemies:
                    enemies.remove(enemy)
                    score += 1
                    canvas.itemconfig(score_text, text = f"Score: {score}")
                    return
            elif enemy["type"] == "tank":
                if enemy["health"] == 2:
                    canvas.itemconfig(enemy["id"], fill = "#DC2626")
                elif enemy["health"] == 1:
                    canvas.itemconfig(enemy["id"], fill = "#F87171")
            elif enemy["type"] == "splitter" and enemy["health"] == 1:
                canvas.delete(enemy["id"])
                enemies.remove(enemy)
                enemy = canvas.create_rectangle(ex1, ey1, ex1 + ENEMY_LENGTH, ey1 + ENEMY_LENGTH, fill = "green")
                enemies.append({"id": enemy, "health": 1, "type": "splitter", "speed": 3})
                enemy = canvas.create_rectangle(ex1, ey1, ex1 - ENEMY_LENGTH, ey1 - ENEMY_LENGTH, fill = "green")
                enemies.append({"id": enemy, "health": 1, "type": "splitter", "speed": 3})
            
                
        

def check_collision_player(enemy):
    global health_bar, health
    px1, py1, px2, py2 = canvas.coords(player)
    ex1, ey1, ex2, ey2 = canvas.coords(enemy["id"])

    if px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1:
        health -= 1
        x1, y1, x2, y2 = canvas.coords(health_bar)
        new_x2 = x1 + (health / MAX_HEALTH) * health_bar_width
        canvas.coords(health_bar, x1, y1, new_x2, y2)
        new_ex1, new_ey1 = ex1, ey1
        px_center = (px1 + px2) / 2
        py_center = (py1 + py2) / 2
        ex_center = (ex1 + ex2) / 2
        ey_center = (ey1 + ey2) / 2

        dx = ex_center - px_center
        dy = ey_center - py_center

        if abs(dx) > abs(dy):
            new_ex1 += enemy["speed"] if dx > 0 else -enemy["speed"]
        else:
            new_ey1 += enemy["speed"] if dy > 0 else -enemy["speed"]

        canvas.coords(enemy["id"], new_ex1, new_ey1, new_ex1 + ENEMY_LENGTH, new_ey1 + ENEMY_LENGTH)

def game_over():
    global alive
    alive = False
    canvas.delete("all")

    game_over_text = canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text= "Game Over. Press r to Restart", fill = "white", font=("Arial", 12))
    score_text = canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9, text = (f"Score: {score}"), fill = "white", font=("Arial", 12))

keys = {
        "Left": False,
        "Right": False,
        "Up": False,
        "Down": False,
        "w": False,
        "a": False,
        "s": False,
        "d": False

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

        if keys["Left"] or keys["a"]:
            dx -= PLAYER_VELO
        elif keys["Right"] or keys["d"]:
            dx += PLAYER_VELO
        elif keys["Up"] or keys["w"]:
            dy -= PLAYER_VELO
        elif keys["Down"] or keys["s"]:
            dy += PLAYER_VELO
        if keys["Left"] and keys["Down"] or keys["a"] and keys["s"]:
            dx = - math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = math.sqrt(0.5 * (PLAYER_VELO ** 2))
        if keys["Left"] and keys["Up"] or keys["a"] and keys["w"]:
            dx = - math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = - math.sqrt(0.5 * (PLAYER_VELO ** 2))
        if keys["Right"] and keys["Down"] or keys["d"] and keys["s"]:
            dx = math.sqrt(0.5 * (PLAYER_VELO ** 2))
            dy = math.sqrt(0.5 * (PLAYER_VELO ** 2))
        if keys["Right"] and keys["Up"] or keys["d"] and keys["w"]:
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
            if bullet in bullets:
                check_hit(bullet)
            
        for enemy in enemies[:]:
            check_collision_player(enemy)

        
        if health <= 0:
            game_over()
            

        root.after(16, game_loop)

        if alive == True:
            root.bind("r", reset)
        else:
            root.bind("r", revive)

reset()
game_loop()
make_enemy()
root.mainloop()