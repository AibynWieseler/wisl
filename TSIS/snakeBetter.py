import pygame
import random
import json
import psycopg2

pygame.init()
WIDTH, HEIGHT = 600, 400
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLUE = (0,0,255)
PURPLE = (150,0,150)
BLACK = (0,0,0)

conn = psycopg2.connect( #database
    dbname="postgres",
    user="postgres",
    password="1939",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE username=%s", (name,))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (name,))
    conn.commit()
    return cur.fetchone()[0]

def save_score(player_id, score, level):
    cur.execute(
        "INSERT INTO game_sessions(player_id,score,level) VALUES(%s,%s,%s)",
        (player_id, score, level)
    )
    conn.commit()

def get_top_scores():
    cur.execute("""
        SELECT p.username, g.score, g.level
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC LIMIT 10
    """)
    return cur.fetchall()

def get_best(player_id):
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id=%s", (player_id,))
    r = cur.fetchone()
    return r[0] or 0

#json for leaderboard
def load_settings():
    try:
        return json.load(open("settings.json"))
    except:
        return {"color":[0,200,0], "grid":True}

def save_settings():
    json.dump(settings, open("settings.json","w"))

settings = load_settings()

state = "menu"
username = ""
player_id = None

#game
def reset_game():
    global snake, dx, dy, score, level, obstacles
    snake = [(100,100)]
    dx, dy = BLOCK, 0
    score = 0
    level = 1
    obstacles = []

reset_game()

def spawn_food():
    while True:
        x = random.randrange(0, WIDTH, BLOCK)
        y = random.randrange(0, HEIGHT, BLOCK)
        if (x,y) not in snake and (x,y) not in obstacles:
            return {"pos":(x,y),"type":"normal"}

def spawn_poison():
    return {"pos":(random.randrange(0,WIDTH,BLOCK),
                   random.randrange(0,HEIGHT,BLOCK)),
            "type":"poison"}

def spawn_power():
    kind = random.choice(["speed","slow","shield"])
    return {"pos":(random.randrange(0,WIDTH,BLOCK),
                   random.randrange(0,HEIGHT,BLOCK)),
            "type":kind,
            "timer":pygame.time.get_ticks()}

food = spawn_food()
poison = spawn_poison()
power = None

active_power = None
power_time = 0
shield_used = False

#obstacles
def generate_obstacles():
    global obstacles
    obstacles = []
    for _ in range(level):
        x = random.randrange(0, WIDTH, BLOCK)
        y = random.randrange(0, HEIGHT, BLOCK)
        if (x,y) not in snake:
            obstacles.append((x,y))

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu": #ui
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = "name"
                elif event.key == pygame.K_l:
                    state = "leaderboard"
                elif event.key == pygame.K_s:
                    state = "settings"

        elif state == "name": #name input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_id = get_or_create_player(username)
                    best = get_best(player_id)
                    reset_game()
                    state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        elif state == "settings": #settings for grid and color
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]
                elif event.key == pygame.K_c:
                    settings["color"] = [random.randint(0,255) for _ in range(3)]
                elif event.key == pygame.K_ESCAPE:
                    save_settings()
                    state = "menu"

        elif state == "game_over": #reset
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    state = "game"
                elif event.key == pygame.K_m:
                    state = "menu"

    if state == "game":

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: dx,dy = 0,-BLOCK
        if keys[pygame.K_DOWN]: dx,dy = 0,BLOCK
        if keys[pygame.K_LEFT]: dx,dy = -BLOCK,0
        if keys[pygame.K_RIGHT]: dx,dy = BLOCK,0

        head = (snake[0][0]+dx, snake[0][1]+dy)

        if head in snake or head in obstacles or not (0<=head[0]<WIDTH and 0<=head[1]<HEIGHT): #collision
            if active_power == "shield" and not shield_used:
                shield_used = True
            else:
                save_score(player_id, score, level)
                state = "game_over"

        snake.insert(0, head)

        if head == food["pos"]: #food spawn
            score += 1
            food = spawn_food()
        else:
            snake.pop()

        if head == poison["pos"]: #poison spawn
            snake = snake[:-2]
            poison = spawn_poison()
            if len(snake) <= 1:
                state = "game_over"

        if power and head == power["pos"]: #powers
            active_power = power["type"]
            power_time = pygame.time.get_ticks()
            shield_used = False
            power = None

        if not power and random.randint(1,200)==1: #powers spawn
            power = spawn_power()

        now = pygame.time.get_ticks()
        if active_power in ["speed","slow"] and now - power_time > 5000: #timer for powers
            active_power = None

        if score % 5 == 0 and score > 0:
            level = score // 5 + 1
            if level >= 3:
                generate_obstacles()

        for s in snake: #snake, etc model
            pygame.draw.rect(screen, settings["color"], (*s,BLOCK,BLOCK))

        pygame.draw.rect(screen, RED, (*food["pos"],BLOCK,BLOCK))
        pygame.draw.rect(screen, (150,0,0), (*poison["pos"],BLOCK,BLOCK))

        if power:
            pygame.draw.rect(screen, BLUE, (*power["pos"],BLOCK,BLOCK))

        for o in obstacles:
            pygame.draw.rect(screen, BLACK, (*o,BLOCK,BLOCK))

        screen.blit(font.render(f"Score:{score}",True,BLACK),(10,10))
        screen.blit(font.render(f"Level:{level}",True,BLACK),(10,30))

    elif state == "menu": #ui
        screen.blit(font.render("SNAKE++",True,BLACK),(250,100))
        screen.blit(font.render("ENTER - Play",True,BLACK),(200,150))
        screen.blit(font.render("L - Leaderboard",True,BLACK),(200,200))

    elif state == "name":
        screen.blit(font.render("Enter Name:",True,BLACK),(200,150))
        screen.blit(font.render(username,True,BLACK),(200,200))

    elif state == "leaderboard":
        scores = get_top_scores()
        y = 100
        for i,s in enumerate(scores):
            screen.blit(font.render(f"{i+1}. {s[0]} {s[1]}",True,BLACK),(150,y))
            y += 30

    elif state == "settings":
        screen.blit(font.render("Settings",True,BLACK),(250,100))
        screen.blit(font.render("G - Toggle Grid",True,BLACK),(200,150))
        screen.blit(font.render("C - Change Color",True,BLACK),(200,200))

    elif state == "game_over":
        screen.blit(font.render("GAME OVER",True,BLACK),(250,150))
        screen.blit(font.render("R - Retry",True,BLACK),(250,200))
        screen.blit(font.render("M - Menu",True,BLACK),(250,250))

    pygame.display.flip()

    speed = 8 #speed with boosts
    if active_power == "speed":
        speed = 12
    elif active_power == "slow":
        speed = 4

    clock.tick(speed)

pygame.quit()
conn.close()