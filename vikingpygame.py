# -- coding: utf-8 --
#########################BUGS:################################
#Dragão dasaparece do nada
#Colisão lateral pode ser implementada para o obstaculo no chao (done)
#Imagem do kkkeae nao esta sendo mostrada
##############################################################
import pygame, os
from random import randrange
from numpy import arange
from settings import *
import time


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
        self.attackframe=0
        self.last_update=0
        self.load_images()
        self.standimg = 0
        self.current_img = pygame.image.load("Images\\Player\\STAND_RIGHT\\stand.png")
        self.speed_x = 0 #velocidade no eixo x
        self.speed_y = 0 #velocidade no eixo x
        self.aceleration = 0 #gravidade
        self.walkR = False #status do player andando para direita
        self.walkL = False #status do player andando para esquerda
        self.jump = False #status do player pulando
        self.rightface= True #sabaer pra onde o jogador esta olhando
        self.leftface = False
        self.look_up = False
        self.attack = False
        self.size = pygame.Surface.get_size(self.current_img) #retangulo equivalente a sprite
        self.rect = self.current_img.get_rect(x = self.x, y = self.y)
        self.collision_floor = False # personagem nao esta colidindo
        self.hitbox = pygame.Rect(self.x,self.y,self.x+self.size[0],self.size[1]) #hitbox do personagem
        self.mask = pygame.mask.from_surface(self.current_img)
        self.collision_enemies = False
        self.collision_plat = False
        self.life = 3
        self.ignore = 0
        self.hurt = False

    def load_images(self):
        self.standingR=Game.loadimages("Images\\Player\\STAND_RIGHT\\stand.png",1,200,200,True)
        self.walkingR_frames=Game.loadimages("Images\\Player\\walk_right\\sprite_walkR{}.png",4,200,200,True)
        self.attackingR_frames=Game.loadimages("Images\\Player\\ATTACK RIGHT\\sprite_ATKRIGHT{}.png",5,450,200,True)
        self.lookingR_up_frames=Game.loadimages("Images\\Player\\CIMA_RIGHT\\cima.png",1,200,200,True)
        self.standingL=Game.loadflipimages(self.standingR)
        self.lookingL_up_frames=Game.loadflipimages(self.lookingR_up_frames)
        self.walkingl_frames=Game.loadflipimages(self.walkingR_frames)
        self.attackingL_frames=Game.loadflipimages(self.attackingR_frames)
        self.hurtingR = Game.loadimages("Images\\Player\\OUCH_RIGHT\\sprite_{}.png",3,200,200,True)
        self.hurtingL = Game.loadflipimages(self.hurtingR)


    def animate(self):
        now=pygame.time.get_ticks()
        if self.look_up==True and self.walkR==False and self.walkL==False and self.jump==False and self.attack==False:
            if self.rightface==True:
                self.current_img=self.lookingR_up_frames[0]
            if self.leftface==True:
                self.current_img=self.lookingL_up_frames[0]

        elif self.hurt == True and self.rightface == True:
            if now - self.last_update>200:
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.hurtingR)
                self.current_img=self.hurtingR[self.current_frame]
                if self.current_frame==0:
                    self.hurt = False
                    self.current_frame=0

        elif self.hurt == True and self.leftface == True:
            if now - self.last_update>200:
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.hurtingL)
                self.current_img=self.hurtingL[self.current_frame]
                if self.current_frame==0:
                    self.hurt = False
                    self.current_frame=0


        elif self.walkR==True and self.walkL==True and self.jump==False:
            if self.leftface==True:
                self.current_img=self.standingL[0]
            if self.rightface==True:
                self.current_img=self.standingR[0]

        elif self.walkR==False and self.walkL==False and self.jump==False and self.attack==False:
            if self.leftface==True:
                self.current_img=self.standingL[0]
            if self.rightface==True:
                self.current_img=self.standingR[0]

        elif self.walkR==True and self.jump==False and self.attack==False:
            if now - self.last_update>80:
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.walkingR_frames)
                self.current_img=self.walkingR_frames[self.current_frame]
                self.current_img=pygame.transform.scale(self.current_img,(200,200))

        elif self.walkL==True and self.jump==False and self.attack==False:
            if now - self.last_update>80:
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.walkingl_frames)
                self.current_img=self.walkingl_frames[self.current_frame]
                self.current_img=pygame.transform.scale(self.current_img,(200,200))

        elif self.attack==True and self.rightface==True:
            if now - self.last_update>90:
                self.last_update=now
                self.attackframe=(self.attackframe+1)%len(self.attackingR_frames)
                self.current_img=self.attackingR_frames[self.attackframe]
                if self.attackframe==0:
                    self.attack=False


        elif self.attack==True and self.leftface==True:
            if now - self.last_update>90:
                self.last_update=now
                self.attackframe=(self.attackframe+1)%len(self.attackingL_frames)
                self.current_img=self.attackingL_frames[self.attackframe]
                if self.attackframe==0:
                    self.attack=False


        elif self.attack==True and self.rightface==True and self.jump==True:
            if now - self.last_update>90:
                self.last_update=now
                self.attackframe=(self.attackframe+1)%len(self.attackingL_frames)
                self.current_img=self.attackingL_frames[self.attackframe]
                if self.attackframe==0:
                    self.attack=False


        elif self.attack==True and self.leftface==True and self.jump==True:
            if now - self.last_update>90:
                self.last_update=now
                self.attackframe=(self.attackframe+1)%len(self.attackingR_frames)
                self.current_img=self.attackingR_frames[self.attackframe]
                if self.attackframe==0:
                    self.attack=False



        elif self.jump==True:
            if self.rightface==True:
                self.current_img=self.standingR[0]
            if self.leftface==True:
                self.current_img=self.standingL[0]


    def move(self,direction):
        #movendo o player
        if direction == "left":
            if self.attack==False:
                self.speed_x = 10
                self.walkL=True #player esta andando para esquerda
                self.leftface=True
                self.rightface=False

        if direction == "right":
            if self.attack==False:
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

        if direction == 0:
            self.speed_x = 0


        if direction == "up":
            if self.attack==False:
                self.aceleration = 0.4 #se o personagem estiver no ar a aceleraçao esta valendo!
                self.speed_y = -15 #+ self.aceleration
                self.jump = True #player esta pulando!
                self.current_frame=0

    def updatepos(self):
        global addBg,diescreen
        #atualizando a posicao do player
        self.animate()
        self.speed_y+=self.aceleration
        self.y += self.speed_y
        self.rect = self.current_img.get_rect(x=self.x,y=self.y)
        self.hitbox = pygame.Rect(self.x+70,self.y,60,192)
        self.mask = pygame.mask.from_surface(self.current_img)
        self.ignore += 1
        #print("vel",self.speed_y)


        for i in floor: #floor é a lista q contem todos os quadrados do chao do jogo
            if self.hitbox.colliderect(i.rect) == True: #se o retangulo do player colidir com o da plataforma
                    self.speed_y = 0
                    self.aceleration = 0
                    self.jump = False
                    self.y = i.rect.top - self.size[1]
                    self.collision_floor = True
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
        for i in obs:
            if self.rect.colliderect(i.rect) == True:
                if self.speed_y > 0 and self.hitbox.colliderect(i.rect) == True:
                    ## se o player estiver caindo
                    self.speed_y = 0
                    self.aceleration = 0
                    self.jump = False
                    self.y = i.rect.top - self.size[1]
                    break
                elif self.aceleration == 0 and self.x > i.x and self.walkR==False:
                    self.speed_y = 0

                    self.speed_x = 0
                elif self.aceleration == 0 and self.x < i.x and self.walkL==False:
                    self.speed_y = 0
                    self.speed_x = 0

        for i in enemies:
            #enemies é uma lista que contem todos os inimigos do player
            if self.rect.colliderect(i.rect) ==  True and self.ignore >=120 : #2 segundos de invulnerabilidade
                if not pygame.sprite.collide_mask(self,i) == None:
                    if self.attack == False:
                        self.collision_enemies= True
                        self.hurt = True
                        if i.x > self.x and self.speed_y < 1:
                            print("direita")
                            self.x -= 100
                        elif i.x < self.x and self.speed_y < 1:
                            print("esquerda")
                            self.x+=100
                        elif self.speed_y>1:
                            print("por cima")
                            self.speed_y = -8
                        self.ignore = 0
                        break
                    else:
                        #self.hurt = False
                        if self.rightface == True and i.x > self.x:
                            i.death = True
                            if oi:
                                soled.play()
                            print("Matei direita")
                        elif self.leftface == True and i.x < self.x:
                            i.death = True
                            if oi:
                                soled.play()
                            print("Matei esquerda")
                else:
                    self.collision_enemies = False

            else:
                self.collision_enemies = False

        for i in water_list:
            if self.rect.colliderect(i.rect) == True:
                self.speed_x = 0
                if self.y > i.y:
                    death01.play()
                    diescreen = True

        if self.collision_floor == False:
            self.aceleration = 0.4

        if self.collision_enemies == True:
            self.life-=1
            if self.life>0:
                dmg01.play()
            else:
                print("you loose")
                death01.play()
                diescreen = True
            addBg = 0
            print(self.life)

        if self.walkR == True and self.jump==False:
            if self.attack==False:
                if self.x < screenPlayerAreaMax:
                    self.x += self.speed_x
                elif self.x >= screenPlayerAreaMax and self.x+addBg+pygame.Surface.get_width(self.current_img) <= map_x:
                    addBg = addBg + self.speed_x

        if self.walkL == True and self.jump==False:
            if self.attack==False:
                if self.x <= screenPlayerAreaMin and addBg <= 0 and self.x >= 0:
                    self.x -= self.speed_x
                elif self.x > screenPlayerAreaMin and addBg > 0:
                    self.x -= self.speed_x
                elif self.x > screenPlayerAreaMin and addBg <= 0:
                    self.x -= self.speed_x
                elif self.x <= screenPlayerAreaMin and addBg > 0:
                    addBg = addBg - self.speed_x

        if self.walkR == True and self.jump==True:
            if self.x < screenPlayerAreaMax:
                self.x += self.speed_x
            elif self.x >= screenPlayerAreaMax and self.x+addBg+pygame.Surface.get_width(self.current_img) <= map_x:
                addBg = addBg + self.speed_x

        elif self.walkL == True and self.jump==True:
            if self.x > screenPlayerAreaMin:
                self.x -= self.speed_x
            if self.x <= screenPlayerAreaMin and addBg > 0:
                addBg = addBg - self.speed_x


