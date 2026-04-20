import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]
current_color = (0,0,0)

drawing = False
mode = "brush"  # brush, rect,circle,eraser

start_pos = None

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))

running = True
while running:
    screen.blit(canvas, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: #mouse controls
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                pygame.draw.rect(canvas, current_color,
                                 (*start_pos,
                                  end_pos[0]-start_pos[0],
                                  end_pos[1]-start_pos[1]))

            if mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, current_color, start_pos, radius)

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, 5)
            elif mode == "eraser":
                pygame.draw.circle(canvas, (255,255,255), event.pos, 10)

        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_b:
                mode = "brush"
            if event.key == pygame.K_r:
                mode = "rect"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_e:
                mode = "eraser"

            if event.key == pygame.K_1: #color change
                current_color = colors[0]
            if event.key == pygame.K_2:
                current_color = colors[1]
            if event.key == pygame.K_3:
                current_color = colors[2]
            if event.key == pygame.K_4:
                current_color = colors[3]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()