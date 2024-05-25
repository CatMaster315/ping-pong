from random import *
from pygame import *
from random import randint
font.init()
mixer.init()
win = display.set_mode((700,500))
display.set_caption('полетушки')
clock = time.Clock()


color = 135, 146, 250
win.fill(color)
FPS = 60

class gameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image , (self.rect.x, self.rect.y))

class playerSprite(gameSprite):
        def movingP1(self):
            keys_pressed = key.get_pressed()
            if self.rect.y > 0:
                if keys_pressed[K_w]:
                    self.rect.y -= self.speed
            if self.rect.y < 400:
                if keys_pressed[K_s]:
                    self.rect.y += self.speed
        def movingP2(self):
            keys_pressed = key.get_pressed()
            if self.rect.y > 0:
                if keys_pressed[K_UP]:
                    self.rect.y -= self.speed
            if self.rect.y < 400:
                if keys_pressed[K_DOWN]:
                    self.rect.y += self.speed

class ballSprite(gameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, x_speed, y_speed):
        super().__init__(player_image, player_x, player_y, x_speed, player_width, player_height)
        self.speed_x = x_speed
        self.speed_y = y_speed
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
    def hit(self,stick):
        if sprite.collide_rect(self, stick):
            fish = ball_rotate(self, stick)
            if abs(fish) == 40:
                self.speed_x = 5
                self.speed_y = 5
                print(1)
            if abs(fish) == 20:
                self.speed_x = 3
                self.speed_y = 5
                print(2)
            if fish == -40:
                self.speed_x = 5
                self.speed_y = -5
                print(3)
            if fish == -20:
                self.speed_x = 3
                self.speed_y = -5
                print(4)
            if self.rect.x > 350:
                self.speed_x *= -1


def score():
        if ball.rect.x > 800:
            ball.rect.y = 150
            ball.rect.x = 400
            player1.score += 1
            ball.speed_x *= -1
        elif ball.rect.x < -100:
            ball.rect.y = 150
            ball.rect.x = 200
            player2.score += 1
            ball.speed_x *= -1
   


def ball_rotate(balz,stick):
    height = stick.rect.bottom - stick.rect.top
    if balz.rect.y <= stick.rect.y+height*1/4:
        return -40
    elif balz.rect.y <= stick.rect.y+height*2/4:
        return -20
        print(2)    
    elif balz.rect.y <= stick.rect.y+height*3/4:
        return 20
        print(3)
    else:
        return 40
        print(4)


ball = ballSprite('ball.png', 250, 250, 100, 70, 3, 3)
player1 = playerSprite('stek.png', 40, 200, 4, 10, 100)
player2 = playerSprite('stek.png', 650, 200, 4, 10, 100)

player1.score = 0
player2.score = 0

font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 65)

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        win.fill(color)
        sc1 = font1.render('счет игрока 1:   '+ str(player1.score), 1, (0, 0, 255))
        sc2 = font1.render('счет игрока 2:   '+ str(player2.score), 1, (255, 0, 0))
        win.blit(sc1, (10,10))
        win.blit(sc2, (530,10))
        player1.movingP1()
        player2.movingP2()
        ball.update()
        player1.reset()
        player2.reset()
        ball.reset()
        if ball.rect.y > 400 or ball.rect.y < 0:
            ball.speed_y *= -1

        score()
        ball.hit(player2)
        ball.hit(player1)

        if player1.score == 10:
                win1 = font2.render('Игрок 1 выиграл!', 1, (0, 0, 255))
                win.blit(win1, (50,240))
                finish = True 


        if player2.score == 10:
            win2 = font2.render('Игрок 2 выиграл!', 1, (255, 0, 0))
            win.blit(win2, (50,240))
            finish = True 
    clock.tick(FPS)
    display.update()
