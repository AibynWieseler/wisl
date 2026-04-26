import pygame
import math
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont(None, 24)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

current_color = BLACK
brush_size = 5

mode = "pencil"  #modes
drawing = False
start_pos = None
last_pos = None

text_input = "" #text
text_pos = None
typing = False

preview_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) #for shape preview

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= WIDTH or py < 0 or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px+1, py))
        stack.append((px-1, py))
        stack.append((px, py+1))
        stack.append((px, py-1))

running = True
while running:
    screen.blit(canvas, (0,0))
    preview_surface.fill((0,0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: #mouse down for drawing
            x, y = event.pos

            if mode == "fill":
                flood_fill(canvas, x, y, current_color)

            elif mode == "text":
                typing = True
                text_input = ""
                text_pos = event.pos

            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP: #mouse up for stopping drawing
            if not drawing:
                continue

            drawing = False
            end = event.pos

            x1, y1 = start_pos
            x2, y2 = end

            if mode == "line":
                pygame.draw.line(canvas, current_color, start_pos, end, brush_size)

            elif mode == "square":
                size = max(abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(canvas, current_color, (x1,y1,size,size), brush_size)

            elif mode == "rtriangle":
                points = [(x1,y1), (x2,y1), (x1,y2)]
                pygame.draw.polygon(canvas, current_color, points, brush_size)

            elif mode == "etriangle":
                side = math.dist(start_pos, end)
                height = side * (3**0.5) / 2
                p1 = (x1, y1)
                p2 = (x1 + side, y1)
                p3 = (x1 + side/2, y1 - height)
                pygame.draw.polygon(canvas, current_color, [p1,p2,p3], brush_size)

            elif mode == "rhombus":
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                dx = abs(x2-x1)//2
                dy = abs(y2-y1)//2
                points = [(cx, cy-dy), (cx+dx, cy), (cx, cy+dy), (cx-dx, cy)]
                pygame.draw.polygon(canvas, current_color, points, brush_size)

        if event.type == pygame.MOUSEMOTION: #mouse motion
            if drawing:
                if mode == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

                elif mode == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size*2)
                    last_pos = event.pos

            #preview line
            if drawing and mode == "line":
                pygame.draw.line(preview_surface, current_color, start_pos, event.pos, brush_size)

        if event.type == pygame.KEYDOWN: #keyboard controls

            # SAVE
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            elif typing: #text typing controls
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_input, True, current_color)
                    canvas.blit(text_surface, text_pos)
                    typing = False

                elif event.key == pygame.K_ESCAPE:
                    typing = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

            else:
                if event.key == pygame.K_p:
                    mode = "pencil"
                elif event.key == pygame.K_l:
                    mode = "line"
                elif event.key == pygame.K_f:
                    mode = "fill"
                elif event.key == pygame.K_t:
                    mode = "text"
                elif event.key == pygame.K_e:
                    mode = "eraser"
                elif event.key == pygame.K_s:
                    mode = "square"
                elif event.key == pygame.K_r:
                    mode = "rhombus"

                elif event.key == pygame.K_1: #color selection
                    current_color = BLACK
                elif event.key == pygame.K_2:
                    current_color = RED
                elif event.key == pygame.K_3:
                    current_color = GREEN
                elif event.key == pygame.K_4:
                    current_color = BLUE
                elif event.key == pygame.K_5:
                    current_color = YELLOW

                elif event.key == pygame.K_6: #brush size
                    brush_size = 2
                elif event.key == pygame.K_7:
                    brush_size = 5
                elif event.key == pygame.K_8:
                    brush_size = 10

    if typing and text_input: #text preview
        text_surface = font.render(text_input, True, current_color)
        screen.blit(text_surface, text_pos)

    screen.blit(preview_surface, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()