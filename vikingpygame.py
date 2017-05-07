import pygame, os
print (os.getcwd())
pygame.init()

class Player:
    #classe para Player
    def __init__(self,x,y,sprite,speed_):
        self.x=x
        self.y=y
        self.sprite=pygame.image.load(sprite)
        self.rect=pygame.Surface.get_size(self.sprite)
        self.speed_x = 0
        self.speed_y = 0
        self.aceleration = + 0.2
        self.walkR=False
        self.walkL=False
    def move(self,direction):

        if direction == "left":
            self.speed_x = -10
        if direction == 0:
            self.speed_x = 0
        if direction == "up":
            self.speed_y = -10 + self.aceleration

    def updatepos(self):
        self.speed_y+=self.aceleration

        if self.y >400:
            self.speed_y = 0
            global jump
            jump=0
            self.y=399
        self.y += self.speed_y

        if self.walkR == True:
            self.x += 10

        if self.walkL == True:
            if self.x > 0:
                self.x -= 10










clock=pygame.time.Clock()

player1="Images\\stand.png"
screen=pygame.display.set_mode((1440,720))
background = pygame.image.load("8bitvapor.png")
background = pygame.transform.scale(background, (1440, 720))

background = background.convert()
#ground= pygame.image.load("ground.png")
#ground= pygame.transform.scale(ground,(100,100))
#x,y=pygame.Surface.get_size(ground)
jump=0
#backcoli = pygame.Surface.get_clip(ground)
#background.fill((250, 250, 250))
char1=Player(400,400,player1,10)
pwalkright0=pygame.image.load("Images\\walk right\\sprite_walkR0.png")
pwalkright0 = pygame.transform.scale(pwalkright0, (char1.rect))
pwalkright1=pygame.image.load("Images\\walk right\\sprite_walkR1.png")
pwalkright1 = pygame.transform.scale(pwalkright1, (char1.rect))
pwalkright2=pygame.image.load("Images\\walk right\\sprite_walkR2.png")
pwalkright2 = pygame.transform.scale(pwalkright2, (char1.rect))
pwalkright3=pygame.image.load("Images\\walk right\\sprite_walkR3.png")
pwalkright3 = pygame.transform.scale(pwalkright3, (char1.rect))




pygame.display.set_caption("RONALDO")
izi=True
while izi:
    screen.blit(background, (0, 0))
    screen.blit(char1.sprite,(char1.x,char1.y))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            izi=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                izi = False
            if event.key == pygame.K_UP and jump==0:
                jump=1
                char1.move("up")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                char1.move(0)
            if event.key == pygame.K_LEFT:
                char1.move(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            char1.walkR=True
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            char1.walkR=False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            char1.walkL=True
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            char1.walkL=False



    #jump=0

    char1.updatepos()
    screen.blit(char1.sprite,(char1.x,char1.y))
    clock.tick(60)
pygame.quit()
quit()
