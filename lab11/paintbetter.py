import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

mode = "brush"   # brush, eraser, square, rtriangle, etriangle, rhombus
drawing = False
start_pos = None

running = True
while running:
    screen.blit(canvas, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP: #mouse up to draw figures
            drawing = False
            end = event.pos

            x1,y1 = start_pos
            x2,y2 = end

            if mode == "square":
                size = max(abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(canvas, current_color, (x1,y1,size,size), 2)

            elif mode == "rtriangle": #right triangle
                points = [(x1,y1), (x2,y1), (x1,y2)]
                pygame.draw.polygon(canvas, current_color, points, 2)

            elif mode == "etriangle": #equilateral triangle
                side = math.dist(start_pos, end)
                height = side * (3**0.5) / 2
                p1 = (x1, y1)
                p2 = (x1 + side, y1)
                p3 = (x1 + side/2, y1 - height)
                pygame.draw.polygon(canvas, current_color, [p1,p2,p3], 2)

            elif mode == "rhombus": #rhombus
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                dx = abs(x2-x1)//2
                dy = abs(y2-y1)//2
                points = [(cx, cy-dy), (cx+dx, cy), (cx, cy+dy), (cx-dx, cy)]
                pygame.draw.polygon(canvas, current_color, points, 2)

        if event.type == pygame.MOUSEMOTION and drawing: #drawing or eraser
            if mode == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, 5)

            elif mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, 12)

        if event.type == pygame.KEYDOWN: #controls
            if event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_x:
                mode = "eraser"
            elif event.key == pygame.K_s:
                mode = "square"
            elif event.key == pygame.K_t:
                mode = "rtriangle"
            elif event.key == pygame.K_e:
                mode = "etriangle"
            elif event.key == pygame.K_r:
                mode = "rhombus"
            elif event.key == pygame.K_1:
                current_color = BLACK
            elif event.key == pygame.K_2:
                current_color = RED
            elif event.key == pygame.K_3:
                current_color = GREEN
            elif event.key == pygame.K_4:
                current_color = BLUE
            elif event.key == pygame.K_5:
                current_color = YELLOW

    pygame.display.flip()
    clock.tick(60)

pygame.quit()