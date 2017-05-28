# -- coding: utf-8 --
import pygame, os
from random import randrange
from numpy import arange
from settings import *


#######
#initializing pygame
pygame.init()
pygame.mixer.init()
#####


class Player(pygame.sprite.Sprite):
    #classe para Player
    def __init__(self,x,y,sprite):
        pygame.sprite.Sprite.__init__(self)
        self.x = x #coordenada x do personagem
        self.y = y #coordenada y do personagem
        self.current_frame=0
        self.last_update=0
        self.load_images()
        self.standimg=0
        self.current_img=pygame.image.load("Images\\Player\\STAND_RIGHT\\stand.png")
        self.speed_x = 0 #velocidade no eixo x
        self.speed_y = 0 #velocidade no eixo x
        self.aceleration = + 0.4 #gravidade
        self.walkR = False #status do player andando para direita
        self.walkL = False #status do player andando para esquerda
        self.jump = False #status do player pulando
        self.rightface= True #sabaer pra onde o jogador esta olhando
        self.leftface = False
        self.look_up=False
        self.attack=False
        self.size = pygame.Surface.get_size(self.current_img) #retangulo equivalente a sprite
        self.rect = self.current_img.get_rect(x = self.x, y = self.y)
        self.collision_floor = False # personagem nao esta colidindo
        self.hitbox = pygame.Rect(self.x,self.y,self.x+self.size[0],self.size[1]) #hitbox do personagem
        self.mask = pygame.mask.from_surface(self.current_img)
        self.collision_enemies = False
        self.collision_plat = False
        #self.rect_atk = pygame.Rect(x = self.x + self.size[0] , y = self.y + (self.size[1])/2 , 50, 40)
        #self.kill = False
        self.rect_atk = pygame.Rect(0,0,0,0)
    def load_images(self):
        self.standingR=Game.loadimages("Images\\Player\\STAND_RIGHT\\stand.png",1,200,200,True)
        self.walkingR_frames=Game.loadimages("Images\\Player\\walk_right\\sprite_walkR{}.png",4,200,200,True)
        self.attackingR_frames=Game.loadimages("Images\\Player\\ATTACK RIGHT\\sprite_ATKRIGHT{}.png",4,400,400,False)
        self.lookingR_up_frames=Game.loadimages("Images\\Player\\CIMA_RIGHT\\cima.png",1,200,200,True)
        self.standingL=Game.loadflipimages(self.standingR)
        self.lookingL_up_frames=Game.loadflipimages(self.lookingR_up_frames)
        self.walkingl_frames=Game.loadflipimages(self.walkingR_frames)
        self.attackingL_frames=Game.loadflipimages(self.attackingR_frames)





    def animate(self):
        now=pygame.time.get_ticks()

        if self.look_up==True and self.walkR==False and self.walkL==False and self.jump==False:
            if self.rightface==True:
                self.current_img=self.lookingR_up_frames[0]
            if self.leftface==True:
                self.current_img=self.lookingL_up_frames[0]

        elif self.walkR==True and self.walkL==True and self.jump==False:
            self.current_img=self.standingL[0]

        elif self.walkR==False and self.walkL==False and self.jump==False and self.attack==False:
            if self.leftface==True:
                self.current_img=self.standingL[0]
            if self.rightface==True:
                self.current_img=self.standingR[0]

        elif self.walkR==True and self.jump==False:
            if now - self.last_update>80:
                self.attack=False
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.walkingR_frames)
                self.current_img=self.walkingR_frames[self.current_frame]
                self.current_img=pygame.transform.scale(self.current_img,(200,200))

        elif self.walkL==True and self.jump==False:
            if now - self.last_update>80:
                self.attack=False
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.walkingl_frames)
                self.current_img=self.walkingl_frames[self.current_frame]
                self.current_img=pygame.transform.scale(self.current_img,(200,200))

        elif self.attack==True and self.rightface==True:
            if now - self.last_update>90:
                self.attack==False
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.attackingR_frames)
                self.current_img=self.attackingR_frames[self.current_frame]
                if self.current_frame==0:
                    self.attack=False
                    self.current_frame=0

        elif self.attack==True and self.leftface==True:
            if now - self.last_update>90:
                self.attack==False
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.attackingL_frames)
                self.current_img=self.attackingL_frames[self.current_frame]
                if self.current_frame==0:
                    self.attack=False
                    self.current_frame=0

        elif self.attack==True and self.rightface==True and self.jump==True:
            if now - self.last_update>90:
                self.attack==False
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.attackingL_frames)
                self.current_img=self.attackingL_frames[self.current_frame]
                if self.current_frame==0:
                    self.attack=False
                    self.current_frame=0


        elif self.attack==True and self.leftface==True and self.jump==True:
            if now - self.last_update>90:
                self.attack==False
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.attackingR_frames)
                self.current_img=self.attackingR_frames[self.current_frame]
                if self.current_frame==0:
                    self.attack=False
                    self.current_frame=0






    def move(self,direction):
        #movendo o player
        if direction == "left":
            self.speed_x = 10
            self.walkL=True #player esta andando para esquerda
            self.leftface=True
            self.rightface=False

        if direction == "right":
            self.speed_x = 10
            self.walkR=True #player esta andando para direita
            self.rightface=True
            self.leftface=False

        if direction=="stopright":
            self.walkR=False
            self.current_frame=0

        if direction=="stopleft":
            self.walkL=False
            self.current_frame=0
        if direction=="stop_attack":
            self.attack=False

        if direction=="look_up":
            self.look_up=True

        if direction=="stoplook_up":
            self.look_up=False

        if direction=="attack":
            self.attack=True
            if self.rightface == True :
                self.rect_atk = pygame.Rect(self.x + self.size[0] -20 , self.y + (self.size[1])/2 +20, 100, 50)
                pygame.draw.rect(screen,(255,0,0),self.rect_atk)
            else:
                self.rect_atk = pygame.Rect(self.x -100  , self.y + (self.size[1])/2 +20, 100, 50)
                pygame.draw.rect(screen,(255,0,255),self.rect_atk)


        if direction == 0:
            self.speed_x = 0


        if direction == "up":
            if self.attack==False:
                self.aceleration = 0.4 #se o personagem estiver no ar a aceleraçao esta valendo!
                self.speed_y = -15 #+ self.aceleration
                self.jump = True #player esta pulando!
                self.current_frame=0


    def updatepos(self):
        global addBg
        #atualizando a posicao do player
        self.animate()
        self.speed_y+=self.aceleration
        self.y += self.speed_y
        self.rect = self.current_img.get_rect(x=self.x,y=self.y)
        self.hitbox = pygame.Rect(self.x+70,self.y,60,192)
        self.mask = pygame.mask.from_surface(self.current_img)

        for i in floor: #floor é a lista q contem todos os quadrados do chao do jogo
            if self.hitbox.colliderect(i.rect) == True: #se o retangulo do player colidir com o da plataforma
                    self.speed_y = 0
                    self.aceleration = 0
                    self.jump = False
                    self.collision_floor = True
                    self.y = i.rect.top - self.size[1]
                    break
            else:
                self.collision_floor=False

        for i in aero:
            #aero é a lista que contem todas as plataformas aéreas do jogo
            if self.speed_y > 0 :
                ## se o player estiver caindo
                if self.hitbox.colliderect(i.rect) == True and self.rect.midbottom[1] <= i.rect.center[1] - (i.height)/4 :
                    ##  se o player colidir com a plataforma e seu pé estiver entre 1/4 da altura da plataforma
                    self.collision_plat = True
                    self.speed_y = 0
                    self.aceleration = 0
                    self.jump = False
                    self.y = i.rect.top - self.size[1]
                    ## player para e é mandado para o topo da plataforma
                    break
                else:
                    self.collision_plat = False
                    #self.jump = True
        for i in enemies:
            #enemies é uma lista que contem todos os inimigos do player
            if self.rect.colliderect(i.rect) ==  True:
                if not pygame.sprite.collide_mask(self,i) == None:
                    self.collision_enemies= True
                    print("morreu")
                    break
                else:
                    self.collision_enemies = False

            elif self.rect_atk.colliderect(i.rect) == True:
                i.death = True
            else:
                self.collision_enemies = False

        if self.collision_floor == False:
            self.aceleration = 0.4

        if self.collision_enemies == True:
            addBg = 0
            self.x = 400

        if self.walkR == True:
            if self.x < screen_x/2:
                self.x += self.speed_x
            elif self.x >= screen_x/2 and self.x+addBg+pygame.Surface.get_width(self.current_img) <= map_x:
                addBg = addBg + self.speed_x

        if self.walkL == True:
            if self.x > 0 and addBg <= 0:
                self.x -= self.speed_x
            elif self.x > 0 and addBg > 0:
                addBg = addBg - self.speed_x

