import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)

music_folder = os.path.join(os.path.dirname(__file__), "music")
playlist = [f for f in os.listdir(music_folder) if f.endswith(".mp3") or f.endswith(".wav")]

current_track = 0
playing = False
start_time = 0

def load_track(index):
    global start_time
    track_path = os.path.join(music_folder, playlist[index])
    pygame.mixer.music.load(track_path)
    start_time = pygame.time.get_ticks()

def play_music():
    global playing, start_time
    pygame.mixer.music.play()
    playing = True
    start_time = pygame.time.get_ticks()

def stop_music():
    global playing
    pygame.mixer.music.stop()
    playing = False

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    load_track(current_track)
    play_music()

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    load_track(current_track)
    play_music()

if playlist:
    load_track(current_track)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                play_music()
            elif event.key == pygame.K_s:  # Stop
                stop_music()
            elif event.key == pygame.K_n:  # Next
                next_track()
            elif event.key == pygame.K_b:  # Back
                prev_track()
            elif event.key == pygame.K_q:  # Quit
                running = False

    if playlist: #display current
        track_name = playlist[current_track]
    else:
        track_name = "No music found"

    text = font.render(f"Track: {track_name}", True, (255, 255, 255))
    screen.blit(text, (20, 50))

    if playing: #display playback
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
    else:
        elapsed = 0

    time_text = font.render(f"Time: {elapsed} sec", True, (200, 200, 200))
    screen.blit(time_text, (20, 100))

    controls = [
        "P - Play",
        "S - Stop",
        "N - Next",
        "B - Previous",
        "Q - Quit"
    ]

    for i, line in enumerate(controls):
        ctrl_text = font.render(line, True, (150, 150, 150))
        screen.blit(ctrl_text, (350, 50 + i * 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()