class Enemy(pygame.sprite.Sprite):
 #     #classe para os minions/mobs
    def __init__(self,x,y,limitx1,limitx2,limity1,limity2,sprite,movingx,movingy,race):
        pygame.sprite.Sprite.__init__(self)
        self.race=race
        self.x=x #coordenada x do personagem
        self.xOriginal = x
        self.y=y #coordenada y do personagem
        self.current_frame=0
        self.death_frame=0
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
        self.traveledDistance = 0#Marca quantos pixels o inimigo andou em relação ao offset (addBg)
        self.death = False

    def load_images(self):
        #self.slimeL=[pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_1.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_2.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_3.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_4.png")]
        self.slimeL=Game.loadimages("Images\\Inimigos\\Slime\\slime_{}.png",5,100,100,True)
        self.slimeR=Game.loadflipimages(self.slimeL)
        self.slimeLD=Game.loadimages("Images\\Inimigos\\Slime\\Slime death\\sprite_{}.png",6,100,100,True)
        self.slimeRD=Game.loadflipimages(self.slimeLD)
        self.dragonL=Game.loadimages("Images\\Inimigos\\Flying demon\\sprite_{}.png",2,300,300,True)
        self.dragonR=Game.loadflipimages(self.dragonL)


    def animate(self):
        now=pygame.time.get_ticks()

        if self.race=="Slime":

            if self.leftface==True and self.rightface==False and self.death==False:
                if now - self.last_update>120:
                    self.last_update=now
                    self.current_frame=(self.current_frame+1)%len(self.slimeL)
                    self.current_img=self.slimeL[self.current_frame]

            elif self.rightface==True and self.leftface==False and self.death==False:
                if now - self.last_update>120:
                    self.last_update=now
                    self.current_frame=(self.current_frame+1)%len(self.slimeR)
                    self.current_img=self.slimeR[self.current_frame]

            if self.death == True:
                self.speed_x=0
                self.speed_y=0
                if self.leftface==True:
                    if now - self.last_update>190:
                        self.last_update=now
                        self.death_frame=(self.death_frame+1)%len(self.slimeLD)
                        self.current_img=self.slimeLD[self.death_frame]
                        if self.death_frame==0:
                            self.kill()
                if self.rightface==True:
                    if now - self.last_update>190:
                        self.last_update=now
                        self.death_frame=(self.death_frame+1)%len(self.slimeRD)
                        self.current_img=self.slimeRD[self.death_frame]
                        if self.death_frame==0:
                            self.kill()





        if self.race=="Dragon":

            if now - self.last_update>200:
                self.last_update=now
                self.current_frame=(self.current_frame+1)%len(self.dragonL)
                self.current_img=self.dragonL[self.current_frame]
            if self.death == True:
                self.kill()




    def move(self,speed_x,speed_y):

        if self.walkR==True:
            self.speed_x=+speed_x
            self.rightface=True
            self.leftface=False

        if self.x==self.limitx1-addBg and self.walkR == True:
            self.speed_x=-speed_x
            self.leftface=True
            self.rightface=False
            self.walkR=False

        elif self.x == self.limitx2-addBg:
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
        if char1.walkR == True and addBg > 0 and char1.x >= screenPlayerAreaMax:
            self.x = self.x - char1.speed_x
            self.traveledDistance += char1.speed_x
        elif addBg <= 0:
            self.x = self.x + self.traveledDistance
            self.traveledDistance = 0

        if char1.walkL == True and addBg > 0 and char1.x <= screenPlayerAreaMin:
            self.x = self.x + char1.speed_x
            self.traveledDistance -= char1.speed_x
        elif addBg <= 0:
            self.x = self.x + self.traveledDistance
            self.traveledDistance = 0

        self.y+=self.speed_y
        self.mask = pygame.mask.from_surface(self.current_img)
        self.rect = self.current_img.get_rect(x = self.x, y = self.y)

        # if self.death == True:
        #     self.kill()



