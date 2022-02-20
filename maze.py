from pygame import *
  
class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()        
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Enemy(Gamesprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 

win_width = 800
win_height = 500
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption("Maze")
background = transform.scale(
    image.load("smb-1-1.jpg"),
    (win_width, win_height)
)

player = Player('pngwing.com.png', 5, win_height - 80, 4)
monster = Enemy('pngegg.png', win_width - 80, 280, 2)
final = Gamesprite('treasure.png', win_width - 120, win_height - 80, 0)

wall1 = Wall(0, 255, 245, 100, 10, 450, 10)
wall2 = Wall(0, 255, 245, 280, 250, 350, 10)
wall3 = Wall(0, 255, 245, 100, 20, 10, 380)
wall4 = Wall(0, 255, 245, 225, 150, 10, 350)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('muzyika-iz-super-mario-bros-23363.ogg')
mixer.music.play()

money = mixer.Sound('zvuk-vyibivaniya-monetyi-iz-igryi-super-mario-30119.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        monster.update()

    wall1.draw_wall()
    player.reset()
    monster.reset()
    final.reset()

    wall1.draw_wall()
    wall2.draw_wall()
    wall3.draw_wall()
    wall4.draw_wall()
        
    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3):
        finish = True
        window.blit(lose, (200, 200))
        kick.play()
            

    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (200,200))
        money.play()
        

    display.update()
    clock.tick(FPS)