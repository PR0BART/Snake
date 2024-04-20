import pygame
import sys
import random
from config import BLACK, GREEN, YELLOW, RED, BLUE, WHITE, WIDTH, HEIGHT, BLOCK_SIZE, FPS, SCORE_PANEL_HEIGHT, TOTAL_HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
clock = pygame.time.Clock()

directions = {
    pygame.K_LEFT: 'LEFT',
    pygame.K_RIGHT: 'RIGHT',
    pygame.K_UP: 'UP',
    pygame.K_DOWN: 'DOWN'
}

snake = []
obstacles = []
score = 0
high_score = 0
food = None

def create_food():
    while True:
        food_position = (random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
                         random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE + SCORE_PANEL_HEIGHT)
        if food_position not in obstacles and food_position not in snake:
            return food_position

def add_obstacles(score):
    if score % 5 == 0:
        orientation = random.choice(['horizontal', 'vertical'])
        obstacle_length = random.choice([2, 3, 4])

        if orientation == 'horizontal':
            obstacle_x = random.randint(0, (WIDTH // BLOCK_SIZE) - obstacle_length) * BLOCK_SIZE
            obstacle_y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE + SCORE_PANEL_HEIGHT
            new_obstacle = [(obstacle_x + i * BLOCK_SIZE, obstacle_y) for i in range(obstacle_length)]
        else:
            obstacle_x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
            obstacle_y = random.randint(0, (HEIGHT // BLOCK_SIZE) - obstacle_length) * BLOCK_SIZE + SCORE_PANEL_HEIGHT
            new_obstacle = [(obstacle_x, obstacle_y + i * BLOCK_SIZE) for i in range(obstacle_length)]

        # Ensure that new obstacles do not overlap existing obstacles or snake parts
        if all(o not in obstacles and o not in snake for o in new_obstacle):
            obstacles.extend(new_obstacle)

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, pygame.Rect(obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))

def reset_game():
    global snake, obstacles, score, food, high_score
    snake = [(WIDTH // 2, HEIGHT // 2 + SCORE_PANEL_HEIGHT)]
    obstacles = []
    score = 0
    food = create_food()
    high_score = get_high_score()

def check_collision_with_obstacles(x, y):
    return (x, y) in obstacles

def get_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def update_high_score(new_score):
    global high_score
    if new_score > high_score:
        high_score = new_score
        with open("high_score.txt", "w") as f:
            f.write(str(new_score))

def draw_score():
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Score: {score}", True, WHITE)
    high_score_surface = font.render(f"High Score: {high_score}", True, WHITE)
    score_rect = score_surface.get_rect(topleft=(10, 10))
    high_score_rect = high_score_surface.get_rect(topright=(WIDTH - 10, 10))
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SCORE_PANEL_HEIGHT))
    screen.blit(score_surface, score_rect)
    screen.blit(high_score_surface, high_score_rect)

def run_game():
    global score, food
    reset_game()
    direction = 'RIGHT'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in directions:
                    new_direction = directions[event.key]
                    if (direction, new_direction) not in [('LEFT', 'RIGHT'), ('RIGHT', 'LEFT'), ('UP', 'DOWN'), ('DOWN', 'UP')]:
                        direction = new_direction

        x, y = snake[0]
        move_offsets = {'RIGHT': (BLOCK_SIZE, 0), 'LEFT': (-BLOCK_SIZE, 0), 'UP': (0, -BLOCK_SIZE), 'DOWN': (0, BLOCK_SIZE)}
        x += move_offsets[direction][0]
        y += move_offsets[direction][1]

        if (x, y) in snake[1:] or check_collision_with_obstacles(x, y) or x < 0 or x >= WIDTH or y < SCORE_PANEL_HEIGHT or y >= TOTAL_HEIGHT:
            break

        snake.insert(0, (x, y))
        if (x, y) == food:
            food = create_food()
            score += 1
            add_obstacles(score)
            update_high_score(score)
        else:
            snake.pop()

        screen.fill(GREEN)
        draw_score()
        draw_obstacles()
        for part in snake:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(part[0], part[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        clock.tick(FPS)

def show_menu():
    menu_font = pygame.font.Font(None, 48)
    play_text = menu_font.render('Play Game', True, WHITE)
    quit_text = menu_font.render('Quit Game', True, WHITE)
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                elif quit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.update()
    run_game()

if __name__ == "__main__":
    while True:
        show_menu()
