import pygame
import sys
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50,90))
        self.color = (color)
        pygame.draw.rect(self.image,self.color,(0,0,50,90))
        self.rect = self.image.get_rect(center = (x,y))
        self.jumpcount = 0
    def gravity(self):
        self.rect.centery += 2
    def jump(self):
        if self.jumpcount < 10:
            self.rect.centery -= 10
            self.jumpcount += 1
    def move(self, deltax, deltay):
        if self.rect.left < 0 or self.rect.right > 1200:
            deltax *= -1
        if self.rect.top < 0 or self.rect.bottom > 600:
            deltay *= -1
        self.rect.centerx += deltax
        self.rect.centery += deltay

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color, hspeed, vspeed, range):
        super().__init__()
        self.image = pygame.Surface((75,25))
        self.color = (color)
        pygame.draw.rect(self.image,self.color,(0,0,75,25))
        self.rect = self.image.get_rect(center = (x,y))
        self.deltax = hspeed
        self.deltay = vspeed
        self.range = range
    def move(self):
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay
        if self.rect.left < self.range[0] or self.rect.right > self.range[1]:
            self.deltax*=-1
        if self.rect.top < self.range[0] or self.rect.bottom > self.range[1]:
            self.deltay*=-1
    def win(self):
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        # apply it to text on a label
        label = myfont.render("You WIN!", 1, (255,255,255))
        # put the label object on the screen at point x=100, y=100
        screen.blit(label, (100, 100))
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,range,yrange):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.color = ((255,200,0))
        pygame.draw.rect(self.image,self.color,(0,0,50,90))
        self.rect = self.image.get_rect(center = (x,y))
        self.deltax = hspeed
        self.deltay = vspeed
        self.range = range
        self.yrange = yrange
    def move(self):
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay
        if self.rect.left < self.range[0] or self.rect.right > self.range[1]:
            self.deltax*=-1
        if self.rect.top > self.yrange[0] or self.rect.bottom < self.yrange[1]:
            self.deltay*=-1

def red_wins():
    # pick a font you have and set its size
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    # apply it to text on a label
    label = myfont.render("Red WINS!", 1, (255,255,255))
    # put the label object on the screen at point x=100, y=100
    return label
    
def blue_wins():
    # pick a font you have and set its size
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    # apply it to text on a label
    label = myfont.render("Blue WINS!", 1, (255,255,255))
    # put the label object on the screen at point x=100, y=100
    return label

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

# Create clock to later control frame rate
clock = pygame.time.Clock()

# Add player
player = Player(430,300, (255,0,0))
player2 = Player(370,300, (0,0,255))

# Add platforms
platforms = pygame.sprite.Group()
platform1=Platform(200,500, (255,255,255), 1, 0, (50,300))
platforms.add(platform1)
platform2 = Platform(600,500, (255,255,255),1,0,(450,750))
platforms.add(platform2)
platforms.add(Platform(400,450, (255,255,255),0,0,0))

# Winning platform
platformws = pygame.sprite.Group()
platformw = Platform(75,350, (255,0,0),0,0,0)
platformws.add(platformw)
platformwb = Platform(725,350, (0,0,255),0,0,0)
platformws.add(platformwb)
platforms.add(platformws)
# Add Enemy
enemies = pygame.sprite.Group()
enemy = Enemy(200,400,2,1,(100,300),(100,300))
enemies.add(enemy)
enemy2 = Enemy(600,400,2,1,(500,700),(100,300))
enemies.add(enemy2)
# Create a list of sprites and add stuff
allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(player2)
allsprites.add(platforms)
allsprites.add(enemies)
allsprites.add(platformws)
blue = pygame.sprite.Group()
blue.add(platformwb)
red = pygame.sprite.Group()
red.add(platformw)

# Game loop
death = False
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill((0,0,0))

    # Gravity
    collide = pygame.sprite.spritecollide(player, platforms, False)
    if not collide:
        player.gravity()
    if collide:
        player.jumpcount=0

    collide2 = pygame.sprite.spritecollide(player2, platforms, False)
    if not collide2:
        player2.gravity()
    if collide2:
        player2.jumpcount=0
    
    # Lose
    die = pygame.sprite.spritecollide(player, enemies, False)
    if die:
        player.kill()
        label = blue_wins()
        death = True
    die2 = pygame.sprite.spritecollide(player2, enemies, False)
    if die2:
        label = red_wins()
        player2.kill()
        death = True
    rb = pygame.sprite.spritecollide(player,blue,False) 
    if rb:
        pygame.quit()
        sys.exit()
    br = pygame.sprite.spritecollide(player2,red,False) 
    if br:
        pygame.quit()
        sys.exit()
    # Win
    win = pygame.sprite.spritecollide(player, red, False)
    if win:
        red_wins()
    win2 = pygame.sprite.spritecollide(player2, blue, False)
    if win2:
        blue_wins()

    if death:
        screen.blit(label, (0,0))

    # Draw All Sprites
    allsprites.draw(screen)
    platform1.move()
    platform2.move()
    enemy.move()
    enemy2.move()
    
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)
    
    # Check for keypresses
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player.jump()
    if keys[pygame.K_DOWN]:
        player.move(0,2)
    if keys[pygame.K_LEFT]:
        player.move(-2,0)
    if keys[pygame.K_RIGHT]:
        player.move(2,0)
    if keys[pygame.K_w]:
        player2.jump()
    if keys[pygame.K_s]:
        player2.move(0,2)
    if keys[pygame.K_a]:
        player2.move(-2,0)
    if keys[pygame.K_d]:
        player2.move(2,0)

# Quit Pygame properly
pygame.quit()
sys.exit()