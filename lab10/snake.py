import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)

snake = [(100, 100)] #snake body
dx, dy = 20, 0
block = 20

def generate_food(): #apple
    while True:
        x = random.randrange(0, WIDTH, block)
        y = random.randrange(0, HEIGHT, block)
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

score = 0
level = 1
speed = 5

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    keys = pygame.key.get_pressed() #controls
    if keys[pygame.K_UP]:
        dx, dy = 0, -block
    if keys[pygame.K_DOWN]:
        dx, dy = 0, block
    if keys[pygame.K_LEFT]:
        dx, dy = -block, 0
    if keys[pygame.K_RIGHT]:
        dx, dy = block, 0

    head = (snake[0][0] + dx, snake[0][1] + dy) #snake movement

    if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT): #border collision - leave screen
        print("Game Over")
        running = False

    if head in snake: #self collision
        print("Game Over")
        running = False

    snake.insert(0, head)

    if head == food: #food collision
        score += 1
        food = generate_food()

        if score % 3 == 0: #levels
            level += 1
            speed += 2
    else:
        snake.pop()

    for segment in snake: #snake drawing
        pygame.draw.rect(screen, GREEN, (*segment, block, block))

    # Draw food
    pygame.draw.rect(screen, RED, (*food, block, block))

    # UI
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, BLACK), (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()