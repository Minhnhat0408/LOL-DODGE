import pygame, math, random

pygame.init()


class Bullet:

    def __init__(self, speed, x, y, cur, win):
        self.speed = speed
        self.x = x
        self.y = y
        self.pos = pygame.math.Vector2(x, y)
        self.vector = cur - self.pos
        self.vector.normalize_ip()
        self.vector = self.vector * self.speed
        self.win = win
        self.sur = pygame.draw.circle(win, (0, 120, 0), self.pos, 10)

    def shoot(self):
        self.pos += self.vector
        self.sur = pygame.draw.circle(self.win, (0, 120, 0), self.pos, 10)

    def collide(self, char):
        char_mask = char.get_mask()
        bullet_sur = pygame.Surface((round(self.sur.w), round(self.sur.h)))
        bullet_mask = pygame.mask.from_surface(bullet_sur)
        offset = (round(self.pos[0]) - round(char.pos[0]), round(self.pos[1]) - round(char.pos[1]))
        collided = char_mask.overlap(bullet_mask, offset)

        return collided


class Character:
    def __init__(self, color, speed, win):
        self.speed = speed
        self.color = color
        self.pos = pygame.math.Vector2(200, 200)
        self.target = self.pos
        self.fl_cd = 500
        self.cd_color = (0, 255, 0)
        self.win = win
        self.x = pygame.draw.rect(self.win, self.color, (self.pos[0] - 15, self.pos[1] - 15, 30, 30))

    def move(self):
        moving_path = self.target - self.pos
        moving_length = moving_path.length()
        if moving_length < self.speed:
            self.pos = self.target
        elif moving_length != 0:
            moving_path.normalize_ip()
            moving_path = moving_path * self.speed
            self.pos += moving_path

    def flash(self, cur):
        if self.fl_cd == 500:
            cur = pygame.math.Vector2(cur)
            vector = cur - self.pos
            if vector.length() > 70:
                k = math.sqrt((vector[0] ** 2 + vector[1] ** 2) / (70 ** 2))
                self.pos = vector[0] / k + self.pos[0], vector[1] / k + self.pos[1]
                self.fl_cd = 0
            else:
                self.pos = cur

    def draw(self):
        self.x = pygame.draw.rect(self.win, self.color, (self.pos[0] - 15, self.pos[1] - 15, 30, 30))
        text("F", 35, (255, 255, 255), (10, 10), self.win)
        pygame.draw.rect(self.win, self.cd_color, (40, 10, self.fl_cd // 5, 30))

    def get_mask(self):
        x = pygame.Surface((round(self.x.w), round(self.x.h)))
        return pygame.mask.from_surface(x)


def text(text, size, color, pos, win):
    font = pygame.font.SysFont("comicsans", size, True)
    display = font.render(text, 10, color)
    win.blit(display, pos)


def main():
    pygame.display.set_caption("LOLDODGE")
    win = pygame.display.set_mode((400, 400))
    gamework = True
    color = [255, 0, 0]
    c1 = Character(color, 2.5, win)
    FPS = pygame.time.Clock()
    bullet = []
    score = 0
    count = 1
    flipc = True
    while gamework:
        FPS.tick(60)
        win.fill((0, 0, 0))
        cur = pygame.mouse.get_pos()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                gamework = False
            if pygame.mouse.get_pressed() == (0, 0, 1):
                c1.target = pygame.math.Vector2(cur)
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_f:
                    c1.flash(cur)
        # adding bullet
        if len(bullet) < (count / 1000):
            if flipc:
                bullet.append(Bullet(4.5, random.randint(0, 399), random.choice((0, 399)), c1.pos, win))
            else:
                bullet.append(Bullet(4.5, random.choice((0, 399)), random.randint(0, 399), c1.pos, win))
            flipc = not flipc
        # handling the bulet
        for i in bullet:
            if i.pos[0] < 0 or i.pos[0] > 400 or i.pos[1] < 0 or i.pos[1] > 400:
                bullet.pop(bullet.index(i))
                score += 1
            if i.collide(c1):
                bullet.pop(bullet.index(i))
                color[0] -= 50
            i.shoot()
        if color[0] == 5:
            gamework = False

        # game mode increase
        if count != 5000:
            count += 1

        # flash bar
        if c1.fl_cd < 500:
            c1.fl_cd += 1
            c1.cd_color = (255, 0, 0)
        else:
            c1.cd_color = (0, 255, 0)

        # character move and draw
        c1.move()
        c1.draw()
        text(f"Score :{score}",25,(0,255,0),(315,370),win)
        pygame.display.update()


main()