class Blocks(pygame.sprite.Sprite):
    # classe para elementos estáticos do jogo

    def __init__(self,x,y,sprite):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = sprite
        self.width,self.height = pygame.Surface.get_size(self.image)
        self.rect = self.image.get_rect(x = self.x, y = self.y)

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
        slime2.update()
        char1.updatepos()
        clock.tick(fps) # ajustando o fps
        pygame.display.update()### atualizando o display

    def animateBG(bgImages): #Função que anima o background
        global last_bg_update, current_bg_frame, current_bg_image
        bgAnimationNOW = pygame.time.get_ticks()
        if bgAnimationNOW - last_bg_update > 200:
            last_bg_update = bgAnimationNOW
            current_bg_frame=(current_bg_frame+1)%len(bgImages)
            current_bg_image = bgImages[current_bg_frame]
        return current_bg_image

    def goal(charHitbox,blockHitbox):
        if charHitbox.colliderect(blockHitbox) == True:
            return True
        else:
            return False
playLoop = True

def yodao():
    global death01,jump,atk01,soled,oi
    death01 = pygame.mixer.Sound("Soundfx\\yoda_lago.wav")
    jump = pygame.mixer.Sound("Soundfx\\yoda_fon.wav")
    atk01 = pygame.mixer.Sound("Soundfx\\yoda_hi.wav")
    soled = pygame.mixer.Sound("Soundfx\\yoda_solado.wav")
    oi = True
