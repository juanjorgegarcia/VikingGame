import pygame
white = [255,255,255]
black = [0,0,0]
red = [255,0,0]
pygame.init()
game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption("A Tale of the Unworthy")
background=pygame.image.load("C:\\Users\\juanj\\OneDrive\\Documentos\\GitHub\\VikingGame\\8bitvapor.png")
pygame.display.update()
w,h=pygame.Surface.get_size(background)
game_exit = False
brect=pygame.Surface.get_rect(background)
lead_x=300
lead_y=300
lead_x_change = 0
lead_y_change = 0
clock = pygame.time.Clock()
char=pygame.image.load("C:\\Users\\juanj\\OneDrive\\Documentos\\GitHub\\VikingGame\\Images\\`PARADO.png")
crect=pygame.Surface.get_rect(char)
while not game_exit:
    game_display.blit(background,brect)
    #game_display.blit(char,(400,300))
    pygame.display.update()
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            game_exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -10
            if event.key == pygame.K_RIGHT:
                lead_x_change = 10
            if event.key == pygame.K_UP:
                lead_y_change= -10
            if event.key == pygame.K_DOWN:
                lead_y_change= +10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                lead_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                lead_y_change = 0
    lead_x += lead_x_change
    lead_y+= lead_y_change
    #game_display.fill(white)
    game_display.blit(char,(lead_x,lead_y))
    #pygame.draw.rect(game_display, black, [lead_x,lead_y,10,10])
    pygame.display.update()

    clock.tick(15)

pygame.quit()
quit()
