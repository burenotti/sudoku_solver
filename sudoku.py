import pygame
import sys
import sudokum
import solver

pygame.init()

arr = [[" " for _ in range(9)] for _ in range(9)]


class Button:
    def __init__(self, width, height,
                 active_color=(170, 180, 185),
                 inactive_color=(130, 140, 150)):
        self.width = width
        self.height = height
        self.active_clr = active_color
        self.inactive_clr = inactive_color
        self.font = pygame.font.SysFont("Arial", 42)

    def draw(self, x: int, y: int, message: str, action=None):
        mouse = pygame.mouse.get_pos()

        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            pygame.draw.rect(screen, self.active_clr, (x, y, self.width, self.height))

            if pygame.event.get(pygame.MOUSEBUTTONUP):
                if action is not None:
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_clr, (x, y, self.width, self.height))

        text_render = self.font.render(message, True, (255, 255, 255))
        screen.blit(text_render, (x + 5, y - 5))

    def change_color(self, active_color, inactive_color):
        self.active_clr = active_color
        self.inactive_clr = inactive_color


WIDTH, HEIGHT = 500, 560
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font1 = pygame.font.SysFont("Arial", 19)
font2 = pygame.font.SysFont("Arial", 48)
font3 = pygame.font.SysFont("Arial", 42)


def draw_background():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(25, 25, 450, 450), 5)
    i = 1
    while (i * 50) < 450:
        line_width = 2 if i % 3 > 0 else 5
        pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2((i * 50) + 25, 25),
                         pygame.Vector2((i * 50) + 25, 470), line_width)
        pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(25, (i * 50) + 25),
                         pygame.Vector2(470, (i * 50) + 25), line_width)
        i += 1

    offset = 35
    for row in range(9):
        for col in range(9):
            output = arr[row][col]
            n_text = font2.render(str(output), True, pygame.Color('black'))
            screen.blit(n_text, pygame.Vector2((col * 50) + offset + 4, (row * 50) + offset - 11))


def write(color="Red"):
    text = font1.render("sudoku", True, pygame.Color(color))
    text_rect = text.get_rect(center=(WIDTH // 2, 12))
    screen.blit(text, text_rect)


def generator():
    global arr
    arr = sudokum.generate(mask_rate=0.7)
    for i in range(9):
        for j in range(9):
            if arr[i][j] == 0:
                arr[i][j] = " "


def generate_button_action():
    generator()
    offset = 35
    for row in range(9):
        for col in range(9):
            output = arr[row][col]
            n_text = font2.render(str(output), True, pygame.Color('black'))
            screen.blit(n_text, pygame.Vector2((col * 50) + offset + 4, (row * 50) + offset - 11))


def exit_button_action():
    pygame.quit()
    sys.exit()


def solve_button_action():
    solver.Sudoku(arr, 0, 0)
    pygame.display.flip()


def check_button_action():
    if not(solver.Check(arr)):
        check_button.change_color((200, 25, 25), (140, 30, 30))

    else:
        check_button.change_color((25, 200, 25), (30, 140, 30))


# Button(width, height, active_color, inactive_color)
# Creating buttons for exit, generate sudoku, solve sudoku
exit_button = Button(65, 45, (200, 25, 25), (140, 30, 30))
generate_button = Button(145, 45)
solve_button = Button(90, 45)
check_button = Button(100, 45)


def main():
    draw_background()
    write()
    exit_button.draw(410, 495, 'exit', exit_button_action)
    generate_button.draw(25, 495, 'generate', generate_button_action)
    solve_button.draw(190, 495, 'solve', solve_button_action)
    check_button.draw(300, 495, 'check', check_button_action)
    pygame.display.flip()


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    main()
