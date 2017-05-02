import pygame
white = [255,255,255]
pygame.init()

game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption("A Tale of the Unworthy")

pygame.display.update()

game_exit = True

while game_exit:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            game_exit = False
        game_display.fill(white)
        pygame.display.update()
pygame.quit()
quit()
