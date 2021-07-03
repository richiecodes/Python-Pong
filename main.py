import pygame, sys, random


def render_visuals():
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
    draw_scores()


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Top and bottom walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        pygame.mixer.Sound.play(wall_hit_sound, 0)

    # Ball collides with opponent wall
    if ball.left <= 0:
        player_score += 1
        pygame.mixer.Sound.play(score_sound, 0)
        score_time = pygame.time.get_ticks()

    # Ball collides with player wall
    if ball.right >= screen_width:
        opponent_score += 1
        pygame.mixer.Sound.play(score_sound, 0)
        score_time = pygame.time.get_ticks()

    # Ball collides with player paddle
    if ball.colliderect(player):
        ball_speed_x *= -1
        pygame.mixer.Sound.play(player_hit_sound, 0)

    # Ball collides with opponent paddle
    if ball.colliderect(opponent):
        ball_speed_x *= -1
        pygame.mixer.Sound.play(opponent_hit_sound, 0)


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed


def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_time < 700:
        number_three = timer_font.render("3", True, light_grey)
        screen.blit(number_three, (screen_width / 2 - 20, 300))
    if 700 < current_time - score_time < 1400:
        number_two = timer_font.render("2", True, light_grey)
        screen.blit(number_two, (screen_width / 2 - 20, 300))
    if 1400 < current_time - score_time < 2100:
        number_one = timer_font.render("1", True, light_grey)
        screen.blit(number_one, (screen_width / 2 - 20, 300))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def draw_scores():
    player_text = game_font.render(f"{player_score}", True, light_grey)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(opponent_text, (600, 470))


# Game Setup
pygame.init()
clock = pygame.time.Clock()
FPS = 60
game_font = pygame.font.SysFont("Arial", 30, True)
timer_font = pygame.font.SysFont("Arial", 60, True)

# Main Window
screen_width, screen_height = (1280, 960)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pongo")

# Game Rectangles
ball = pygame.Rect((screen_width / 2) - 15, (screen_height / 2) - 15, 30, 30)
player = pygame.Rect(screen_width - 20, (screen_height / 2) - 70, 10, 140)
opponent = pygame.Rect(10, (screen_height / 2) - 70, 10, 140)

# Game Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Game Sounds
wall_hit_sound = pygame.mixer.Sound('asset/wall-hit.wav')
player_hit_sound = pygame.mixer.Sound('asset/player-hit.wav')
opponent_hit_sound = pygame.mixer.Sound('asset/opponent-hit.wav')
score_sound = pygame.mixer.Sound('asset/score.wav')

# Game Physics
ball_speed_x = 7
ball_speed_y = 7
paddle_speed = 3
player_speed = 0
opponent_speed = 7

# Other Variables
player_score = 0
opponent_score = 0

score_time = True

# Game Loop
while True:
    # Handle Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed += 7
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed -= 7
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_speed += 7
    # Visuals
    ball_animation()
    player_animation()
    opponent_ai()
    render_visuals()

    if score_time:
        ball_start()

    # Updates
    pygame.display.flip()
    clock.tick(FPS)
