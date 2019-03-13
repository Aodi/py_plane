import pygame
from pygame.locals import *
import random
import start_and_end

#处理文件路径
from pathlib import Path
image_path = Path('/sound/')


enemy_bullet_list = []
hero_bullet_list = []
enemy_plane_list = []
ENEMY_APPEAR = pygame.USEREVENT + 1


def play():
    # pygame.init()
    start_and_end.start_and_end.start()
    window = pygame.display.set_mode((480, 640))
    background = pygame.image.load(r".\images\background.png")
    window.blit(background, (0, 0))

    # plane = pygame.image.load(r".\images\hero1.png")
    plane1 = HeroPlane(window)
    # plane2 = Plane(window, 1)
    bullets = []

    pygame.time.set_timer(ENEMY_APPEAR, random.randint(100, 3000))
    # x = 190
    # y = 516
    while True:

        window.blit(background, (0, 0))
        # window.blit(plane.image, (plane.x, plane.y))
        hero_crush(plane1)
        enemy_crush()

        plane1.display()
        # plane2.display()
        EnemyPlane.enemies_display()
        Bullet.bullets_display()

        # 判断是否是点击了退出按钮
        for event in pygame.event.get():
            # print(event.type)
            if event.type == QUIT:
                print("exit")
                exit()
            if event.type == ENEMY_APPEAR:
                EnemyPlane.count -= 1
                if EnemyPlane.count > 0:
                    pygame.time.set_timer(ENEMY_APPEAR, random.randint(100, 1000))
                else:
                    pygame.time.set_timer(ENEMY_APPEAR, 300000)
                # print("enemy appear")
                enemy_plane_list.append(EnemyPlane(window))

        key_control(plane1)
        # key_control(plane2)
        EnemyPlane.enemies_move()
        Bullet.bullets_move()
        # plane2.bullets_move()

        score(window, plane1)

        result = judge_win_or_lose(plane1)
        if result is not None:
            break

        pygame.display.update()

        pygame.time.Clock().tick(60)

    start_and_end.start_and_end.end(window,result, EnemyPlane.crushed)


class GameObj(object):
    x = 0
    y = 0
    pace = 0
    image = ''


class Plane(GameObj):
    health = 10

    def display(self):
        pass


class HeroPlane(GameObj):
    shoot_int = 2

    def __init__(self, win, pnum=0):
        self.x = 480 // 2 - 100
        self.y = 640 - 124
        self.pace = 9
        self.image = pygame.image.load(r".\images\hero1.png")
        self.window = win

        self.player_num = pnum  # player number

        self.bulpre = 0     # shoot preparation

        self.blowIndex = 0   # blow image index

        self.bullet_image_name = r".\images\bullet.png"

        self.crushed_image = [self.image,
                              pygame.image.load(r".\images\hero_blowup_n3.png"),
                              pygame.image.load(r".\images\hero_blowup_n2.png"),
                              pygame.image.load(r".\images\hero_blowup_n1.png")]
                           

        # 击中事宜
        self.health = 10
        self.crushed = 0

    def move_left(self):
        if self.x > -50 + self.pace:
            self.x -= self.pace
        else:
            self.x = -50

    def move_right(self):
        if self.x < 480 - 50 - self.pace:
            self.x += self.pace
        else:
            self.x = 480 - 50

    def move_up(self):
        if self.y > self.pace:
            self.y -= self.pace
        else:
            self.y = 0

    def move_down(self):
        if self.y < 640 - 3 - self.pace:
            self.y += self.pace
        else:
            self.y = 640 - 3

    def display(self):
        # 将图片进行加载
        self.window.blit(self.crushed_image[self.blowIndex], (self.x, self.y))

        if self.blowIndex > 0:
            self.blowIndex -= 1

        if self.bulpre > 0:
            self.bulpre -= 1

    keyboard = ({"up": K_w, "left": K_a, "down": K_s, "right": K_d, "shoot": K_j},
                {"up": K_UP, "left": K_LEFT, "down": K_DOWN, "right": K_RIGHT, "shoot": K_SPACE})

    def shoot(self):
        if self.bulpre == 0:
            hero_bullet_list.append(Bullet(self.x+39, self.y, -10, self.window, self.bullet_image_name))
            self.bulpre = self.shoot_int+1
        # self.bullets.append(SelfBullet(self.x + 17, self.y+10, -10, self.window))
        # self.bullets.append(SelfBullet(self.x + 61, self.y+10, -10, self.window))

    def get_hit(self):
        self.health -= 1
        self.blowIndex = 3


