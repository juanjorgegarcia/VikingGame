import pygame
white = [255,255,255]
black = [0,0,0]
red = [255,0,0]
pygame.init()
game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption("A Tale of the Unworthy")

pygame.display.update()

game_exit = False

lead_x=300
lead_y=300
lead_x_change = 0
lead_y_change = 0
clock = pygame.time.Clock()


while not game_exit:
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
    game_display.fill(white)
    pygame.draw.rect(game_display, black, [lead_x,lead_y,10,10])
    pygame.display.update()

    clock.tick(15)

pygame.quit()
quit()
