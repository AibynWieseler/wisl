import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255,255,255)
RED = (200,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GOLD = (255,215,0)
BLUE = (0,0,255)

clock = pygame.time.Clock()

player = pygame.Rect(180, 500, 40, 60)
speed = 5

enemies = [pygame.Rect(random.randint(0,360), random.randint(-600,-100), 40,60) for _ in range(3)]
enemy_speed = 5

coins = []

coins_collected = 0
font = pygame.font.SysFont(None, 30)

LEVEL_UP = 5  #increase speed every 5 coins

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() #movement
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += speed

    for enemy in enemies: #enemy movement
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy.y = random.randint(-200, -100)
            enemy.x = random.randint(0, WIDTH - 40)

        if player.colliderect(enemy): #collision
            running = False

    if random.randint(1, 40) == 1: #weight coins
        x = random.randint(0, WIDTH-20)
        y = -20

        value = random.choice([1, 2, 3]) #diff coins
        if value == 1:
            color = YELLOW
        elif value == 2:
            color = BLUE
        else:
            color = GOLD

        coins.append([pygame.Rect(x, y, 20, 20), value, color])

    for coin in coins: #coin spawn
        coin[0].y += 4

    for coin in coins[:]: #coin collection
        if player.colliderect(coin[0]):
            coins_collected += coin[1]
            coins.remove(coin)

            # 🚀 Increase difficulty
            if coins_collected % LEVEL_UP == 0:
                enemy_speed += 1

    pygame.draw.rect(screen, RED, player)

    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, enemy)

    for coin in coins:
        pygame.draw.circle(screen, coin[2], coin[0].center, 10)

    text = font.render(f"Coins: {coins_collected}", True, BLACK) #ui
    screen.blit(text, (WIDTH-130, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()