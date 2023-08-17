from os import environ, system
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from time import sleep
from sys import exit as sys_exit
from win32gui import SetWindowPos, SetForegroundWindow
import tkinter as tk

pygame.init()


# Set variables
try:
    end_win_score = int(input("Enter the score to win: "))

except Exception as e:
    if "invalid literal for int() with base 1" in str(e):
        print("Invalid input. Provide an integer as your input.")
        while True:
            try:
                end_win_score = int(input("Enter the score to win: "))
            except Exception as e:
                print("Invalid input. Provide an integer as your input.")
            else:
                break
    else:
        sys_exit("Sorry, there was an unexpected error.")

title = "Pong By Ryan Satur - v1.2.1"
pygame.display.set_caption(title)

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

width = 600
height = 600

font = pygame.font.SysFont("Arial", 48)

fps = 30

p_speed = 15
p_width = 25
p_height = 100
p1_x = 10
p1_y = height / 2 - p_height / 2
p2_x = width - p_width - 10
p2_y = height / 2 - p_height / 2
p1_score = 0
p2_score = 0

p1_u = False
p1_d = False
p2_u = False
p2_d = False

ball_x = width / 2
ball_y = height / 2
ball_width = 10
ball_x_vel = -15
ball_y_vel = 0

root = tk.Tk()
root.withdraw()

screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()


x = round((screen_w - width) / 2)
y = round((screen_h - height) / 2 * 0.8)

win = pygame.display.set_mode((width, height))
SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 1)


# Define functions and classes

# Define button


class Button:
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(
                win,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
            )

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("arial", 48)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2),
                ),
            )

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# Draw paddles, ball and score


def draw_obj():
    win.fill(black)
    global p1
    p1 = pygame.draw.rect(win, white, (p1_x, p1_y, p_width, p_height))
    global p2
    p2 = pygame.draw.rect(win, white, (p2_x, p2_y, p_width, p_height))
    global ball
    ball = pygame.draw.circle(win, white, (ball_x, ball_y), ball_width)
    score = font.render(str(p1_score) + " - " + str(p2_score), False, white)
    win.blit(score, (250, 30))


# Apply movement to paddles


def move_player():
    global p1_y, p2_y

    if p1_u:
        p1_y = max(p1_y - p_speed, 0)
    elif p1_d:
        p1_y = min(p1_y + p_speed, height)
    elif p2_u:
        p2_y = max(p2_y - p_speed, 0)
    elif p2_d:
        p2_y = min(p2_y + p_speed, height)


# Apply movement to ball


def move_ball():
    global ball_x, ball_y, ball_x_vel, ball_y_vel, p1_score, p2_score, p1_x, p2_x, p1_y, p2_y

    if (ball_x + ball_x_vel < p1_x + p_width) and (
        p1_y < ball_y + ball_y_vel + ball_width < p1_y + p_height
    ):
        pygame.mixer.music.load("sfx\paddle_hit.mp3")
        pygame.mixer.music.play()
        ball_x_vel = -ball_x_vel
        ball_y_vel = -((p1_y + p_height / 2 - ball_y) / 15)

    elif ball_x + ball_x_vel < 0:
        pygame.mixer.music.load("sfx\wall_hit.mp3")
        pygame.mixer.music.play()
        ball_x = width / 2
        ball_y = height / 2
        ball_x_vel = -ball_x_vel
        p2_score += 1
        p1_x = 10
        p1_y = height / 2 - p_height / 2
        p2_x = width - p_width - 10
        p2_y = height / 2 - p_height / 2
        sleep(0.25)

    if (ball_x + ball_x_vel > p2_x - p_width) and (
        p2_y < ball_y + ball_y_vel + ball_width < p2_y + p_height
    ):
        pygame.mixer.music.load("sfx\paddle_hit.mp3")
        pygame.mixer.music.play()
        ball_x_vel = -ball_x_vel
        ball_y_vel = -((p2_y + p_height / 2 - ball_y) / 15)

    elif ball_x + ball_x_vel > height:
        pygame.mixer.music.load("sfx\wall_hit.mp3")
        pygame.mixer.music.play()
        ball_x = width / 2
        ball_y = height / 2
        ball_x_vel = -ball_x_vel
        p1_score += 1
        p1_x = 10
        p1_y = height / 2 - p_height / 2
        p2_x = width - p_width - 10
        p2_y = height / 2 - p_height / 2
        sleep(0.25)

    if ball_y + ball_y_vel < 0 or ball_y + ball_y_vel > height:
        pygame.mixer.music.load("sfx\wall_hit.mp3")
        pygame.mixer.music.play()
        ball_y_vel = -ball_y_vel

    ball_x += ball_x_vel
    ball_y += ball_y_vel


