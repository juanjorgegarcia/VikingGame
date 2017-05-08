import pygame, os
#print (os.getcwd())
pygame.init()

class Player:
    #classe para Player
    def __init__(self,x,y,sprite,speed_):
        self.x = x #coordenada x do personagem
        self.y = y #coordenada y do personagem
        self.sprite=pygame.image.load(sprite).convert() # carregando o sprite parada do player
        self.speed_x = 0 #velocidade no eixo x
        self.speed_y = 0 #velocidade no eixo x
        self.aceleration = + 0.2 #gravidade
        self.walkR = False #status do player andando para direita
        self.walkL = False #status do player andando para esquerda
        self.jump = False #status do player pulando
        self.right= True #sabaer pra onde o jogador esta olhando
        self.current_img = pygame.image.load(sprite) # sprite atual o player
        self.rect=pygame.Surface.get_size(self.current_img) #retangulo equivalente a sprite
    def move(self,direction):
        #movendo o player
        if direction == "left":
            self.speed_x = 10
            self.walkL=True #player esta andando para esquerda
            if self.right==True:
                self.right=False
                char1.current_img = pygame.transform.flip(char1.current_img, True, False)
        if direction == "right":
            self.speed_x = 10
            self.walkR=True #player esta andando para direita
            if self.right==False:
                self.right=True
                char1.current_img = pygame.transform.flip(char1.current_img, True, False)
        if direction == 0:
            self.speed_x = 0
            #self.walkL=False
            #self.walkR=False

        if direction == "up":
            self.aceleration = 0.2 #se o personagem estiver no ar a aceleraçao esta valendo!
            self.speed_y = -10 + self.aceleration
            self.jump = True #player esta pulando!

    def updatepos(self):
        #atualizando a posicao do player
        self.speed_y+=self.aceleration

        if self.y >400:
            #  se a posicao y do player estiver abaixo Do chao a velocidade_y e a gravidade dele se torna 0
            self.speed_y = 0 #
            self.aceleration = 0 #
            self.jump=False #impedindo o jump infinito
            self.y=400 #.99999999999999
        self.y += self.speed_y

        if self.walkR == True:
            self.x += self.speed_x


        if self.walkL == True:
            if self.x > 0:
                self.x -= self.speed_x


######
clock=pygame.time.Clock() #importando o timer
######
######
screen=pygame.display.set_mode((1280,720)) #criando o display do jogo
######
###### carregando o background Do jogo
background = pygame.image.load("8bitvapor.png") #dando load
background = pygame.transform.scale(background, (1280, 720))  #escalano conforme a tela
background = background.convert() #covertenod os pixels da imagem (a imagem é carregada mais rapidamete)
######
############ carregando as sprites do player
player1="Images\\stand.png"
char1=Player(400,400,player1,10)
pwalkright0 = pygame.image.load("Images\\walk right\\sprite_walkR0.png").convert() #dando load
pwalkright0 = pygame.transform.scale(pwalkright0, (char1.rect))#escalano conforme o tamanho personagem
pwalkright1 = pygame.image.load("Images\\walk right\\sprite_walkR1.png").convert() #dando load
pwalkright1 = pygame.transform.scale(pwalkright1, (char1.rect))#escalano conforme o tamanho personagem
pwalkright2 = pygame.image.load("Images\\walk right\\sprite_walkR2.png").convert() #dando load
pwalkright2 = pygame.transform.scale(pwalkright2, (char1.rect))#escalano conforme o tamanho personagem
pwalkright3 = pygame.image.load("Images\\walk right\\sprite_walkR3.png").convert() #dando load
pwalkright3 = pygame.transform.scale(pwalkright3, (char1.rect))#escalano conforme o tamanho personagem
############

pygame.display.set_caption("A Tale of the Unworthy") #Titulo da janela do jogo
running=True
############
while running:
    screen.blit(background, (0, 0)) ### pintando o background
    screen.blit(char1.current_img,(char1.x,char1.y)) ### pintando o player
    pygame.display.update()### atualizando o display
    for event in pygame.event.get(): #pegando as açoes do usuario
        if event.type == pygame.QUIT:
            running=False #saindo do jogo fechando a janela
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False #saindo do jogo apertano esc
            if event.key == pygame.K_UP and char1.jump==False:
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


    char1.updatepos() ## atualizando a posicao do personagem
    screen.blit(char1.current_img,(char1.x,char1.y))### pintando o player
    clock.tick(60) # ajustando o fps
############
pygame.quit() #fechando o pygame
quit() # fechandoo python
