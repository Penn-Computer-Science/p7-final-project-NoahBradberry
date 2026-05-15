import tkinter as tk
import random
import math
import time
from bullet import Bullet
from enemy import Enemy, NormalEnemy, SplitterEnemy, TankEnemy, SpeedyEnemy, KamikazeEnemy

PLAYER_LENGTH = 25
PLAYER_SPEED = 5
ENEMY_LENGTH = 25
BULLET_SPEED = 10
MAX_HEALTH = 500
POWERUP_RADIUS = 20
POWERUP_SPEED = 3

root = tk.Tk()
root.title("Top-Down Shooter")
root.attributes("-fullscreen", True)

SCREEN_WIDTH = root.winfo_screenwidth() #1920
SCREEN_HEIGHT = root.winfo_screenheight() #1080

canvas = tk.Canvas(root, bg = "black")
canvas.pack(fill=tk.BOTH, expand=True)

display_names = {"spread_shot": "Spread Shot", "bigger_bullets": "Bigger Bullets", "piercing_bullets": "Piercing Bullets"}


def reset(event = None):
    global player, enemies, bullets, health, alive, health_bar, health_bar_width, score, score_text, enemy_refresh_rate, powerup_refresh_rate, powerups, spread_shot, active_powerups, powerups_text, bullet_radius, bigger_bullets, piercing, god
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
    powerup_refresh_rate = 5000
    powerups = []
    spread_shot = False
    bigger_bullets = False
    active_powerups = {"spread_shot": 0, "bigger_bullets": 0, "piercing_bullets": 0}
    powerups_text = canvas.create_text(10, 40, text = "", fill = "white", font = ("Arial", 20), anchor = "w")
    bullet_radius = 5
    piercing = False
    god = False

def revive(event = None):
    reset()
    game_loop()
    make_enemy()

def random_spawn_position():
    side = random.randint(1, 4)
    if side == 1:
        return -ENEMY_LENGTH, random.randint(0, SCREEN_HEIGHT)
    elif side == 2:
        return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
    elif side == 3:
        return SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
    else:
        return random.randint(0, SCREEN_WIDTH), -ENEMY_LENGTH

def make_enemy():
    global enemy_refresh_rate
    enemy_class = random.choice([NormalEnemy, TankEnemy, SpeedyEnemy, SplitterEnemy, KamikazeEnemy])
    x,y = random_spawn_position()
    enemy = enemy_class(canvas, x, y, ENEMY_LENGTH)
    enemies.append(enemy)
    enemy_refresh_rate -= 10
    if not god:
        root.after(max(enemy_refresh_rate, 500), make_enemy)
    else:
        root.after(1, make_enemy)

def move_enemies():
    px1, py1, px2, py2 = canvas.coords(player)

    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2

    for enemy in enemies[:]:
        if not canvas.coords[enemy.id]:
            if enemy in enemies:
                enemies.remove(enemy)
                continue
            enemy.move_towards_player(player_center_x, player_center_y)

def damage_player(amount):
    global health
    health -= amount

    x1, y1, x2, y2 = canvas.coords(health_bar)
    new_x2 = x1 + (health / MAX_HEALTH) * health_bar_width

    canvas.coords(health_bar, x1, y1, new_x2, y2)

def shoot(event):
    global bullet_radius
    px1, py1, px2, py2 = canvas.coords(player)
    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2
    mouse_x = event.x
    mouse_y = event.y

    if bigger_bullets:
        bullet_radius = 20
    else:
        bullet_radius = 10

    bullets.append(Bullet(canvas, player_center_x - bullet_radius, player_center_y - bullet_radius, player_center_x + bullet_radius, player_center_y + bullet_radius, player_center_x, player_center_y, mouse_x, mouse_y))

    if spread_shot:
        mouse_x += 30
        mouse_y += 30
        bullets.append(Bullet(canvas, player_center_x - bullet_radius, player_center_y - bullet_radius, player_center_x + bullet_radius, player_center_y + bullet_radius, player_center_x, player_center_y, mouse_x, mouse_y))

        mouse_x -= 60
        mouse_y -= 60
        bullets.append(Bullet(canvas, player_center_x - bullet_radius, player_center_y - bullet_radius, player_center_x + bullet_radius, player_center_y + bullet_radius, player_center_x, player_center_y, mouse_x, mouse_y))


            