class Enemy(pygame.sprite.Sprite):
 #     #classe para os minions/mobs
    def __init__(self,x,y,limitx1,limitx2,limity1,limity2,sprite,movingx,movingy,race):
        pygame.sprite.Sprite.__init__(self)
        self.race=race
        self.x=x #coordenada x do personagem
        self.y=y #coordenada y do personagem
        self.current_frame=0
        self.limitx1=limitx1
        self.limity1=limity1
        self.limitx2=limitx2
        self.limity2=limity2
        self.last_update=0
        self.load_images()
        self.standimg=0
        self.current_img=sprite
        self.speed_x = 0 #velocidade no eixo x
        self.speed_y = 0 #velocidade no eixo x
        self.aceleration = + 0.4 #gravidade
        self.walkR = movingx #status do player andando para direita
        self.walkL = False #status do player andando para esquerda
        self.jump = False #status do player pulando
        self.moveUP=movingy
        self.rightface= False #saber pra onde o inimigo esta olhando
        self.leftface = True
        self.size = pygame.Surface.get_size(self.current_img) #retangulo equivalente a sprite
        self.rect = self.current_img.get_rect(x = self.x, y = self.y)
        self.collision_floor = False # personagem nao esta colidindo
        self.hitbox = pygame.Rect(self.x,self.y,self.x+self.size[0],self.size[1]) #hitbox do personagem
        self.mask = pygame.mask.from_surface(self.current_img)
        self.death = False
    def load_images(self):
        #self.slimeL=[pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_1.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_2.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_3.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_4.png")]
        self.slimeL=Game.loadimages("Images\\Inimigos\\Slime\\slime_{}.png",5,100,100,True)
        self.slimeR=Game.loadflipimages(self.slimeL)
        self.dragonL=Game.loadimages("Images\\Inimigos\\Flying demon\\sprite_{}.png",2,300,300,True)
        self.dragonR=Game.loadflipimages(self.dragonL)


    def animate(self):
        now=pygame.time.get_ticks()
        if self.race=="Slime":

            if self.leftface==True and self.rightface==False:
                if now - self.last_update>120:
                    self.last_update=now
                    self.current_frame=(self.current_frame+1)%len(self.slimeL)
                    self.current_img=self.slimeL[self.current_frame]

            elif self.rightface==True and self.leftface==False:
                if now - self.last_update>120:
                    self.last_update=now
                    self.current_frame=(self.current_frame+1)%len(self.slimeR)
                    self.current_img=self.slimeR[self.current_frame]


        if self.race=="Dragon":


            if now - self.last_update>200:
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.dragonL)
                self.current_img=self.dragonL[self.current_frame]




    def move(self,speed_x,speed_y):

        if self.walkR==True:
            self.speed_x=+speed_x
            self.rightface=True
            self.leftface=False

        if self.x==self.limitx1 and self.walkR == True:
            self.speed_x=-speed_x
            self.leftface=True
            self.rightface=False
            self.walkR=False

        elif self.x == self.limitx2:
            self.walkR=True

        if self.moveUP==True:
            self.speed_y=-speed_y

        if self.y<self.limity1 and self.moveUP == True:
            self.speed_y=+speed_y
            self.moveUP=False

        elif self.y > self.limity2:
            self.moveUP=True



    def update(self):
        self.animate()
        self.x+=self.speed_x
        if char1.walkR == True and addBg > 0:
            self.x = self.x - char1.speed_x
        if char1.walkL == True and addBg > 0:
            self.x = self.x + char1.speed_x
        self.y+=self.speed_y
        self.mask = pygame.mask.from_surface(self.current_img)
        self.rect = self.current_img.get_rect(x = self.x, y = self.y)

        if self.death == True:
            self.kill()


