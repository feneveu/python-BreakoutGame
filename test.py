import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
# Width and the height of the screen
WIDTH, HEIGHT = 800, 600
# Speed that the users paddle can move at
PADDLE_SPEED = 6
# the number of bricks in each col/row
BRICK_ROWS, BRICK_COLS = 5, 8
# the width of each brick is proportional to the screen width
BRICK_WIDTH = WIDTH // BRICK_COLS
# height of each brick
BRICK_HEIGHT = 30

# Colors - basic entities
WHITE = (255, 255, 255)
DRED = (139, 0, 0)
BLACK = (0, 0, 0)

# used for coloring the bricks
fire_colors = [(255, 0, 0), (255, 90, 0), (255, 154, 0), (255, 206, 0), (255, 232, 8)]

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Load the title background image
title_background = pygame.image.load("background.jpg")
title_background = pygame.transform.scale(title_background, (WIDTH, HEIGHT))

# Fonts - 2 custom fonts in files as specified
font = pygame.font.Font("arcade_font.otf", 80)
sub_font = pygame.font.Font("pixel_font.ttf", 20)


def draw_title_screen():
    """Draws the title screen"""
    # .blit - draw at this location
    screen.blit(title_background, (0, 0))
    # Render the title text and start text in different fonts
    title_text = font.render("BREAKOUT", True, WHITE)
    start_text = sub_font.render("Press any key to start", True, WHITE)

    # draw them at these points
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    # update the screen
    pygame.display.update()


# Displaying the title screen
showing_title = True
while showing_title:
    # draw the title to the screen and then wait for event
    draw_title_screen()
    # if there is any event possible
    for event in pygame.event.get():
        # if the event is quit, end the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if it's just a random key stop showing the title and begin the game
        if event.type == pygame.KEYDOWN:
            showing_title = False

# Difficulty selection - starts off as None
difficulty = None


def draw_menu():
    """Draws the Level Menu"""
    # fill the screen with black
    screen.fill(BLACK)

    # render the different levels
    text_easy = sub_font.render("1. Easy", True, WHITE)
    text_medium = sub_font.render("2. Medium", True, WHITE)
    text_hard = sub_font.render("3. Hard", True, WHITE)

    # place the text on the screen
    screen.blit(text_easy, (WIDTH // 2 - 50, HEIGHT // 2 - 60))
    screen.blit(text_medium, (WIDTH // 2 - 50, HEIGHT // 2))
    screen.blit(text_hard, (WIDTH // 2 - 50, HEIGHT // 2 + 60))

    # update the window
    pygame.display.update()


# while the user is choosing a level
choosing = True
while choosing:
    # draw the menu of options
    draw_menu()
    for event in pygame.event.get():
        # if ever the user presses quit exit on that command
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # otherwise if it's a keydown, check if it's a specific one
        if event.type == pygame.KEYDOWN:
            # if key down was 1, game is easy
            if event.key == pygame.K_1:
                difficulty = 4  # Easy
            # if key down is 2 game is medium
            elif event.key == pygame.K_2:
                difficulty = 6  # Medium
            # if keydown was 3 game is hard
            elif event.key == pygame.K_3:
                difficulty = 10  # Hard
            # if a difficulty exists, exit this loop and begin the game at that difficulty
            if difficulty:
                choosing = False

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10)

# Ball - the ball will move with the speed set by the difficulty
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 20, 20)
ball_dx, ball_dy = difficulty, -difficulty

# Bricks with random fire colors
bricks = [(pygame.Rect(int(col * BRICK_WIDTH), int(row * BRICK_HEIGHT), int(BRICK_WIDTH - 2), int(BRICK_HEIGHT - 2)),
           random.choice(fire_colors))
          for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]

# Initialize the number of lives
lives = 2

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    # fill the screen with black
    screen.fill(BLACK)

    # quits if user exits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement - if paddle can go left/right it will go left/right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-PADDLE_SPEED, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(PADDLE_SPEED, 0)

    # Ball movement
    ball.move_ip(ball_dx, ball_dy)

    # Ball collisions
    # .colliderect - compares 2 pygame rects and checks if they collide
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy
    if ball.colliderect(paddle):
        ball_dy = -ball_dy

    # Ball and brick collisions
    for brick, color in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove((brick, color))
            ball_dy = -ball_dy
            break

    # Ball out of bounds
    if ball.bottom >= HEIGHT:
        lives -= 1  # Player loses a life
        if lives <= 0:  # Game over if no lives left
            screen.fill(BLACK)
            game_over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            running = False
        else:  # Reset ball position
            ball.topleft = (WIDTH // 2, HEIGHT // 2)
            ball_dx, ball_dy = difficulty, -difficulty

    # Check win condition
    if len(bricks) == 0:
        screen.fill(BLACK)
        win_text = font.render("YOU WIN!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 40))
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting
        running = False  # Player wins if all bricks are destroyed

    # Draw elements
    pygame.draw.rect(screen, DRED, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

    # Draw lives in the bottom-left corner
    lives_text = sub_font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, HEIGHT - 30))

    # Draw game over message if out of lives
    if lives <= 0:
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))

    # Refresh screen
    pygame.display.update()
    clock.tick(60)

pygame.quit()