def check_collision_player_enemy(enemy):
    global health_bar, health
    px1, py1, px2, py2 = canvas.coords(player)
    ex1, ey1, ex2, ey2 = canvas.coords(enemy.id)

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
            new_ex1 += enemy.speed if dx > 0 else -enemy.speed
        else:
            new_ey1 += enemy.speed if dy > 0 else -enemy.speed

        canvas.coords(enemy.id, new_ex1, new_ey1, new_ex1 + ENEMY_LENGTH, new_ey1 + ENEMY_LENGTH)

def spawn_powerup(color, type):
    spawn_side = random.randint(1, 4)
    start_x = random.randint(0, SCREEN_WIDTH)
    start_y = random.randint(0, SCREEN_HEIGHT)
    target_x = random.randint(0, SCREEN_WIDTH)
    target_y = random.randint(0, SCREEN_HEIGHT)
    if spawn_side == 1:
        id = canvas.create_oval(- POWERUP_RADIUS, start_y , 0, start_y + POWERUP_RADIUS, fill = color)
    elif spawn_side == 2:
        id = canvas.create_oval(start_x, SCREEN_HEIGHT , start_x + POWERUP_RADIUS, SCREEN_HEIGHT + POWERUP_RADIUS, fill = color)
    elif spawn_side == 3:
        id = canvas.create_oval(SCREEN_WIDTH, start_y, SCREEN_WIDTH + POWERUP_RADIUS, start_y + POWERUP_RADIUS, fill = color)
    elif spawn_side == 4:
        id = canvas.create_oval(start_x, 0 , start_x + POWERUP_RADIUS, 0 - POWERUP_RADIUS, fill = color)
    return { "id": id, "target_x": target_x, "target_y": target_y, "type": type}

def make_powerup():
    global powerup_refresh_rate
    if not god:
        powerup_type = random.choice(["spread_shot", "health", "bigger_bullets", "piercing_bullets"])
        if powerup_type == "spread_shot":
            powerup = spawn_powerup("#F97316", powerup_type)
            powerups.append(powerup)
        elif powerup_type == "health":
            powerup = spawn_powerup("#32CD32", powerup_type)
            powerups.append(powerup)
        elif powerup_type == "bigger_bullets":
            powerup = spawn_powerup("#DC2626", powerup_type)
            powerups.append(powerup)
        elif powerup_type == "piercing_bullets":
            powerup = spawn_powerup("#7E22CE", powerup_type)
            powerups.append(powerup)

        powerup_refresh_rate -= 10
        root.after(max(powerup_refresh_rate, 100), make_powerup)

def move_powerups():
    for powerup in powerups:
        try: x1, y1, x2, y2 = canvas.coords(powerup["id"])
        except: powerups.remove(powerup)

        center_x = (x2 + x1) / 2
        center_y = (y2 + y1) / 2

        dx = powerup["target_x"] - center_x
        dy = powerup["target_y"] - center_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance < 2:
            powerup["target_x"] = random.randint(0, SCREEN_WIDTH)
            powerup["target_y"] = random.randint(0, SCREEN_HEIGHT)

        move_x = (dx / distance) * POWERUP_SPEED
        move_y = (dy / distance) * POWERUP_SPEED

        canvas.move(powerup["id"], move_x, move_y)

def check_colision_player_powerup(powerup):
    global spread_shot, active_powerups, health, bullet_radius, bigger_bullets, piercing
    plx1, ply1, plx2, ply2 = canvas.coords(player)
    pox1, poy1, pox2, poy2 = canvas.coords(powerup["id"])

    if plx1 < pox2 and plx2 > pox1 and ply1 < poy2 and ply2 > poy1:
        if powerup["type"] == "spread_shot":
            spread_shot = True
            active_powerups["spread_shot"] = time.time() + 5
        elif powerup["type"] == "health":
            if health + 50 > 500:
                health = 500
            else:
                health += 50
            x1, y1, x2, y2 = canvas.coords(health_bar)
            new_x2 = x1 + (health / MAX_HEALTH) * health_bar_width
            canvas.coords(health_bar, x1, y1, new_x2, y2)
        elif powerup["type"] == "bigger_bullets":
            bigger_bullets = True
            active_powerups["bigger_bullets"] = time.time() + 5
        elif powerup["type"] == "piercing_bullets":
            piercing = True
            active_powerups["piercing_bullets"] = time.time() + 5

        canvas.delete(powerup["id"])
        if powerup in powerups:
            powerups.remove(powerup)

