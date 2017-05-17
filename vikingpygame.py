import pygame, os
from numpy import arange
pygame.init()

class Player:
	#classe para Player
	def __init__(self,x,y,sprite):
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
		self.colision = False # personagem nao esta colidindo
		self.hitbox = pygame.Rect(self.x,self.y,self.x+self.size[0],self.size[1]) #hitbox do personagem

	def load_images(self):
		self.walkingR_frames=[pygame.image.load("Images\\Player\\walk_right\\sprite_walkR0.png"),pygame.image.load("Images\\Player\\walk_right\\sprite_walkR1.png"),pygame.image.load("Images\\Player\\walk_right\\sprite_walkR2.png"),pygame.image.load("Images\\Player\\walk_right\\sprite_walkR3.png")]
		self.attacking_frames=[pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT0.png"),pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT1.png"),pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT2.png"),pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT3.png")]
		self.walkingR_frames=[pygame.image.load("Images\\Player\\WALK_RIGHT\\sprite_walkR0.png"),pygame.image.load("Images\\Player\\WALK_RIGHT\\sprite_walkR1.png"),pygame.image.load("Images\\Player\\WALK_RIGHT\\sprite_walkR2.png"),pygame.image.load("Images\\Player\\WALK_RIGHT\\sprite_walkR3.png")]
		self.attacking_frames=[pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT0.png"),pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT1.png"),pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT2.png"),pygame.image.load("Images\\Player\\ATTACK_RIGHT\\sprite_ATKRIGHT3.png")]
		self.walkingl_frames=[]
		self.attackingl_frames=[]

		for frame in self.walkingR_frames:
			self.walkingl_frames.append(pygame.transform.flip(frame,True,False))


	def animate(self):
		now=pygame.time.get_ticks()

		if self.look_up==True and self.walkR==False and self.walkL==False and self.jump==False:
			if self.rightface==True:
				self.current_img=pygame.transform.scale(pygame.image.load("Images\\Player\\CIMA_RIGHT\\cima.png"),(200,200))
			if self.leftface==True:
				self.current_img=pygame.transform.scale(pygame.image.load("Images\\Player\\CIMA_RIGHT\\cima.png"),(200,200))
				self.current_img = pygame.transform.flip(self.current_img, True, False)

		elif self.walkR==True and self.walkL==True and self.jump==False:
			if self.leftface==True:
				self.current_img=pygame.transform.scale(pygame.image.load("Images\\Player\\STAND_RIGHT\\stand.png"),(200,200))
				self.current_img = pygame.transform.flip(self.current_img, True, False)
			elif self.rightface==True:
				self.current_img=pygame.transform.scale(pygame.image.load("Images\\Player\\STAND_RIGHT\\stand.png"),(200,200))

		elif self.walkR==False and self.walkL==False and self.jump==False and self.attack==False:
			if self.leftface==True:
				self.current_img=pygame.transform.scale(pygame.image.load("Images\\Player\\STAND_RIGHT\\stand.png"),(200,200))
				self.current_img = pygame.transform.flip(self.current_img, True, False)
			if self.rightface==True:
				self.current_img=pygame.transform.scale(pygame.image.load("Images\\Player\\STAND_RIGHT\\stand.png"),(200,200))

		elif self.walkR==True and self.jump==False:
			if now - self.last_update>80:
				self.last_update=now
				self.current_frame=(self.current_frame+1)%len(self.walkingR_frames)
				self.current_img=self.walkingR_frames[self.current_frame]
				self.current_img=pygame.transform.scale(self.current_img,(200,200))

		elif self.walkL==True and self.jump==False:
			if now - self.last_update>80:
				self.last_update=now
				self.current_frame=(self.current_frame+1)%len(self.walkingl_frames)
				self.current_img=self.walkingl_frames[self.current_frame]
				self.current_img=pygame.transform.scale(self.current_img,(200,200))

		if self.attack==True:
			if now - self.last_update>80:
				self.attack==False
				self.last_update=now
				self.current_frame=(self.current_frame+1)%len(self.attacking_frames)
				self.current_img=self.attacking_frames[self.current_frame]
				self.current_img=pygame.transform.scale(self.current_img,(200,200))


	def move(self,direction):
		#movendo o player
		if direction == "left":
			self.speed_x = 10
			self.walkL=True #player esta andando para esquerda
			if self.jump==False:
				self.leftface=True
				self.rightface=False

		if direction == "right":
			self.speed_x = 10
			self.walkR=True #player esta andando para direita
			if self.jump==False:
				self.rightface=True
				self.leftface=False

		if direction=="stopright":
			self.walkR=False

		if direction=="stopleft":
			self.walkL=False
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
			self.aceleration = 0.4 #se o personagem estiver no ar a aceleraçao esta valendo!
			self.speed_y = -15 #+ self.aceleration
			self.jump = True #player esta pulando!


	def updatepos(self):
		global bgMoveRight, addBg
		#atualizando a posicao do player
		self.animate()
		self.speed_y+=self.aceleration
		#x, y = pygame.mouse.get_pos()
		#print(x,y)
		self.y += self.speed_y
		self.rect = self.current_img.get_rect(x=self.x,y=self.y)
		self.hitbox = pygame.Rect(self.x+70,self.y,60,192)
		#print(self.hitbox)
		#%print("X={},Y={} ".format(self.x,self.y))
		#print(ground.top)
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
			if self.x < screen_x/2:           
				self.x += self.speed_x
				addBgRight = False
			elif self.x >= screen_x/2 and self.x+addBg+pygame.Surface.get_width(self.current_img) <= map_x:
				addBgRight = True
				addBg = addBg + self.speed_x 

		if self.walkL == True:
			if self.x > 0 and addBg <= 0:
				self.x -= self.speed_x
				addBgLeft = False
			elif self.x > 0 and addBg > 0:
				addBgLeft = True
				addBg = addBg - self.speed_x

