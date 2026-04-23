import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

clock = pygame.time.Clock()

block = 20

snake = [(100,100)]
dx, dy = block, 0

def generate_food(): #generate food with timer
    while True:
        x = random.randrange(0, WIDTH, block)
        y = random.randrange(0, HEIGHT, block)
        if (x,y) not in snake:
            value = random.choice([1,2,3])
            timer = pygame.time.get_ticks() + 5000  # 5 seconds
            return {"pos": (x,y), "value": value, "timer": timer}

food = generate_food()

score = 0
font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() #controls
    if keys[pygame.K_UP]: dx,dy = 0,-block
    if keys[pygame.K_DOWN]: dx,dy = 0,block
    if keys[pygame.K_LEFT]: dx,dy = -block,0
    if keys[pygame.K_RIGHT]: dx,dy = block,0

    head = (snake[0][0]+dx, snake[0][1]+dy) #snake movement

    if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT): #collision with walls
        running = False

    if head in snake:
        running = False

    snake.insert(0, head)

    if pygame.time.get_ticks() > food["timer"]: #food timer
        food = generate_food()

    if head == food["pos"]:
        score += food["value"]
        food = generate_food()
    else:
        snake.pop()

    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, block, block))

    if food["value"] == 1:
        color = RED
    elif food["value"] == 2:
        color = BLUE
    else:
        color = (255,215,0) #weight coloured food

    pygame.draw.rect(screen, color, (*food["pos"], block, block))

    screen.blit(font.render(f"Score: {score}", True, BLACK), (10,10))

    pygame.display.flip()
    clock.tick(8)

pygame.quit()