class Blocks(pygame.sprite.Sprite):
    # classe para elementos estáticos do jogo

    def __init__(self,x,y,sprite):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = sprite
        self.width,self.height = pygame.Surface.get_size(self.image)
        self.rect = self.image.get_rect(x = self.x, y = self.y)
        #self.top = [[self.x,self.width + self.x],[self.y-char1.size[1],self.y-char1.size[1]]]

    def move(self,speed):
        if char1.walkR == True and addBg > 0:
            self.x+= -speed - char1.speed_x*0.1
        elif char1.walkL == True and addBg > 0:
            self.x+= -speed + char1.speed_x*0.1
        else:
            self.x+= -speed
        if self.x<(0-self.width):
            self.x = 1280
            self.y = randrange(0,300)

class Game():
    #classe para o menu o jogo
    #devera conter funções como, start, savegame, highscore, creditos e customizaçao (posivelmente)
    def loadimages(sprite,Nframes,sizex,sizey,Siz):
        lista=[]
        if Siz==True:
            for i in range(Nframes):
                S=pygame.image.load(sprite.format(i)).convert_alpha()
                S=pygame.transform.scale(S,(sizex,sizey)).convert_alpha()
                lista.append(S)
            return lista

        if Siz==False:
            for i in range(Nframes):
                S=pygame.image.load(sprite.format(i))
                lista.append(S)
            return lista

        return lista

    def loadflipimages(Rimagelist):
        lista=[]
        for frame in Rimagelist:
            lista.append(pygame.transform.flip(frame,True,False))
        return lista

    def update():
        dragon1.update()
        dragon1.move(0,3)
        slime2.move(5,0)
        slime1.move(5,0)
        slime1.update()
        slime2.update()
        char1.updatepos()



