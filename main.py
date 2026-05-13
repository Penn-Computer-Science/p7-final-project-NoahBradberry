import tkinter as tk
import random
import math
import time
from bullet import Bullet
from enemy import Enemy, SplitterEnemy, TankEnemy

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

def normal_enemy():
    x, y = random_spawn_position()
    color = "purple"
    health = 1
    speed = 3
    type = "normal"
    enemy = Enemy(canvas, x, y, ENEMY_LENGTH, color, health, speed, type)
    enemies.append(enemy)

def tank_enemy():
    x, y = random_spawn_position()
    enemy = Enemy(canvas, x, y, ENEMY_LENGTH)
    enemies.append(enemy)

def speedy_enemy():
    x, y = random_spawn_position()
    color = "#E0115F"
    health = 1
    speed = 6
    type = "speedy"
    enemy = Enemy(canvas, x, y, ENEMY_LENGTH, color, health, speed, type)
    enemies.append(enemy)

def splitter_enemy():
    x, y = random_spawn_position()
    color = "green"
    health = 2
    speed = 3
    type = "splitter"
    enemy = Enemy(canvas, x, y, ENEMY_LENGTH, color, health, speed, type)
    enemies.append(enemy)

def kamikaze_enemy():
    x, y = random_spawn_position()
    color = "#D0571C"
    health = 1
    speed = 3
    type = "kamikaze"
    enemy = Enemy(canvas, x, y, ENEMY_LENGTH, color, health, speed, type)
    enemies.append(enemy)

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
    if not god:
        root.after(max(enemy_refresh_rate, 500), make_enemy)
    else:
        root.after(1, make_enemy)

def move_enemies():
    px1, py1, px2, py2 = canvas.coords(player)
    player_center_x = (px2 + px1) / 2
    player_center_y = (py2 + py1) / 2

    for enemy in enemies[:]:
        coords = canvas.coords(enemy.id)
        if not coords:
            enemies.remove(enemy)
            continue
        ex1, ey1, ex2, ey2 = canvas.coords(enemy.id)
        enemy_center_x = (ex2 + ex1) / 2
        enemy_center_y = (ey2 + ey1) / 2

        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            continue  
    
        move_x = (dx / distance) * enemy.speed
        move_y = (dy / distance) * enemy.speed

        canvas.move(enemy.id, move_x, move_y)

def shoot(event):
    global bullet_radius
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

    if bigger_bullets:
        bullet_radius = 20
    else:
        bullet_radius = 10

    bullets.append(Bullet(canvas, player_center_x - bullet_radius, player_center_y - bullet_radius, player_center_x + bullet_radius, player_center_y + bullet_radius, -dx, -dy))

    if spread_shot:
        mouse_x += 30
        mouse_y += 30
        distance_x = player_center_x - mouse_x
        distance_y = player_center_y - mouse_y
        relative_distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        dx = (distance_x / relative_distance) * BULLET_SPEED
        dy = (distance_y / relative_distance) * BULLET_SPEED
        bullets.append(Bullet(canvas, player_center_x - bullet_radius, player_center_y - bullet_radius, player_center_x + bullet_radius, player_center_y + bullet_radius, -dx, -dy))

        mouse_x -= 60
        mouse_y -= 60
        distance_x = player_center_x - mouse_x
        distance_y = player_center_y - mouse_y
        relative_distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        dx = (distance_x / relative_distance) * BULLET_SPEED
        dy = (distance_y / relative_distance) * BULLET_SPEED
        bullets.append(Bullet(canvas, player_center_x - bullet_radius, player_center_y - bullet_radius, player_center_x + bullet_radius, player_center_y + bullet_radius, -dx, -dy))

def check_delete(bullet):
    bx1, by1, bx2, by2 = canvas.coords(bullet.id)
    if bx2 < 0 or bx1 > SCREEN_WIDTH or by1 > SCREEN_HEIGHT or by2 < 0:
        canvas.delete(bullet.id)
        bullets.remove(bullet)

def check_hit(bullet):
    global score, health
    bbox = canvas.bbox(bullet.id)
    if bbox is None:
        return

    bx1, by1, bx2, by2 = bbox

    for enemy in enemies[:]:
        enemy_bbox = canvas.bbox(enemy.id)
        if enemy_bbox is None:
            if enemy in enemies:
                enemies.remove(enemy)
                continue

        try: ex1, ey1, ex2, ey2 = enemy_bbox
        except: continue

        if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
            if piercing == False:
                canvas.delete(bullet.id)
                if bullet in bullets:
                    bullets.remove(bullet)
            
            enemy.take_damage(enemies)

            if enemy.type == "kamikaze":
                explosion_radius = 100
                explosion = canvas.create_oval(ex1 - explosion_radius, ey1 - explosion_radius, ex2 + explosion_radius, ey2 + explosion_radius, fill = "red")
                x1, y1, x2, y2 = canvas.coords(explosion)
                px1, py1, px2, py2 = canvas.coords(player)
                for other_enemy in enemies[:]:
                    bbox = canvas.bbox(other_enemy.id)
                    if bbox is None:
                        continue
                    ex1_o, ey1_o, ex2_o, ey2_o = canvas.bbox(other_enemy.id)
                    if x1 < ex2_o and x2 > ex1_o and y1 < ey2_o and y2 > ey1_o:
                        if other_enemy in enemies:
                            canvas.delete(other_enemy.id)
                            enemies.remove(other_enemy)
                            score += 1
                            canvas.itemconfig(score_text, text = f"Score: {score}")
                
                if  x1 < px2 and x2 > px1 and y1 < py2 and y2 > py1:
                    health -= 50
                    x1, y1, x2, y2 = canvas.coords(health_bar)
                    new_x2 = x1 + (health / MAX_HEALTH) * health_bar_width
                    canvas.coords(health_bar, x1, y1, new_x2, y2)
                canvas.after(100, lambda: canvas.delete(explosion))
        

            elif enemy.type == "tank":
                TankEnemy.take_damage(enemy, enemies)
            
            elif enemy.type == "splitter" and enemy.health == 1:
                SplitterEnemy.die(enemy, enemies)
            
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
        
        
        move_enemies()
        move_powerups()

        for bullet in bullets[:]:
            bullet.move()
            check_delete(bullet)
            if bullet in bullets:
                check_hit(bullet)
            
        for enemy in enemies[:]:
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