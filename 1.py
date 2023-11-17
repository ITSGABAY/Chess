import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_BACKSPACE, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9

# Constants
WIDTH, HEIGHT = 400, 200
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Persistent Variable Game")
clock = pygame.time.Clock()

# Global variables
persistent_variable = 0

font = pygame.font.Font(None, 36)
input_text = ""

def display_text():
    text_surface = font.render(f"Persistent Variable: {persistent_variable}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

def handle_events():
    global persistent_variable, input_text

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                try:
                    persistent_variable = int(input_text)
                except ValueError:
                    print("Invalid input. Please enter an integer.")
                input_text = ""
            elif event.key == K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                input_text += event.unicode

def run_game():
    global persistent_variable

    while True:
        handle_events()
        screen.fill((0, 0, 0))
        display_text()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run_game()
