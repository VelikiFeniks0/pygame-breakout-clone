# importing libraries
import pygame, sys, time, threading

# initialize pygame
pygame.init()


# initialize joystick / controller

try:
    j = pygame.joystick.Joystick(0)
    j.init()
except:
    pass


# setup

width, height = 800, 600

ballbrick = False

ballplayer = False

lives = 5

score_var = 0

font = pygame.font.SysFont('Calibri', 50)
font1 = pygame.font.SysFont('Calibri', 80)
score = font.render(f'{str(score_var)}', True, (255,255,255))


game_over = False




# brick sprite
class Brick(pygame.sprite.Sprite):
    def __init__(self, color: str, position: tuple, ind: int):
        super().__init__()
        self.color = color
        self.ind = ind

        self.image = pygame.Surface((100, 30))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = position
    
    def destroy_self(self):
        global ballbrick
        if pygame.sprite.spritecollide(ball_sprite.sprite, brick_sprite, False):
            try:
                ballbrick = True
                del brick_layers[self.color][self.ind]
                Brick.kill()
            except:
                pass
    
    def update(self):
        self.destroy_self()



# ball sprite
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player = Player()

        self.image = pygame.Surface((15,15))
        self.image.fill('white')
        self.pos = [-230, -200, -100, -50, 50, 100, 200, 230]
        self.ball_x_speed = 4.50
        self.ball_y_speed = 4.50

        self.rect = self.image.get_rect()
        self.rect.center = ((width/2)-self.player.rect.x, (height/2)+200)
        self.rect.x = self.player.rect.x

    
    def move(self):
        global ballbrick, score_var, score, font, lives, ballplayer
        self.rect.x += self.ball_x_speed
        self.rect.y += self.ball_y_speed

        if pygame.sprite.spritecollide(player_sprite.sprite, ball_sprite, False):
            self.ball_x_speed *= 1
            self.ball_y_speed *= -1


        # if ball touches the brick
        if ballbrick:
            self.ball_y_speed *= -1
            self.ball_x_speed *= -1
            time.sleep(0.05)
            score_var += 1
            score = font.render(f'{str(score_var)}', True, (255,255,255))
            dis.blit(score, (20, 20))
            ballbrick = False


        if self.rect.top <= 0:
            self.ball_y_speed *= -1

        if self.rect.bottom >= height:
            lives -= 1
            self.ball_x_speed = 0
            self.ball_y_speed = 0
            time.sleep(1)
            ballplayer = True
            self.rect.center = ((width/2), (height/2)+200)
            self.rect.x = self.player.rect.x
            self.ball_x_speed = 4.50
            self.ball_y_speed = 4.50


        if self.rect.x <= 0 or self.rect.right >= width:
            self.ball_x_speed *= -1
        
    

    def update(self):
        self.move()
        



# player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((100, 10))
        self.image.fill('#477ab5')

        self.rect = self.image.get_rect()
        self.rect.center = (width/2, (height/2)+240)
    

    def user_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= 5
        
        if key[pygame.K_RIGHT]:
            self.rect.x += 5

        try:
            if j.get_button(13): # only for joystick/controller
                self.rect.x -= 5
            
            if j.get_button(14):
                self.rect.x += 5
        except:
            pass
            

    def boundaries(self):
        global ballplayer
        if self.rect.x <= 0:
            self.rect.x = 0
        
        if self.rect.right >= 800:
            self.rect.x = 700

        if ballplayer:
            self.rect.center = (width/2, (height/2)+240)
            ballplayer = False
        

    def update(self):
        self.user_input()
        self.boundaries()





# display
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Breakout')


# clock
clock = pygame.time.Clock()


# ball sprite group
ball_sprite = pygame.sprite.GroupSingle()
ball = Ball()
ball_sprite.add(ball)


# player sprite group
player_sprite = pygame.sprite.GroupSingle()
player = Player()
player_sprite.add(player)


# brick sprite group and coordinates

brick_layers = {
    "red": [(90, 50), (220, 50), (350, 50), (480, 50), (610, 50)],
    "orange": [(90, 90), (220, 90), (350, 90), (480, 90), (610, 90)],
    "green": [(90, 130), (220, 130), (350, 130), (480, 130), (610, 130)],
    "yellow": [(90, 170), (220, 170), (350, 170), (480, 170), (610, 170)],
    "blue": [(90, 210), (220, 210), (350, 210), (480, 210), (610, 210)]
}

brick_sprite = pygame.sprite.GroupSingle()



# draw bricks
def red_bricks():
    for item in brick_layers['red']:
        brick = Brick('red', item, brick_layers['red'].index(item))
        brick_sprite.add(brick)
        brick_sprite.draw(dis)   
        brick.update()      

def orange_bricks():
    for item in brick_layers['orange']:
        brick = Brick('orange', item, brick_layers['orange'].index(item))
        brick_sprite.add(brick)
        brick_sprite.draw(dis)         
        brick.update()

def green_bricks():
    for item in brick_layers['green']:
        brick = Brick('green', item, brick_layers['green'].index(item))
        brick_sprite.add(brick)
        brick_sprite.draw(dis)
        brick.update()   


def yellow_bricks():
    for item in brick_layers['yellow']:
        brick = Brick('yellow', item, brick_layers['yellow'].index(item))
        brick_sprite.add(brick)
        brick_sprite.draw(dis) 
        brick.update()        


def blue_bricks():
    for item in brick_layers['blue']:
        brick = Brick('blue', item, brick_layers['blue'].index(item))
        brick_sprite.add(brick)
        brick_sprite.draw(dis) 
        brick.update()        


# update bricks
def update_bricks():
    red_bricks()
    orange_bricks()
    green_bricks()
    yellow_bricks()
    blue_bricks()


# update player
def update_player():
    player_sprite.draw(dis)
    player.update()





def reset_game():
    global ballbrick, ballplayer, lives, score_var, game_over, score, brick_layers
    ballbrick = False
    ballplayer = True
    ballplayer = False
    lives = 5
    score_var = 0
    game_over = False
    score = font.render(f'{str(score_var)}', True, (255,255,255))
    dis.blit(score, (20,20))
    brick_layers = {
        "red": [(90, 50), (220, 50), (350, 50), (480, 50), (610, 50)],
        "orange": [(90, 90), (220, 90), (350, 90), (480, 90), (610, 90)],
        "green": [(90, 130), (220, 130), (350, 130), (480, 130), (610, 130)],
        "yellow": [(90, 170), (220, 170), (350, 170), (480, 170), (610, 170)],
        "blue": [(90, 210), (220, 210), (350, 210), (480, 210), (610, 210)]
    }



# game
run = True

while run:
    dis.fill((0,0,0))
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
    if lives <= 0:
        game_over = True
    if not game_over and score_var < 25:
        threading.Thread(target=update_bricks).start()
        ball_sprite.draw(dis)
        ball.update()
        threading.Thread(target=update_player).start()
        dis.blit(score, (20,20))
    elif score_var >= 25:
        you_won_text = font1.render('You won!', True, (255,255,255))
        dis.blit(you_won_text, (240, 240))
        if j.get_button(6) or key[pygame.K_ESCAPE]:
            reset_game()
    else:
        game_over_text = font1.render('Game Over', True, (255,255,255))
        dis.blit(game_over_text, (240, 240))
        if j.get_button(6) or key[pygame.K_ESCAPE]:
            reset_game()
    pygame.display.flip()
    clock.tick(60)
    