class EnemyPlane(Plane):
    shoot_int = 5
    count = 40
    crushed = 0
    finished = 0

    def __init__(self, screen):
        # 设置飞机默认的位置
        self.x = random.randint(-10, 480-40)
        self.y = -10

        # move speed
        self.pace = 3

        # 设置要显示内容的窗口
        self.screen = screen

        self.imageName = r".\images\enemy0.png"
        self.image = pygame.image.load(self.imageName)
        self.bullet_image_name = r".\images\bullet1.png"

        # 子弹发射间隔控制
        self.bulpre = 0

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        # if self.bulpre == 0:
        self.shoot()
        #     self.bulpre = self.shoot_int + 1
        # if self.bulpre > 0:
        #     self.bulpre -= 1

    def shoot(self):
        num = random.randint(1, 50)
        if num > 48:
            # print("发射子弹！")
            newBullet = Bullet(self.x+21, self.y+39, 8, self.screen,
                               self.bullet_image_name)
            enemy_bullet_list.append(newBullet)

    def move(self):
        self.y += self.pace
        if self.y > 640:
            return 0
        else:
            return 1

    @staticmethod
    def enemies_move():
        i = 0
        while i < len(enemy_plane_list):
            if enemy_plane_list[i].move() == 0:
                del enemy_plane_list[i]
                EnemyPlane.finished += 1
                i -= 1
            i += 1

    @staticmethod
    def enemies_display():
        for ene in enemy_plane_list:
            ene.display()


class Bullet(GameObj):
    speed = -10
    image = ""

    def __init__(self, x, y, speed, window, image_name):
        self.x = x
        self.y = y
        self.speed = speed
        self.window = window
        self.image = pygame.image.load(image_name)

    def move(self):
        if self.y < -abs(self.speed) or self.y > 640 + abs(self.speed):
            return 0
        else:
            self.y += self.speed
            return 1

    def display(self):
        self.window.blit(self.image, (self.x, self.y))

    @staticmethod
    def bullets_move():
        i = 0
        while i < len(hero_bullet_list):
            if hero_bullet_list[i].move() == 0:
                del hero_bullet_list[i]
                i -= 1
            i += 1

        i = 0
        while i < len(enemy_bullet_list):
            if enemy_bullet_list[i].move() == 0:
                del enemy_bullet_list[i]
                i -= 1
            i += 1

    @staticmethod
    def bullets_display():
        for bul in hero_bullet_list:
            bul.display()
        for bul in enemy_bullet_list:
            bul.display()


def key_control(heroPlane):

    keys = heroPlane.keyboard[heroPlane.player_num]
    key_pressed = pygame.key.get_pressed()
    if key_pressed[keys["up"]]:
        heroPlane.move_up()
    if key_pressed[keys["down"]]:
        heroPlane.move_down()
    if key_pressed[keys["left"]]:
        heroPlane.move_left()
    if key_pressed[keys["right"]]:
        heroPlane.move_right()
    if key_pressed[keys["shoot"]]:
        heroPlane.shoot()
        print(EnemyPlane.finished)
        # heroPlane.sheBullet()


def hero_crush(heroPlane):
    num = 0
    for i in enemy_bullet_list:
        if abs(i.x - heroPlane.x - 50) + abs(i.y - heroPlane.y - 20) <= 50:
            #被击中
            heroPlane.get_hit()
            # heroPlane.crushed = 1
            break
        num += 1
    if num != len(enemy_bullet_list):
        del (enemy_bullet_list[num])
            #子弹销毁

    num = 0
    for i in enemy_plane_list:
        if abs(i.x - heroPlane.x - 50) + abs(i.y - heroPlane.y - 20) <= 50:
            # 被击中
            # heroPlane.crushed = 1
            heroPlane.get_hit()
            break
        num += 1
    if num != len(enemy_plane_list):
        EnemyPlane.finished += 1
        EnemyPlane.crushed += 1
        del (enemy_plane_list[num])

    return True


def enemy_crush():
    num = 0
    for i in enemy_plane_list:
        num_j = 0
        for j in hero_bullet_list:
            if abs(i.x - j.x + 25) + abs(i.y - j.y + 20) <= 30:
                EnemyPlane.finished += 1
                EnemyPlane.crushed += 1
                break
            num_j += 1
        if num_j != len(hero_bullet_list):
            del enemy_plane_list[num]
            del hero_bullet_list[num_j]

        num += 1
    return False


def score(screen, hero_plane):
    """绘制每个飞机的血量信息"""

    # 绘制玩家飞机血量
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render("Health:"+str(hero_plane.health), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # 绘制玩家得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render("Score{0}:".format(1)+str(EnemyPlane.crushed), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 50]
    screen.blit(score_text, text_rect)

    # # 绘制敌机飞机血量
    # score_font = pygame.font.Font(None, 36)
    # score_text = score_font.render(str(enemy_plane.blood), True, (128, 128, 128))
    # text_rect = score_text.get_rect()
    # text_rect.topleft = [10, 50]
    # screen.blit(score_text, text_rect)


def judge_win_or_lose(hero_plane):
    """用来完成输赢的判断"""

    if hero_plane.health <= 0:
        return "lose"
    elif EnemyPlane.finished >= 40:
        return "win"


if __name__ == "__main__":
    play()