win.fill(black)

pygame.display.flip()


# Main Game Loop

running = True

y_btn = Button(green, 80, 350, 150, 75, "Yes")
n_btn = Button(red, 400, 350, 150, 75, "No")


while running:
    exit_loop = False
    draw_obj()
    move_player()
    move_ball()
    pygame.display.flip()
    pygame.time.wait(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p1_u = True
                if p1.top == 0:
                    p1_u = False
            if event.key == pygame.K_s:
                p1_d = True
                if p1.bottom == height:
                    p1_d = False
            if event.key == pygame.K_UP:
                p2_u = True
                if p2.top == 0:
                    p2_u = False
            if event.key == pygame.K_DOWN:
                p2_d = True
                if p2.bottom == height:
                    p2_d = False
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1_u = False
            if event.key == pygame.K_s:
                p1_d = False
            if event.key == pygame.K_UP:
                p2_u = False
            if event.key == pygame.K_DOWN:
                p2_d = False

    win.fill(black)

    if p1.bottom == height:
        p1_d == False
    if p1.top == 0:
        p1_u == False
    if p2.bottom == height:
        p2_d == False
    if p2.top == 0:
        p2_u == False

    if p1_score == end_win_score:
        pygame.mixer.music.load("sfx\game_over.mp3")
        pygame.mixer.music.play()
        win.fill(black)
        while True:
            score_msg = font.render("Player 1 Wins! Play Again?", False, white)
            win.blit(score_msg, (20, 200))
            y_btn.draw(win)
            n_btn.draw(win)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if y_btn.isOver(pygame.mouse.get_pos()):
                        p1_x = 10
                        p1_y = height / 2 - p_height / 2
                        p2_x = width - p_width - 10
                        p2_y = height / 2 - p_height / 2
                        p1_score, p2_score = 0, 0
                        ball_x_vel = -15
                        ball_y_vel = 0
                        win.fill(black)
                        draw_obj()
                        move_player()
                        move_ball()
                        exit_loop = True
                        pygame.display.flip()
                        break
                    if n_btn.isOver(pygame.mouse.get_pos()):
                        running = False
                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
                    if event.key == pygame.K_y:
                        p1_x = 10
                        p1_y = height / 2 - p_height / 2
                        p2_x = width - p_width - 10
                        p2_y = height / 2 - p_height / 2
                        p1_score, p2_score = 0, 0
                        ball_x_vel = -15
                        ball_y_vel = 0
                        win.fill(black)
                        move_player()
                        move_ball()
                        draw_obj()
                        exit_loop = True
                        pygame.display.flip()
                        break
                    if event.key == pygame.K_n:
                        running = False
                        break
                if event.type == pygame.QUIT:
                    running = False
                    break
            if exit_loop:
                break
            if running == False:
                break
    if p2_score == end_win_score:
        pygame.mixer.music.load("sfx\game_over.mp3")
        pygame.mixer.music.play()
        win.fill(black)
        while True:
            score_msg = font.render("Player 2 Wins! Play Again?", False, white)
            win.blit(score_msg, (20, 200))
            y_btn.draw(win)
            n_btn.draw(win)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if y_btn.isOver(pygame.mouse.get_pos()):
                        p1_x = 10
                        p1_y = height / 2 - p_height / 2
                        p2_x = width - p_width - 10
                        p2_y = height / 2 - p_height / 2
                        p1_score, p2_score = 0, 0
                        ball_x_vel = -15
                        ball_y_vel = 0
                        win.fill(black)
                        move_player()
                        move_ball()
                        draw_obj()
                        exit_loop = True
                        pygame.display.flip()
                        break
                    if n_btn.isOver(pygame.mouse.get_pos()):
                        running = False
                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
                    if event.key == pygame.K_y:
                        p1_x = 10
                        p1_y = height / 2 - p_height / 2
                        p2_x = width - p_width - 10
                        p2_y = height / 2 - p_height / 2
                        p1_score, p2_score = 0, 0
                        ball_x_vel = -15
                        ball_y_vel = 0
                        win.fill(black)
                        move_player()
                        move_ball()
                        draw_obj()
                        exit_loop = True
                        pygame.display.flip()
                        break
                    if event.key == pygame.K_n:
                        running = False
                        break
                if event.type == pygame.QUIT:
                    running = False
                    break
            if exit_loop:
                break
            if running == False:
                break
