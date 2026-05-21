import math
BULLET_SPEED = 10

class Bullet:
   def __init__(self, canvas, x1, y1, x2, y2, player_center_x, player_center_y, mouse_x, mouse_y):
      self.canvas = canvas
      self.id = canvas.create_oval(x1, y1, x2, y2, fill = "red")

      distance_x = player_center_x - mouse_x
      distance_y = player_center_y - mouse_y

      relative_distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

      self.dx = (distance_x / relative_distance) * BULLET_SPEED
      self.dy = (distance_y / relative_distance) * BULLET_SPEED

   def move(self, player, mouse_x, mouse_y):
      self.canvas.move(self.id, -self.dx, -self.dy)

   def check_delete(self, SCREEN_WIDTH, SCREEN_HEIGHT, bullets):
      bx1, by1, bx2, by2 = self.canvas.coords(self.id)
      if bx2 < 0 or bx1 > SCREEN_WIDTH or by1 > SCREEN_HEIGHT or by2 < 0:
         self.canvas.delete(self.id)
         bullets.remove(self)
   
   def check_hit(self, enemies, piercing, bullets, player, damage_player):
      bbox = self.canvas.bbox(self.id)
      if bbox is None:
        return

      bx1, by1, bx2, by2 = bbox

      for enemy in enemies[:]:
        enemy_bbox = self.canvas.bbox(enemy.id)
        if enemy_bbox is None:
            if enemy in enemies:
                enemies.remove(enemy)
                continue

        try: ex1, ey1, ex2, ey2 = enemy_bbox
        except: continue
        

        if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
            if piercing == False:
                self.canvas.delete(self.id)
                if self in bullets:
                    bullets.remove(self)
            
            old_enemy_count = len(enemies)
            
            enemy.take_damage(enemies, player, damage_player)

      

