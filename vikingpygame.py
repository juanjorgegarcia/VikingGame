import pygame, os
print (os.getcwd())
pygame.init()

class Player:
    #classe para Player
    def __init__(self,x,y,sprite,speed_):
        self.x = x
        self.y = y
        self.sprite=pygame.image.load(sprite)

        self.speed_x = 0
        self.speed_y = 0
        self.aceleration = + 0.2
        self.walkR = False
        self.walkL = False
        self.current_img = pygame.image.load(sprite)
        self.rect=pygame.Surface.get_size(self.current_img)
    def move(self,direction):

        if direction == "left":
            self.speed_x = 10
            char1.walkL=True
        if direction == "right":
            self.speed_x = 10
            char1.walkR=True
        if direction == 0:
            self.speed_x = 0
        if direction == "up":
            self.speed_y = -10 + self.aceleration
            global jump
            jump=1

    def updatepos(self):
        self.speed_y+=self.aceleration

        if self.y >400:
            self.speed_y = 0
            global jump
            jump=0
            self.y=399
        self.y += self.speed_y

        if self.walkR == True:
            self.x += self.speed_x


        if self.walkL == True:
            if self.x > 0:
                self.x -= self.speed_x




clock=pygame.time.Clock()

player1="Images\\stand.png"
screen=pygame.display.set_mode((1280,720))

###### carregando o background Do jogo
background = pygame.image.load("8bitvapor.png") #dando load
background = pygame.transform.scale(background, (1280, 720))  #escalano conforme a tela
background = background.convert() #covertenod os pixels da imagem (a imagem é carregada mais rapidamete)
#%######%##
jump=0
###%######## carregando as sprites do player
char1=Player(400,400,player1,10)
pwalkright0=pygame.image.load("Images\\walk right\\sprite_walkR0.png")#dando load
pwalkright0 = pygame.transform.scale(pwalkright0, (char1.rect))#escalano conforme o tamanho personagem
pwalkright1=pygame.image.load("Images\\walk right\\sprite_walkR1.png")#dando load
pwalkright1 = pygame.transform.scale(pwalkright1, (char1.rect))#escalano conforme o tamanho personagem
pwalkright2=pygame.image.load("Images\\walk right\\sprite_walkR2.png")#dando load
pwalkright2 = pygame.transform.scale(pwalkright2, (char1.rect))#escalano conforme o tamanho personagem
pwalkright3=pygame.image.load("Images\\walk right\\sprite_walkR3.png")#dando load
pwalkright3 = pygame.transform.scale(pwalkright3, (char1.rect))#escalano conforme o tamanho personagem




pygame.display.set_caption("A Tale of the Unworthy") #Titulo da janela do jogo
running=True
while running:
    screen.blit(background, (0, 0))
    screen.blit(char1.current_img,(char1.x,char1.y))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP and jump==0:

                char1.move("up")
            if event.key == pygame.K_RIGHT:
                char1.move("right")
            if event.key == pygame.K_LEFT:
                char1.move("left")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                char1.walkR=False
            if event.key == pygame.K_LEFT:
                char1.walkL=False


        # #if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        #     #char1.walkR=True
        # if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
        #     char1.walkR=False
        # # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        # #     char1.walkL=True
        # if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
        #     char1.walkL=False



    #jump=0

    char1.updatepos()
    screen.blit(char1.current_img,(char1.x,char1.y))
    clock.tick(60)
pygame.quit()
quit()
