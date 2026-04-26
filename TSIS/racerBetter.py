import pygame
import random
import json

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

LANES = [60, 140, 220, 300]

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,200)
YELLOW = (255,255,0)

#json to load/save
def load_settings():
    try:
        return json.load(open("settings.json"))
    except:
        return {"sound": True, "difficulty": "normal", "color": "red"}

def save_settings():
    json.dump(settings, open("settings.json", "w"))

settings = load_settings()


def save_score(name, score, distance): 
    try:
        data = json.load(open("scores.json"))
    except:
        data = []

    data.append({"name": name, "score": score, "distance": int(distance)})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    json.dump(data, open("scores.json", "w"))

def load_scores():
    try:
        return json.load(open("scores.json"))
    except:
        return []


game_state = "menu"
username = ""

lane_index = 1 #player  model
player = pygame.Rect(LANES[lane_index]-20, 500, 40, 60)

lane_cooldown = 150
last_move_time = 0

def get_player_color():
    return {"red": RED, "blue": BLUE, "green": GREEN}[settings["color"]]

traffic = [] #objects
obstacles = []
powerups = []

base_speed = 5 
speed = base_speed

active_power = None #powerups
power_timer = 0
invincible_until = 0
lives = 1

coins_collected = 0
distance = 0

def safe_lane(): #enemies and whatnot
    return random.choice([l for l in LANES if abs(l - player.centerx) > 40])

def spawn_traffic():
    lane = safe_lane()
    traffic.append(pygame.Rect(lane-20, -60, 40, 60))

def spawn_obstacle():
    lane = safe_lane()
    kind = random.choice(["oil", "barrier", "boost"])
    obstacles.append([pygame.Rect(lane-15, -30, 30, 30), kind])

def spawn_powerup():
    lane = safe_lane()
    kind = random.choice(["nitro", "shield", "repair"])
    powerups.append([pygame.Rect(lane-15, -30, 30, 30), kind, pygame.time.get_ticks()])

def draw_text(text, x, y):
    screen.blit(font.render(text, True, BLACK), (x,y))

def draw_game(): #models
    screen.fill(WHITE)

    pygame.draw.rect(screen, get_player_color(), player)

    for e in traffic:
        pygame.draw.rect(screen, BLACK, e)

    for o in obstacles:
        color = BLUE if o[1]=="oil" else RED if o[1]=="barrier" else GREEN
        pygame.draw.rect(screen, color, o[0])

    for p in powerups:
        pygame.draw.circle(screen, YELLOW, p[0].center, 10)

    draw_text(f"score: {coins_collected*10 + int(distance)}", 10, 10)
    draw_text(f"dist: {int(distance)}", 10, 40)
    draw_text(f"lives: {lives}", 10, 70)

    if active_power:
        draw_text(f"power: {active_power}", 10, 100)

running = True
while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username = ""
                    game_state = "name"

        elif game_state == "name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #R to reset
                    traffic.clear() 
                    obstacles.clear()
                    powerups.clear()
                    distance = 0
                    lives = 1
                    active_power = None
                    game_state = "game"
                elif event.key == pygame.K_m:
                    game_state = "menu"

    if game_state == "game":

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and lane_index > 0: #movement
            if now - last_move_time > lane_cooldown:
                lane_index -= 1
                last_move_time = now

        if keys[pygame.K_RIGHT] and lane_index < len(LANES)-1:
            if now - last_move_time > lane_cooldown:
                lane_index += 1
                last_move_time = now

        target_x = LANES[lane_index]
        player.centerx += (target_x - player.centerx) * 0.2

        distance += 0.1

        if random.randint(1,30) == 1: #spawning
            spawn_traffic()
        if random.randint(1,60) == 1:
            spawn_obstacle()
        if random.randint(1,200) == 1:
            spawn_powerup()

        speed = base_speed #speed reset

        if active_power == "nitro": #nitro
            speed = base_speed * 2
            if now - power_timer > 4000:
                active_power = None

        for e in traffic: #incoming car movement
            e.y += speed
        for o in obstacles:
            o[0].y += speed
        for p in powerups:
            p[0].y += speed

        for e in traffic: #collisions
            if player.colliderect(e):
                if active_power == "shield":
                    active_power = None
                    invincible_until = now + 1000
                elif now > invincible_until:
                    if lives > 0:
                        lives -= 1
                        invincible_until = now + 1000
                    else:
                        save_score(username, coins_collected*10, distance)
                        game_state = "game_over"

        for o in obstacles:
            if player.colliderect(o[0]):
                if o[1] == "oil":
                    lane_index = random.randint(0,3)
                elif o[1] == "barrier":
                    game_state = "game_over"
                elif o[1] == "boost":
                    speed = base_speed * 2

        for p in powerups[:]:
            if player.colliderect(p[0]):
                active_power = p[1]
                power_timer = now
                powerups.remove(p)

                if active_power == "repair": #repair power
                    lives += 1
                    active_power = None

        traffic[:] = [e for e in traffic if e.y < HEIGHT]
        obstacles[:] = [o for o in obstacles if o[0].y < HEIGHT]
        powerups[:] = [p for p in powerups if p[0].y < HEIGHT and now - p[2] < 5000]

        #menu
    screen.fill(WHITE)

    if game_state == "menu":
        draw_text("Racer", 150, 200)
        draw_text("Press ENTER", 120, 250)

    elif game_state == "name":
        draw_text("Enter Name:", 120, 200)
        draw_text(username, 120, 250)

    elif game_state == "game":
        draw_game()

    elif game_state == "game_over":
        draw_text("GAME OVER", 130, 200)
        draw_text("R = Retry", 140, 250)
        draw_text("M = Menu", 140, 300)

    pygame.display.flip()

pygame.quit()