oi = False
######
clock = pygame.time.Clock() #importando o timer
######
######
#char1=Player(400,400,player1)
map_x = 5000
map_y = 720
screen=pygame.display.set_mode((screen_x,screen_y)) #criando o display do jogo
screenPlayerAreaMin = 400
screenPlayerAreaMax = screen_x/2
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
last_bg_update = 0
current_bg_frame = 0
current_bg_image = 0
bgImages = Game.loadimages("Images\\Background_fire\\sprite_{}.png",14,screen_x,screen_y,True)

############ carregando as sprites do player
player1="Images\\Player\\STAND_RIGHT\\stand.png"
char1=Player(400,400,player1)
char_spritedata = {}
####################

dragon=pygame.image.load("Images\\Inimigos\\Flying demon\\sprite_0.png").convert()
Slime1=pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png").convert()
slime11=pygame.transform.scale(Slime1,(100,100))
#(self,x,y,limitx1,limitx2,limity1,limity2,sprite,movingx,movingy,race):
slime2=Enemy(1100,500,1100,0,0,0,slime11,True,False,"Slime")
#enemies.append(slime1)
#slime1=Enemy(500,500,600,0,0,0,slime11,True,False,"Slime")
dragon1=Enemy(1200,200,0,0,-90,200,dragon,False,True,"Dragon")
enemies = pygame.sprite.Group(slime2,dragon1)
#################################
############


