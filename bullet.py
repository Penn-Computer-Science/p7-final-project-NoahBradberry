class Bullet:
     def __init__(self, canvas, x1, y1, x2, y2, dx, dy):
        self.canvas = canvas
        self.dx = dx
        self.dy = dy

        self.id = canvas.create_oval(x1, y1, x2, y2, fill = "red")

     def move(self):
        self.canvas.move(self.id, self.dx, self.dy)

