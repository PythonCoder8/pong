import pygame
import random
import time

pygame.mixer.pre_init(22050, -16, 2, 512)  # Lower frequency for faster processing
pygame.init()
pygame.font.init()

# Measurements
screen_width = 800
screen_height = 600

white = (255, 255, 255)
black = (0, 0, 0)

paddle_width = 15
paddle_height = 100

ball_size = 15


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

font = pygame.font.Font(r"fonts\Silkscreen-Regular.ttf", 74)
start_font = pygame.font.Font(r"fonts\Silkscreen-Regular.ttf", 30)

hit_sound = pygame.mixer.Sound(r"sfx\hit.wav")
score_sound = pygame.mixer.Sound(r"sfx\score.mp3")
bob = pygame.mixer.Sound(r"sfx\bob.wav")

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, paddle_width, paddle_height)
        self.speed = 6

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

class Ball:
    def __init__(self, x, y, speed=20):
        self.rect = pygame.Rect(x, y, ball_size, ball_size)
        self.speed_x = speed * random.choice((1, -1))
        self.speed_y = speed * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            hit_sound.play()
            self.speed_y *= -1

    def draw(self):
        if self.rect:
            pygame.draw.ellipse(screen, white, self.rect)

    def hide(self):
        self.rect = None

def start_screen():
    screen.fill(black)
    start_text = start_font.render("Press SPACEBAR to start", True, white)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_loop(ball_speed=5.3):
    clock = pygame.time.Clock()
    running = True

    player_start_x = screen_width - 20
    player_start_y = screen_height // 2 - paddle_height // 2
    opponent_start_x = 10
    opponent_start_y = screen_height // 2 - paddle_height // 2

    player = Paddle(player_start_x, player_start_y)
    opponent = Paddle(opponent_start_x, opponent_start_y)
    min_ball_speed = 1
    ball = Ball(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, speed=ball_speed)

    player_score = 0
    opponent_score = 0
    winning_score = 11

    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.move(up=True)
        if keys[pygame.K_DOWN] and player.rect.bottom < screen_height:
            player.move(up=False)
        if keys[pygame.K_w] and opponent.rect.top > 0:
            opponent.move(up=True)
        if keys[pygame.K_s] and opponent.rect.bottom < screen_height:
            opponent.move(up=False)

        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            ball_speed += 0.2
        if keys[pygame.K_MINUS] and ball_speed > min_ball_speed:
            ball_speed -= 0.2

        ball.speed_x = ball_speed * (1 if ball.speed_x > 0 else -1)
        ball.speed_y = ball_speed * (1 if ball.speed_y > 0 else -1)

        ball.move()

        if ball.rect.left <= 0:
            score_sound.play()
            player_score += 1
            ball.hide()
            if player_score < winning_score:
                countdown_to_next_round()
            ball = Ball(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, speed=ball_speed)
            player = Paddle(player_start_x, player_start_y)
            opponent = Paddle(opponent_start_x, opponent_start_y)

        if ball.rect.right >= screen_width:
            score_sound.play()
            opponent_score += 1
            ball.hide()
            if opponent_score < winning_score:
                countdown_to_next_round()
            ball = Ball(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, speed=ball_speed)
            player = Paddle(player_start_x, player_start_y)
            opponent = Paddle(opponent_start_x, opponent_start_y)

        if ball.rect and (ball.rect.colliderect(player.rect) or ball.rect.colliderect(opponent.rect)):
            hit_sound.play()
            ball.speed_x *= -1

        if player_score == winning_score or opponent_score == winning_score:
            bob.play()
            winner_text = "Player 2 Wins!" if player_score == winning_score else "Player 1 Wins!"
            display_winner(winner_text, ball_speed)
            running = False

        screen.fill(black)
        player.draw()
        opponent.draw()
        ball.draw()

        player_text = font.render(str(player_score), True, white)
        opponent_text = font.render(str(opponent_score), True, white)
        screen.blit(player_text, (screen_width - 100, 10))
        screen.blit(opponent_text, (50, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def countdown_to_next_round():
    for i in range(3, 0, -1):
        screen.fill(black)
        countdown_text = font.render(f"Next Round in {i}", True, white)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

def display_winner(winner_text, ball_speed):
    screen.fill(black)
    text = font.render(winner_text, True, white)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)

    option_font = pygame.font.Font(r"fonts\Silkscreen-Regular.ttf", 20)
    play_again_text = option_font.render("Press R to Play Again or Q to Quit", True, white)
    screen.blit(play_again_text, (screen_width // 2 - play_again_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    bob.stop()
                    game_loop(ball_speed)
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    bob.stop()
                    waiting_for_input = False

if __name__ == "__main__":
    start_screen()
    game_loop()