class Enemy(pygame.sprite.Sprite):
#     #classe para os minions/mobs
	def __init__(self,x,y,sprite):
		pygame.sprite.Sprite.__init__(self)
		self.x=x #coordenada x do personagem
		self.y=y #coordenada y do personagem
		self.current_frame=0
		self.last_update=0
		self.load_images()
		self.standimg=0
		self.current_img=sprite
		self.speed_x = 0 #velocidade no eixo x
		self.speed_y = 0 #velocidade no eixo x
		self.aceleration = + 0.4 #gravidade
		self.walkR = False #status do player andando para direita
		self.walkL = False #status do player andando para esquerda
		self.jump = False #status do player pulando
		self.rightface= False #sabaer pra onde o jogador esta olhando
		self.leftface = True
		self.look_up=False
		self.size = pygame.Surface.get_size(self.current_img) #retangulo equivalente a sprite
		self.rect = self.current_img.get_rect(x = self.x, y = self.y)
		self.colision = False # personagem nao esta colidindo
		self.hitbox = pygame.Rect(self.x,self.y,self.x+self.size[0],self.size[1]) #hitbox do personagem
		self.mask = pygame.mask.from_surface(self.current_img)

	def load_images(self):
		self.slimeL=[pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_1.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_2.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_3.png"),pygame.image.load("Images\\Inimigos\\Slime\\slime_4.png")]
		self.slimeR=[]

		for frame in self.slimeL:
			self.slimeR.append(pygame.transform.flip(frame,True,False))
	def animate(self):
		now=pygame.time.get_ticks()

		if self.leftface==True and self.rightface==False:
			if now - self.last_update>120:
				self.last_update=now
				self.current_frame=(self.current_frame+1)%len(self.slimeL)
				self.current_img=self.slimeL[self.current_frame]
				self.current_img=pygame.transform.scale(self.current_img,(100,100))

		elif self.rightface==True and self.leftface==False:
			if now - self.last_update>120:
				self.last_update=now
				self.current_frame=(self.current_frame+1)%len(self.slimeR)
				self.current_img=self.slimeR[self.current_frame]
				self.current_img=pygame.transform.scale(self.current_img,(100,100))





	def move(self,speed_x,speed_y):
		if self.x==1100:
			self.speed_x=-speed_x
			self.leftface=True
			self.rightface=False



		elif self.x == 0:
			self.speed_x=+speed_x
			self.rightface=True
			self.leftface=False

	def updatepos(self):
		self.animate()
		self.x+=self.speed_x
		self.y+=self.speed_y
		self.mask = pygame.mask.from_surface(self.current_img)
		self.rect = self.current_img.get_rect(x = self.x, y = self.y)



class Blocks():
	# classe para elementos estáticos do jogo

	def __init__(self,x,y,sprite):
		self.x = x
		self.xInicial = x
		self.y = y
		self.image = sprite
		self.width,self.height = pygame.Surface.get_size(self.image)
		self.rect = self.image.get_rect(x = self.x, y = self.y)
		#self.top = [[self.x,self.width + self.x],[self.y-char1.size[1],self.y-char1.size[1]]]


class Menu():
	#classe para o menu o jogo
	#devera conter funções como, start, savegame, highscore, creditos e customizaçao (posivelmente)
	pass


######
clock=pygame.time.Clock() #importando o timer
######
######
#char1=Player(400,400,player1)
map_x = 5000
map_y = 720
screen_x=1280
screen_y=720
screen=pygame.display.set_mode((screen_x,screen_y)) #criando o display do jogo
######
###### carregando o background Do jogo
vapor = pygame.image.load("8bitvapor.png").convert()
background = vapor #dando load
background = pygame.transform.scale(background, (screen_x, screen_y))  #escalano conforme a tela
background = background.convert() #covertenod os pixels da imagem (a imagem é carregada mais rapidamete)
bgMoveRight = False
addBg = 0 
addBgRight = False
addBgLeft = False
######

############ carregando as sprites do player
player1="Images\\Player\\STAND_RIGHT\\stand.png"
char1=Player(400,400,player1)
char_spritedata = {}
for i in range (3):
	name = "pwalkright{}".format(i)
	pwalkright = pygame.image.load("Images\\Player\\WALK_RIGHT\\sprite_walkR{}.png".format(i)).convert()
	pwalkright = pygame.transform.scale(pwalkright, (char1.size))
	char_spritedata[name] = pwalkright
####################
enemies = []
Slime1=pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png").convert()
slime11=pygame.transform.scale(Slime1,(100,100))

slime1=Enemy(1100,500,slime11)
enemies.append(slime1)
#################################
############
music1=pygame.mixer.music.load("Visager_-_02_-_Royal_Entrance.mp3")
############
kkkeae = pygame.image.load("kkkeaeman.jpg").convert()
############
ground0 = pygame.image.load("Images\\Plataforma\\chão\\ground_middle.png").convert()
ground0 = pygame.image.load("Images\\Plataforma\\CHÃO\\ground_middle.png").convert()
ground0 = pygame.transform.scale(ground0,(100,100)).convert()
groundRange = arange(0,map_x,pygame.Surface.get_width(ground0))

pygame.display.set_caption("A Tale of the Unworthy") #Titulo da janela do jogo
running=True
############
while running:
<<<<<<< HEAD
	screen.blit(background, (0, 0)) ### pintando o background
	ground1 = Blocks(800-addBg,450,ground0)
	ground2 = Blocks(800+ground1.width-addBg,450,ground0)
	floor=[ground1,ground2]
	for i in groundRange:
		chao = Blocks(i-addBg,390+char1.size[1],ground0)
		floor.append(chao)
		screen.blit(chao.image,(i-addBg,390+(char1.size[1])))
	for i in floor:
		screen.blit(i.image,(i.x,i.y))
	### pintando inimigos
	screen.blit(slime1.current_img,(slime1.x-addBg,slime1.y))
	### pintando o player
	screen.blit(char1.current_img,(char1.x,char1.y))
	pygame.display.update()### atualizando o display
	for event in pygame.event.get(): #pegando as açoes do usuario
		if event.type == pygame.QUIT:
			running=False #saindo do jogo fechando a janela
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_m:
				pygame.mixer.music.play(loops=1)
			if event.key == pygame.K_ESCAPE:
				running = False #saindo do jogo apertano esc
			if event.key == pygame.K_SPACE and char1.jump==False:
				char1.move("up")
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
			if event.key == pygame.K_j:
				char1.move("stop_attack")
	slime1.move(5,0)
	slime1.updatepos()
	char1.updatepos() ## atualizando a posicao do personagem
	screen.blit(pygame.image.load("Images\\Inimigos\\Slime\\slime_0.png"),(200,200))
	clock.tick(60) # ajustando o fps
=======
    screen.blit(background, (0, 0)) ### pintando o background
    screen.blit(ground.image,(ground.x,ground.y))
    floor=[ground]
    for i in groundRange:
        chao = Blocks(i,390+char1.size[1],ground.image)
        floor.append(chao)
        screen.blit(ground.image,(i,390+(char1.size[1])))
    screen.blit(char1.current_img,(char1.x,char1.y)) ### pintando o player
    screen.blit(slime1.current_img,(slime1.x,slime1.y))
    pygame.display.update()### atualizando o display
    for event in pygame.event.get(): #pegando as açoes do usuario
        if event.type == pygame.QUIT:
            running=False #saindo do jogo fechando a janela
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pygame.mixer.music.play(loops=1)
            if event.key == pygame.K_ESCAPE:
                running = False #saindo do jogo apertano esc
            if event.key == pygame.K_SPACE and char1.jump==False:
                char1.move("up")
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
            if event.key == pygame.K_j:
                char1.move("stop_attack")
            if event.key == pygame.K_k:
                background = vapor
                background = pygame.transform.scale(background, (screen_x, screen_y))

    slime1.move(5,0)
    slime1.update()
    char1.updatepos() ## atualizando a posicao do personagem
    floor=[ground]
    clock.tick(60) # ajustando o fps
>>>>>>> parent of 2ec747c... Codigo mais limpo
############
pygame.quit() #fechando o pygame
quit() # fechandoo python