######
clock = pygame.time.Clock() #importando o timer
######
######
#char1=Player(400,400,player1)
map_x = 5000
map_y = 720
screen=pygame.display.set_mode((screen_x,screen_y)) #criando o display do jogo
######
###### carregando o background Do jogo
vapor = pygame.image.load("8bitvapor.png").convert()
background = vapor #dando load
background = pygame.transform.scale(background, (screen_x, screen_y))  #escalano conforme a tela
addBg = 0
######
cloud = pygame.image.load("Images\\Plataforma\\NUVEM\\CLOUD.png").convert_alpha()
cloud = pygame.transform.scale(cloud,(50,50))
cloudi = Blocks(1280,150,cloud)

cloud2 = pygame.image.load("Images\\Plataforma\\NUVEM\\CLOUD_2.png").convert_alpha()
cloud2 = pygame.transform.scale(cloud2,(30,30))
cloudi2 = Blocks(1280,200,cloud2)
cloud3 = pygame.image.load("Images\\Plataforma\\NUVEM\\CLOUD_3.png").convert_alpha()

clouds = [cloud,cloud2,cloud3]

#################

############ carregando as sprites do player
player1="Images\\Player\\STAND_RIGHT\\stand.png"
char1=Player(400,400,player1)
char_spritedata = {}
####################
#enemies = []
dragon=pygame.image.load("Images\\Inimigos\\Flying demon\\sprite_0.png").convert()
Slime1=pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png").convert()
slime11=pygame.transform.scale(Slime1,(100,100))
#(self,x,y,limitx1,limitx2,limity1,limity2,sprite,movingx,movingy,race):
slime1=Enemy(1100,500,1100,0,0,0,slime11,False,False,"Slime")
slime2=Enemy(500,500,600,50,0,0,slime11,True,False,"Slime")
dragon1=Enemy(1200,200,0,0,-90,200,dragon,True,True,"Dragon")
enemies = pygame.sprite.Group(slime1,slime2)
#################################
############
jump = pygame.mixer.Sound("Jump10.wav")
music1 = pygame.mixer.music.load("Heroic Demise (New).mp3")
############
kkkeae = pygame.image.load("kkkeaeman.jpg").convert()
############

