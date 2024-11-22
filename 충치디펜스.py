import pygame
import random
import sys

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("충치디펜스")

pygame.mixer.music.load("C:/Users/pd pc1/deepprogram/bgm.mp3")
pygame.mixer.music.play(-1)

# 이미지 로드 (원시 문자열 사용)
backgrounds = [
    pygame.image.load("C:/Users/pd pc1/deepprogram/background1.jpg"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/background2.jpg"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/background3.jpg")
]
start_background = pygame.image.load("C:/Users/pd pc1/deepprogram/start.jpg")
game_over_background = pygame.image.load("C:/Users/pd pc1/deepprogram/gameover.jpg")
character_images = [
    pygame.image.load("C:/Users/pd pc1/deepprogram/character1.png"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/character2.png"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/character3.png")
]
bomb_images = [
    pygame.image.load("C:/Users/pd pc1/deepprogram/bomb1.png"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/bomb2.png"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/bomb3.png"),
    pygame.image.load("C:/Users/pd pc1/deepprogram/bomb4.png")
]

# 플레이어 설정
player_size = character_images[0].get_rect().size
player_width = player_size[0]
player_height = player_size[1]
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_height]

# 폭탄 설정
bomb_size = bomb_images[0].get_rect().size
bomb_width = bomb_size[0]
bomb_height = bomb_size[1]
bomb_list = [[random.randint(0, SCREEN_WIDTH - bomb_width), 0, random.choice(bomb_images)]]

# 속도 설정
bomb_speed = 10
player_speed = 10

# 시계 설정
clock = pygame.time.Clock()

# 폰트 설정
font_path = pygame.font.match_font('malgun gothic')  # 한글 폰트 설정
font = pygame.font.Font(font_path, 35)
small_font = pygame.font.Font(font_path, 25)

# 배경 이미지 인덱스 초기화
current_background = 0

def drop_bombs(bomb_list):
    delay = random.random()
    if len(bomb_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - bomb_width)
        y_pos = 0
        bomb_list.append([x_pos, y_pos, random.choice(bomb_images)])

def draw_bombs(bomb_list):
    for bomb_pos in bomb_list:
        screen.blit(bomb_pos[2], (bomb_pos[0], bomb_pos[1]))

def update_bomb_positions(bomb_list, score):
    for idx, bomb_pos in enumerate(bomb_list):
        if bomb_pos[1] >= 0 and bomb_pos[1] < SCREEN_HEIGHT:
            bomb_pos[1] += bomb_speed
        else:
            bomb_list.pop(idx)
            score += 1
    return score

def collision_check(bomb_list, player_pos):
    for bomb_pos in bomb_list:
        if detect_collision(bomb_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, bomb_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    b_x = bomb_pos[0]
    b_y = bomb_pos[1]

    if (b_x >= p_x and b_x < (p_x + player_width)) or (p_x >= b_x and p_x < (b_x + bomb_width)):
        if (b_y >= p_y and b_y < (p_y + player_height)) or (p_y >= b_y and p_y < (b_y + bomb_height)):
            return True
    return False

def game_over_screen(score):
    screen.blit(game_over_background, (0, 0))
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render("Score: {}".format(score), True, WHITE, BLACK)
    advice_text = small_font.render("양치를 열심히 합시다!", True, BLACK)
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, BLACK)

    # 텍스트 높이 계산
    game_over_height = game_over_text.get_height()
    score_height = score_text.get_height()
    restart_height = restart_text.get_height()
    advice_height = advice_text.get_height()

    # 화면 중앙에 배치하기 위한 Y 좌표 계산
    y_position = SCREEN_HEIGHT // 2 - (game_over_height + score_height + restart_height + advice_height + 100) // 2 - 80

    # 각 텍스트를 계산된 위치에 출력
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, y_position))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_position + game_over_height + 30))
    screen.blit(advice_text, (SCREEN_WIDTH // 2 - advice_text.get_width() // 2, y_position + game_over_height + 30 + score_height))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, y_position + game_over_height + 30 + score_height + advice_height))

    pygame.display.update()

def start_screen():
    screen.blit(start_background, (0, 0))
    BLUE = (0, 0, 255)
    title_text = font.render("충치디펜스", True, BLUE, BLACK)
    play_text = small_font.render("Press any key to Play", True, WHITE, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 50))
    screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT // 2 - play_text.get_height() // 2 + 50))
    pygame.display.update()

# 게임 루프
while True:
    start_screen()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

    game_over = False
    score = 0
    lives = 3  # 캐릭터의 목숨
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_height]
    bomb_list = [[random.randint(0, SCREEN_WIDTH - bomb_width), 0, random.choice(bomb_images)]]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_width:
            player_pos[0] += player_speed

        screen.blit(backgrounds[current_background], (0, 0))  # 현재 배경 이미지로 초기화

        drop_bombs(bomb_list)
        score = update_bomb_positions(bomb_list, score)

        text = font.render("Score: {}".format(score), 1, WHITE)
        screen.blit(text, (10, 10))

        # lives 텍스트는 배경 없이 출력
        lives_text = font.render("Lives: {}".format(lives), 1, RED)
        screen.blit(lives_text, (10, 50))

        if collision_check(bomb_list, player_pos):
            lives -= 1
            if lives == 0:
                game_over = True
                current_background = len(backgrounds) - 1  # 마지막 배경으로 설정
            else:
                current_background = (current_background + 1) % len(backgrounds)  # 다음 배경 이미지로 순환
                bomb_list = [[random.randint(0, SCREEN_WIDTH - bomb_width), 0, random.choice(bomb_images)]]  # 충돌 시 폭탄 초기화

        draw_bombs(bomb_list)

        # 목숨에 따라 다른 캐릭터 이미지 사용
        if lives >= 1:
            screen.blit(character_images[3 - lives], (player_pos[0], player_pos[1]))

        pygame.display.update()

        clock.tick(30)

    game_over_screen(score)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            game_over = False
            current_background = 0  # 게임 재시작 시 첫 번째 배경으로 초기화
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()