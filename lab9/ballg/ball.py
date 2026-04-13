import pygame
pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("ball game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

radius = 25 #ball
x = 600 // 2
y = 400 // 2
step = 20
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #movement
            if event.key == pygame.K_LEFT:
                if x - step - radius >= 0:
                    x -= step

            elif event.key == pygame.K_RIGHT:
                if x + step + radius <= 600:
                    x += step

            elif event.key == pygame.K_UP:
                if y - step - radius >= 0:
                    y -= step

            elif event.key == pygame.K_DOWN:
                if y + step + radius <= 400:
                    y += step

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)
    pygame.display.flip()

pygame.quit()