ground0 = pygame.image.load("Images\\Plataforma\\CHÃO\\ground_middle.png").convert()
ground0 = pygame.transform.scale(ground0,(100,100)).convert()
ground = Blocks(300,300,ground0)
ground2 = Blocks(400,300,ground0)
ground3 = Blocks(800-addBg,200,ground0)
ground4 = Blocks(900-addBg,200,ground0)
ground5 = Blocks(1000-addBg,200,ground0)

groundRange = arange(0,map_x,pygame.Surface.get_width(ground0))

pygame.display.set_caption(title) #Titulo da janela do jogo
running=True
############

while running:
    screen.blit(background, (0, 0)) ### pintando o background
    ground = Blocks(300-addBg,300,ground0)
    ground2 = Blocks(300+ground.width-addBg,300,ground0)
    ground3 = Blocks(800-addBg,200,ground0)
    ground4 = Blocks(900-addBg,200,ground0)
    ground5 = Blocks(1000-addBg,200,ground0)
    aero=[ground,ground2,ground3,ground4,ground5]
    for i in aero:
        screen.blit(i.image,(i.x,i.y))
    cloudi.move(2)
    cloudi2.move(1.5)
    screen.blit(cloudi.image,(cloudi.x,cloudi.y))
    screen.blit(cloudi2.image,(cloudi2.x,cloudi2.y))
    floor=[]
    for i in groundRange:
        chao = Blocks(i-addBg,390+char1.size[1],ground.image)
        floor.append(chao)
        screen.blit(chao.image,(i-addBg,390+(char1.size[1])))
    for i in enemies:
        if i.death == False:
            screen.blit(i.current_img,(i.x,i.y))
    screen.blit(char1.current_img,(char1.x,char1.y)) ### pintando o player
    for event in pygame.event.get(): #pegando as açoes do usuario
        if event.type == pygame.QUIT:
            running=False #saindo do jogo fechando a janela
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pygame.mixer.music.play(loops=-1)
            if event.key == pygame.K_ESCAPE:
                running = False #saindo do jogo apertano esc
            if event.key == pygame.K_SPACE and char1.jump==False:
                char1.move("up")
                #jump.play()
            if event.key == pygame.K_w:
                char1.move("look_up")
            if event.key == pygame.K_d:
                char1.move("right")
            if event.key == pygame.K_a:
                char1.move("left")
            if event.key == pygame.K_j:
                char1.move("attack")
            if event.key == pygame.K_k:
                background = kkkeae
                background = pygame.transform.scale(background, (screen_x, screen_y))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                char1.move("stopright")
            if event.key == pygame.K_a:
                char1.move("stopleft")
            if event.key == pygame.K_w:
                char1.move("stoplook_up")
            if event.key == pygame.K_k:
                background = vapor
                background = pygame.transform.scale(background, (screen_x, screen_y))
            if event.key == pygame.K_j:
                char1.rect_atk = pygame.Rect(0,0,0,0)
     ## atualizando a posicao do personagem
    Game.update()
    floor=[]
    clock.tick(fps) # ajustando o fps
    pygame.display.update()### atualizando o display
############
pygame.quit() #fechando o pygame
quit() # fechandoo python
