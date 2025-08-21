import pygame, random, sys

# --- Settings ---
WIDTH, HEIGHT = 640, 480
TILE = 20
FPS = 12  # snake speed (increase for harder)

# Colors (R,G,B)
BG = (20, 20, 24)
GRID = (36, 36, 42)
SNAKE = (60, 200, 80)
HEAD = (80, 230, 110)
FOOD = (220, 70, 70)
TEXT = (230, 230, 235)

def draw_grid(surf):
    for x in range(0, WIDTH, TILE):
        pygame.draw.line(surf, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(surf, GRID, (0, y), (WIDTH, y))

def spawn_food(snake):
    cols = WIDTH // TILE
    rows = HEIGHT // TILE
    empty = {(x, y) for x in range(cols) for y in range(rows)} - set(snake)
    if not empty:
        return None  # board filled (win)
    return random.choice(list(empty))

def move(snake, direction):
    dx, dy = direction
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)
    return new_head

def out_of_bounds(cell):
    x, y = cell
    return x < 0 or y < 0 or x >= WIDTH // TILE or y >= HEIGHT // TILE

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake (pygame)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    big = pygame.font.SysFont(None, 48)

    def reset():
        start = (WIDTH // TILE // 2, HEIGHT // TILE // 2)
        snake = [start, (start[0]-1, start[1]), (start[0]-2, start[1])]
        direction = (1, 0)  # moving right
        food = spawn_food(snake)
        score = 0
        paused = False
        return snake, direction, food, score, paused

    snake, direction, food, score, paused = reset()

    def draw():
        screen.fill(BG)
        draw_grid(screen)

        # food
        if food is not None:
            fx, fy = food
            pygame.draw.rect(screen, FOOD, (fx*TILE, fy*TILE, TILE, TILE))

        # snake
        for i, (x, y) in enumerate(snake):
            color = HEAD if i == 0 else SNAKE
            pygame.draw.rect(screen, color, (x*TILE, y*TILE, TILE, TILE))

        # HUD
        hud = font.render(f"Score: {score}", True, TEXT)
        screen.blit(hud, (10, 8))

        pygame.display.flip()

    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if not game_over:
                    # avoid reversing directly
                    if e.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif e.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif e.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif e.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)
                    elif e.key == pygame.K_p:
                        paused = not paused
                else:
                    if e.key == pygame.K_r:
                        snake, direction, food, score, paused = reset()
                        game_over = False

        if not running:
            break

        if game_over or paused:
            if game_over:
                # Draw game over overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 140))
                screen.blit(overlay, (0, 0))
                text1 = big.render("GAME OVER", True, TEXT)
                text2 = font.render("Press R to restart, ESC to quit", True, TEXT)
                screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 40))
                screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 10))
                pygame.display.flip()
            else:
                # paused
                pause = font.render("Paused (P to resume)", True, TEXT)
                screen.blit(pause, (WIDTH//2 - pause.get_width()//2, HEIGHT//2 - 10))
                pygame.display.flip()
            continue

        # advance snake
        new_head = move(snake, direction)

        # collisions
        if out_of_bounds(new_head) or (new_head in snake):
            game_over = True
            continue

        snake.insert(0, new_head)

        # eat?
        if food is not None and new_head == food:
            score += 1
            food = spawn_food(snake)
        else:
            snake.pop()

        draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