atk01 = pygame.mixer.Sound("Soundfx\\atk_01.wav")
death01 = pygame.mixer.Sound("Soundfx\\death_01.wav")
jump = pygame.mixer.Sound("Soundfx\\Jump_00.wav")
dmg01 = pygame.mixer.Sound("Soundfx\\damage_01.wav")
music1 = pygame.mixer.music.load("Soundfx\\Heroic Demise (New).mp3")

############
kkkeae = pygame.image.load("kkkeaeman.jpg").convert()
############
water = pygame.image.load("Images\\Plataforma\\Agua\\Agua clone\\sprite_0.png").convert_alpha()
water = pygame.transform.scale(water,(100,100))

ground0 = pygame.image.load("Images\\Plataforma\\CHÃO\\ground_middle.png").convert()
ground0 = pygame.transform.scale(ground0,(100,100)).convert()
groundDEFAULT = Blocks(300,300,ground0)

obstaculo0 = pygame.image.load("Images\\Plataforma\\CHÃO\\sprite_0.png").convert()
obstaculo0 = pygame.transform.scale(obstaculo0,(100,100)).convert()
obstaculoDEFAULT = Blocks(300,300,obstaculo0)
#obs = pygame.sprite.Group()
########
groundRange = arange(0,map_x,pygame.Surface.get_width(ground0))
###
endBlockIMG = pygame.image.load("Images\\end_block.png").convert_alpha()#Bloco final do mapa
endBlockIMG = pygame.transform.scale(endBlockIMG,(100,100)).convert_alpha()
#####
diedIMG = pygame.image.load("Images\\menu\\you_died.png").convert()#Bloco final do mapa
diescreen = False
#####
restart = False #Variavel para recomeçar o jogo do zero
#####################################FIM DAS VARIAVEIS ------> LEMBRAR DE COPIAR E COLAR NO DPLAYLOOP O QUE FOR VARIAVEL##################################

pygame.display.set_caption(title) #Titulo da janela do jogo

