import pygame, os
from numpy import arange
pygame.init()

class Player:
    #classe para Player
    def __init__(self,x,y,sprite):
        self.x = x #coordenada x do personagem
        self.y = y #coordenada y do personagem
        self.sprite=pygame.image.load(sprite).convert() # carregando o sprite parada do player
        self.speed_x = 0 #velocidade no eixo x
        self.speed_y = 0 #velocidade no eixo x
        self.aceleration = + 0.4 #gravidade
        self.walkR = False #status do player andando para direita
        self.walkL = False #status do player andando para esquerda
        self.jump = False #status do player pulando
        self.rightface= True #sabaer pra onde o jogador esta olhando
        self.leftface = False
        self.current_img = pygame.image.load(sprite).convert_alpha() # sprite atual o player
        self.size = pygame.Surface.get_size(self.current_img) #retangulo equivalente a sprite
        self.rect = self.current_img.get_rect(x = self.x, y = self.y)
        self.colision = False # personagem nao esta colidindo
        self.hitbox = pygame.Rect(self.x,self.y,self.x+self.size[0],self.size[1]) #hitbox do personagem
    def move(self,direction):
        #movendo o player
        if direction == "left":
            self.speed_x = 10
            self.walkL=True #player esta andando para esquerda
            if self.rightface==True and self.walkR==False:
                self.rightface=False
                self.leftface=True
                char1.current_img = pygame.transform.flip(char1.current_img, True, False)
                if self.leftface==False:
                    char1.current_img = pygame.transform.flip(char1.current_img, True, False)

        if direction == "right":
            self.speed_x = 10
            self.walkR=True #player esta andando para direita
            if self.rightface==False and self.walkL==False:
                self.leftface=False
                self.rightface=True
                char1.current_img = pygame.transform.flip(char1.current_img, True, False)

        if direction=="stopright":
            self.walkR=False
            if self.walkL==True and self.rightface==True:
                char1.current_img = pygame.transform.flip(char1.current_img, True, False)
                self.leftface=True
                self.rightface=False

        if direction=="stopleft":
            self.walkL=False
            if self.walkR==True and self.leftface==True:
                char1.current_img = pygame.transform.flip(char1.current_img, True, False)
                self.leftface=False
                self.rightface=True

        if direction == 0:
            self.speed_x = 0
            #self.walkL=False
            #self.walkR=False

        if direction == "up":
            self.aceleration = 0.4 #se o personagem estiver no ar a aceleraçao esta valendo!
            self.speed_y = -15 #+ self.aceleration
            self.jump = True #player esta pulando!

    def updatepos(self):
        #atualizando a posicao do player
        self.speed_y+=self.aceleration

        self.y += self.speed_y
        self.rect = self.current_img.get_rect(x=self.x,y=self.y)
        self.hitbox = pygame.Rect(self.x+70,self.y,60,192)
        #print(self.hitbox)
        for i in floor: #floor é a lista q contem todos os objetos da plataforma
            if self.hitbox.colliderect(i.rect) == True: #se o retangulo do player colidir com o da plataforma
                #print("colidindo")
                self.speed_y = 0
                self.aceleration = 0
                self.jump = False
                self.colision = True
                break
            else:
                self.colision=False

        if self.colision == False:
            self.aceleration = 0.4

        if self.walkR == True:
            self.x += self.speed_x


        if self.walkL == True:
            if self.x > 0:
                self.x -= self.speed_x


class Blocks():
    # classe para elementos estáticos do jogo

    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.image = sprite
        self.width,self.height = pygame.Surface.get_size(self.image)
        self.rect = self.image.get_rect(x = self.x, y = self.y)

class Menu():
    #classe para o menu o jogo
    #devera conter funções como, start, savegame, highscore, creditos e customizaçao (posivelmente)
    pass


######
clock=pygame.time.Clock() #importando o timer
######
######
screen_x=1280
screen_y=720
screen=pygame.display.set_mode((screen_x,screen_y)) #criando o display do jogo
######
###### carregando o background Do jogo
background = pygame.image.load("8bitvapor.png") #dando load
background = pygame.transform.scale(background, (screen_x, screen_y))  #escalano conforme a tela
background = background.convert() #covertenod os pixels da imagem (a imagem é carregada mais rapidamete)
######
ground0 = pygame.image.load("Images\\chão\\ground_middle.png").convert()
ground0 = pygame.transform.scale(ground0,(100,100)).convert()
ground = Blocks(800,450,ground0)
groundRange =arange(0,screen_x,ground.width)
############ carregando as sprites do player
player1="Images\\stand.png"
char1=Player(400,400,player1)
char_spritedata = {}
for i in range (3):
    name = "pwalkright{}".format(i)
    pwalkright = pygame.image.load("Images\\walk right\\sprite_walkR{}.png".format(i)).convert()
    pwalkright = pygame.transform.scale(pwalkright, (char1.size))
    char_spritedata[name] = pwalkright
############

pygame.display.set_caption("A Tale of the Unworthy") #Titulo da janela do jogo
running=True
############
while running:
    screen.blit(background, (0, 0)) ### pintando o background
    screen.blit(ground.image,(ground.x,ground.y))
    floor=[ground]
    for i in groundRange:
        chao = Blocks(i,390+char1.size[1],ground.image)
        floor.append(chao)
        screen.blit(ground.image,(i,390+(char1.size[1])))
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
            if char1.walkR==True and char1.walkL==True:
                print("teste")
            if event.key == pygame.K_RIGHT:
                char1.move("right")
            if event.key == pygame.K_LEFT:
                char1.move("left")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                char1.move("stopright")
            if event.key == pygame.K_LEFT:
                char1.move("stopleft")

    char1.updatepos() ## atualizando a posicao do personagem
    floor=[ground]
    screen.blit(char1.current_img,(char1.x,char1.y))### pintando o player
    clock.tick(60) # ajustando o fps
############
pygame.quit() #fechando o pygame
quit() # fechandoo python
