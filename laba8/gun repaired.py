from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)
n = int(input())
l0 = 20


class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        if self.x >= 700:
            self.vx *= -1
        if self.y >= 500:
            self.vy *= -0.5
        self.vy += 1
        self.x += self.vx
        self.y += self.vy
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (obj.r) ** 2:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canvas.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.x != 20:

                self.an = math.atan((event.y - 450) / (event.x - 20))
            else:
                if event.y - 450 > 0:
                    self.an = math.pi / 2
                else:
                    self.an = -math.pi / 2

        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.an),
                      450 + max(self.f2_power, 20) * math.sin(self.an)
                      )
        for b in balls:
            b.move()
        for t in targets:
            t.move()
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(500, 600)
        y = self.y = rnd(300, 500)
        r = self.r = rnd(20, 50)
        self.vx = 0
        self.vy = 0
        color = self.color = 'red'
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)

    def set_coords(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):

        self.x += self.vx
        self.y += self.vy
        if self.x >= 700 or self.x <= 0:
            self.vx *= -1
        if self.y >= 500 or self.y <= 0:
            self.vy *= -1
        self.vx += self.acceleration()[0]
        self.vy += self.acceleration()[1]
        if abs(self.vx)>10:
            self.vx -= self.acceleration()[0]
        if abs(self.vy)>10:
            self.vy -= self.acceleration()[1]
        self.set_coords()

    def acceleration(self):
        ax = 0
        ay = 0
        for i in targets:
            if i.x != self.x and i.y != self.y:
                l = ((i.x - self.x) ** 2 + (i.x - self.x) ** 2) ** 0.5
                a = l - l0
                ax = a * self.x / l * 0.0001
                ay = a * self.y / l * 0.0001
        return [ax, ay]

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.delete(self.id)
        self.points += points


glob_points = 0
targets = []

screen1 = canvas.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []
score = canvas.create_text(30,30,text = glob_points,font = '28')

def empty(event):
    pass


def new_game(event=''):
    global gun, t1, screen1, balls, bullet, glob_points, targets
    for i in range(n):
        targets.append(target())
    for i in targets:
        i.new_target()
        i.live = 1
    bullet = 0
    balls = []
    canvas.bind('<Button-1>', g1.fire2_start)
    canvas.bind('<ButtonRelease-1>', g1.fire2_end)
    canvas.bind('<Motion>', g1.targetting)
    canvas.itemconfig(screen1, text='')

    z = 0.03
    all_live = n
    while all_live or balls:
        for b in balls:
            b.move()
        for t in targets:
            t.move()
            for b in balls:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.hit()
                    all_live -= 1
                    glob_points += 1
                    canvas.itemconfig(score, text=glob_points)

            if not all_live:
                canvas.bind('<Button-1>', empty)
                canvas.bind('<ButtonRelease-1>', empty)
                canvas.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        if not all_live:
            for b in balls:
                canvas.delete(b.id)
            targets = []
            balls = []
        canvas.update()
        time.sleep(z)
        g1.targetting()
        g1.power_up()
    root.after(750, new_game)


new_game()

tk.mainloop()