while playLoop: ######LOOP DO RESTART DO JOGO
    char1=Player(400,400,player1)
    clouds = [cloud,cloud2,cloud3]
    addBg = 0
    last_bg_update = 0
    current_bg_frame = 0
    current_bg_image = 0
    slime2=Enemy(1100,530,1100,0,0,0,slime11,True,False,"Slime")
    dragon1=Enemy(1200,200,0,0,-90,200,dragon,False,True,"Dragon")
    slime3=Enemy(1400 + 100,430,1100,2000-100,0,0,slime11,True,False,"Slime")
    enemies = pygame.sprite.Group(slime2,dragon1,slime3)
    diescreen = False
    restart = False
    char1.walkR = False
    char1.walkL = False

    running=True
    ############
    while running:
        if background == kkkeae:
            screen.blit(background, (0, 0))
        else:
            screen.blit(Game.animateBG(bgImages), (0, 0)) ### pintando o background
        cloudi.move(2)
        cloudi2.move(1.5)
        screen.blit(cloudi.image,(cloudi.x,cloudi.y))
        screen.blit(cloudi2.image,(cloudi2.x,cloudi2.y))

        #######LISTA DOS CHAOS NO MAPA
        ground10 = Blocks(300-addBg,350,ground0)
        ground11 = Blocks(300+groundDEFAULT.width-addBg,350,ground0)
        ground12 = Blocks(300+groundDEFAULT.width*2-addBg,350,ground0)
        ground20 = Blocks(800-addBg,200,ground0)
        ground21 = Blocks(800+groundDEFAULT.width-addBg,200,ground0)
        ground22 = Blocks(800+groundDEFAULT.width*2-addBg,200,ground0)
        obs_1 = Blocks(1400-addBg,430+char1.size[1]-groundDEFAULT.height,obstaculoDEFAULT.image)
        obs_2 = Blocks(2000-addBg,430+char1.size[1]-groundDEFAULT.height,obstaculoDEFAULT.image)
        obs_3 = Blocks(2000-addBg,-obs_1.height+430+char1.size[1]-groundDEFAULT.height,obstaculoDEFAULT.image)
        water0 = Blocks(3100-addBg,635,water)
        water1 = Blocks(3200-addBg,635,water)
        water2 = Blocks(3300-addBg,635,water)
        water_list=[water0,water1,water2]

        #obs.add(obs_1)
        obs=[obs_1,obs_2,obs_3]
        for i in obs:
            screen.blit(i.image,(i.x,i.y))
        aero=[ground10,ground11,ground12,ground20,ground21,ground22] #LISTA COM OS CHAOS
        for i in aero:
            screen.blit(i.image,(i.x,i.y))

        floor=[]
        for i in groundRange:
            if i > 3000 and i <3400:
                continue
            else:
                chao = Blocks(i-addBg,430+char1.size[1],groundDEFAULT.image)
                floor.append(chao)
                screen.blit(chao.image,(i-addBg,430+(char1.size[1])))
        for i in enemies:
            if i.death == False:
                screen.blit(i.current_img,(i.x,i.y))
        for a in enemies:
            screen.blit(a.current_img,(a.x,a.y))
        endBlock = Blocks(map_x-pygame.Surface.get_width(char1.current_img)-addBg,400,endBlockIMG)
        screen.blit(endBlock.image,(endBlock.x,endBlock.y))
        screen.blit(char1.current_img,(char1.x,char1.y)) ### pintando o player
        for i in water_list:
            screen.blit(i.image,(i.x,i.y))
        for event in pygame.event.get(): #pegando as açoes do usuario
            if event.type == pygame.QUIT:
                running=False #saindo do jogo fechando a janela
                playLoop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.play(loops=-1)
                if event.key == pygame.K_ESCAPE:
                    running = False #saindo do jogo apertano esc
                    playLoop = False
                if event.key == pygame.K_SPACE and char1.jump==False:
                    jump.play()
                    char1.move("up")
                if event.key == pygame.K_y:
                    yodao()
                if event.key == pygame.K_w:
                    char1.move("look_up")
                if event.key == pygame.K_d:
                    char1.move("right")
                if event.key == pygame.K_a:
                    char1.move("left")
                if event.key == pygame.K_j:
                    char1.move("attack")
                    atk01.play()
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
        Game.update()
        if Game.goal(char1.hitbox,endBlock.rect) == True:
            diescreen = True
        while diescreen == True:
            screen.blit(diedIMG,(0,0))
            Game.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        diescreen = False
                        restart = True
                    if event.key == pygame.K_ESCAPE:
                        diescreen = False
                        running = False #saindo do jogo apertano esc
                        playLoop = False
                    if event.type == pygame.QUIT:
                        diescreen = False
                        running=False #saindo do jogo fechando a janela
                        playLoop = False
        if restart == True:
            running = False
            restart = False
    ############
pygame.quit() #fechando o pygame
quit() # fechandoo python
