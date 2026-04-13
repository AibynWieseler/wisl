import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface((800, 600))
canvas.fill((255, 255, 255))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

color = BLACK
brush_size = 5
drawing = False
last_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                last_pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = pygame.mouse.get_pos()
                if last_pos:
                    pygame.draw.line(canvas, color, last_pos, current_pos, brush_size)
                last_pos = current_pos

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                color = RED
            elif event.key == pygame.K_g:
                color = GREEN
            elif event.key == pygame.K_b:
                color = BLUE
            elif event.key == pygame.K_k:
                color = BLACK
            elif event.key == pygame.K_w:
                color = WHITE
            elif event.key == pygame.K_c:
                canvas.fill(WHITE)

    screen.blit(canvas, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()