def game_over():
    global alive
    alive = False
    canvas.delete("all")

    game_over_text = canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text= "Game Over. Press r to Restart", fill = "white", font=("Arial", 12))
    score_text = canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9, text = (f"Score: {score}"), fill = "white", font=("Arial", 12))

def god_mode(event):
    global health, bigger_bullets, piercing, spread_shot, powerup_refresh_rate, god, MAX_HEALTH
    god = True
    MAX_HEALTH = 2147483647
    health = 2147483647
    for powerup in powerups:
        canvas.delete(powerup["id"])
        powerups.remove(powerup)
    bigger_bullets = True
    piercing = True
    spread_shot = True
    god_text = canvas.create_text(80, 40, text = "God Mode", font = ("Arial", 24), fill = "white")

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
root.bind("g", god_mode)

def game_loop():
    global spread_shot, bigger_bullets, piercing
    dx = 0
    dy = 0

    if alive:

        if keys["Left"] or keys["a"]:
            dx -= PLAYER_SPEED
        elif keys["Right"] or keys["d"]:
            dx += PLAYER_SPEED
        elif keys["Up"] or keys["w"]:
            dy -= PLAYER_SPEED
        elif keys["Down"] or keys["s"]:
            dy += PLAYER_SPEED
        if keys["Left"] and keys["Down"] or keys["a"] and keys["s"]:
            dx = - math.sqrt(0.5 * (PLAYER_SPEED ** 2))
            dy = math.sqrt(0.5 * (PLAYER_SPEED ** 2))
        if keys["Left"] and keys["Up"] or keys["a"] and keys["w"]:
            dx = - math.sqrt(0.5 * (PLAYER_SPEED ** 2))
            dy = - math.sqrt(0.5 * (PLAYER_SPEED ** 2))
        if keys["Right"] and keys["Down"] or keys["d"] and keys["s"]:
            dx = math.sqrt(0.5 * (PLAYER_SPEED ** 2))
            dy = math.sqrt(0.5 * (PLAYER_SPEED ** 2))
        if keys["Right"] and keys["Up"] or keys["d"] and keys["w"]:
            dx = math.sqrt(0.5 * (PLAYER_SPEED ** 2))
            dy = - math.sqrt(0.5 * (PLAYER_SPEED ** 2))

        px1, py1, px2, py2 = canvas.coords(player)

        if 0 <= px1 + dx and px2 + dx <= SCREEN_WIDTH:
            canvas.move(player, dx, 0)

        if 0 <= py1 + dy and py2 + dy <= SCREEN_HEIGHT:
            canvas.move(player, 0, dy)
        
        move_powerups()

        for bullet in bullets[:]:
            x = root.winfo_pointerx()
            y = root.winfo_pointery()
            bullet.move(player, x, y)
            bullet.check_delete(SCREEN_WIDTH, SCREEN_HEIGHT, bullets)
            if bullet in bullets:
                bullet.check_hit(enemies, score, piercing, bullets, player, damage_player, score_text)
            
        for enemy in enemies[:]:
            enemy.move_towards_player(px1, py1)
            check_collision_player_enemy(enemy)

        for powerup in powerups[:]:
            check_colision_player_powerup(powerup)
        
        if spread_shot and time.time() > active_powerups["spread_shot"] and not god:
            spread_shot = False
        
        if bigger_bullets and time.time() > active_powerups["bigger_bullets"] and not god:
            bigger_bullets = False

        if piercing and time.time() > active_powerups["piercing_bullets"] and not god:
            piercing = False
        
        powerup_lines = []
        
        for powerup in active_powerups:
            time_left = active_powerups[powerup] - time.time()

            if time_left > 0:
                powerup_lines.append(f"{display_names[powerup]}: {round(time_left, 1)}s")

            canvas.itemconfig(powerups_text, text = "\n".join(powerup_lines))

        if health <= 0:
            game_over()

        if alive == True:
            root.bind("r", reset)
        else:
            root.bind("r", revive)

        root.after(16, game_loop)

reset()
game_loop()
make_enemy()
make_powerup()
root.mainloop()