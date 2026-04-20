import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()


player = pygame.Rect(180, 500, 40, 60) #player's car
speed = 5

#incoming cars
enemies = []
for _ in range(3):
    enemies.append(pygame.Rect(random.randint(0, 360), random.randint(-600, -100), 40, 60))

enemy_speed = 5

coins = []
coin_size = 20

coin_count = 0 #score
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

running = True
game_over = False

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and game_over: #restart after crash
            if event.key == pygame.K_r:
                # Reset game
                player.x, player.y = 180, 500
                coin_count = 0
                coins.clear()
                enemies = [
                    pygame.Rect(random.randint(0, 360), random.randint(-600, -100), 40, 60)
                    for _ in range(3)
                ]
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed() #movement
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
            player.x += speed

        # Move enemies
        for enemy in enemies:
            enemy.y += enemy_speed

            if enemy.y > HEIGHT: #respawn incoming car
                enemy.y = random.randint(-200, -100)
                enemy.x = random.randint(0, WIDTH - 40)

            if player.colliderect(enemy): #collision
                game_over = True

        if random.randint(1, 50) == 1: #coin spawn
            coins.append(pygame.Rect(random.randint(0, WIDTH - coin_size), -20, coin_size, coin_size))

        for coin in coins: #coin movement
            coin.y += 4

        for coin in coins[:]: #coin collision
            if player.colliderect(coin):
                coins.remove(coin)
                coin_count += 1

    pygame.draw.rect(screen, RED, player) #player's car

    for enemy in enemies: #enemies
        pygame.draw.rect(screen, BLACK, enemy)

    for coin in coins: #coins
        pygame.draw.circle(screen, YELLOW, coin.center, coin_size // 2)

    score_text = font.render(f"Coins: {coin_count}", True, BLACK) #ui
    screen.blit(score_text, (WIDTH - 120, 10))

    if game_over:
        text = big_font.render("GAME OVER", True, RED) #game over text
        screen.blit(text, (70, 250))

        restart_text = font.render("Press R to restart", True, BLACK)
        screen.blit(restart_text, (110, 320))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()