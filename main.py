import pygame
import random
import math

# Initializing PyGame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Creating the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Game Title & Icon
icon = pygame.image.load('Assets/Images/ufo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Fighters')

# Game variables
DANGER_LINE_Y = 400  # Y level where enemies trigger an event
player_lives = 3
score = 0
game_over_state = False
background_y1 = 0
background_y2 = -screen_height  # Second background starts above screen

# Load images once for efficiency
try:
    heart_img = pygame.image.load('Assets/Images/heart.png')
    spaceship_img = pygame.image.load('Assets/Images/spaceship.png')
    ufo_img = pygame.image.load('Assets/Images/ufo.png')
    bullet_img = pygame.image.load('Assets/Images/laserBullet.png')
    background_img = pygame.image.load('Assets/Images/space_background.jpg')  # Add your space background
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
except pygame.error as e:
    print(f"Could not load image: {e}")
    # Create a simple starfield background if no background image
    background_img = pygame.Surface((screen_width, screen_height))
    background_img.fill((0, 0, 20))  # Dark blue space
    # Add some stars
    for _ in range(100):
        star_x = random.randint(0, screen_width)
        star_y = random.randint(0, screen_height)
        pygame.draw.circle(background_img, (255, 255, 255), (star_x, star_y), random.randint(1, 2))

# Load sound effects
try:
    bullet_sound = pygame.mixer.Sound('Assets/Audio/bullet_fire.wav')  # Add your bullet fire sound
    bullet_sound.set_volume(0.3)  # Adjust volume (0.0 to 1.0)
except pygame.error:
    print("Could not load bullet_fire.wav, continuing without sound")
    bullet_sound = None

try:
    hit_sound = pygame.mixer.Sound('Assets/Audio/explosion.wav')  # Add your hit/explosion sound
    hit_sound.set_volume(0.5)
except pygame.error:
    print("Could not load explosion.wav, continuing without sound")
    hit_sound = None

# Load and play background music
try:
    pygame.mixer.music.load('Assets/Audio/space_music.mp3')  # Add your background music
    pygame.mixer.music.set_volume(0.2)  # Adjust volume
    pygame.mixer.music.play(-1)  # -1 means loop forever
except pygame.error:
    print("Could not load space_music.mp3, continuing without music")


# Background scrolling function
def scroll_background():
    global background_y1, background_y2

    # Move both backgrounds down
    background_y1 += 0.5  # Adjust speed as needed
    background_y2 += 0.5

    # Reset positions when they go off screen
    if background_y1 >= screen_height:
        background_y1 = background_y2 - screen_height
    if background_y2 >= screen_height:
        background_y2 = background_y1 - screen_height


def draw_background():
    screen.blit(background_img, (0, background_y1))
    screen.blit(background_img, (0, background_y2))


# Collision detection function
def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < 35  # Slightly increased for better hit detection


# Showing Lives with Hearts
def show_lives():
    for i in range(player_lives):
        screen.blit(heart_img, (10 + i * 40, 10))


# Showing Score
def show_score():
    font = pygame.font.Font('freesansbold.ttf', 32)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_shadow = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_shadow, (screen_width - 199, 11))  # Shadow effect
    screen.blit(score_text, (screen_width - 200, 10))


# Game Over
def game_over():
    # Semi-transparent overlay
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_over_text = over_font.render('GAME OVER', True, (255, 0, 0))
    game_over_shadow = over_font.render('GAME OVER', True, (128, 0, 0))

    # Center the text
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    shadow_rect = game_over_shadow.get_rect(center=(screen_width // 2 + 2, screen_height // 2 - 48))

    screen.blit(game_over_shadow, shadow_rect)
    screen.blit(game_over_text, text_rect)

    # Final score
    final_font = pygame.font.Font('freesansbold.ttf', 36)
    final_score_text = final_font.render(f'Final Score: {score}', True, (255, 255, 255))
    final_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    screen.blit(final_score_text, final_rect)

    restart_font = pygame.font.Font('freesansbold.ttf', 24)
    restart_text = restart_font.render('Close window to exit', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
    screen.blit(restart_text, restart_rect)


# The Player
class Player:
    def __init__(self, player_img, player_X, player_Y):
        self.player_img = player_img
        self.player_X = player_X
        self.player_Y = player_Y

    def drawPlayer(self, screen):
        screen.blit(self.player_img, (self.player_X, self.player_Y))


player_X = screen_width // 2 - 32
player_Y = 470
player = Player(spaceship_img, player_X, player_Y)
playerX_change = 0


# The Enemy
class Enemy:
    def __init__(self, enemy_img, enemy_X, enemy_Y):
        self.enemy_img = enemy_img
        self.enemy_X = enemy_X
        self.enemy_Y = enemy_Y
        self.speed = 1

    def move(self):
        self.enemy_Y += self.speed

    def drawEnemy(self, screen):
        screen.blit(self.enemy_img, (self.enemy_X, self.enemy_Y))


enemy = []
no_of_enemies = random.randint(3, 6)

for i in range(no_of_enemies):
    enemy_X = random.randint(0, 736)
    enemy_Y = random.randint(-200, -50)
    enemy.append(Enemy(ufo_img, enemy_X, enemy_Y))


# Bullet
class Bullet:
    def __init__(self, bulletImg, bullet_X, bullet_Y):
        self.bulletImg = bulletImg
        self.bullet_X = bullet_X
        self.bullet_Y = bullet_Y
        self.speed = 5

    def bulletMove(self):
        self.bullet_Y -= self.speed

    def drawBullet(self, screen):
        screen.blit(self.bulletImg, (self.bullet_X, self.bullet_Y))


bullets = []

# Game Loop
run_status = True
clock = pygame.time.Clock()

while run_status:
    # Scroll and draw background
    if not game_over_state:
        scroll_background()
    draw_background()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_status = False

        # Only allow input if game is not over
        if not game_over_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 4
                elif event.key == pygame.K_SPACE:
                    # Play bullet fire sound
                    if bullet_sound:
                        bullet_sound.play()

                    left_bullet_x = player.player_X + 8
                    right_bullet_x = player.player_X + 40
                    bullet_y = player.player_Y
                    bullets.append(Bullet(bullet_img, left_bullet_x, bullet_y))
                    bullets.append(Bullet(bullet_img, right_bullet_x, bullet_y))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    # Only update game logic if game is not over
    if not game_over_state:
        # Update player position
        player.player_X += playerX_change

        # Keep player within screen bounds
        if player.player_X <= 0:
            player.player_X = 0
        elif player.player_X >= screen_width - 64:
            player.player_X = screen_width - 64

        # Update and check enemies
        for i in range(len(enemy) - 1, -1, -1):
            enemy[i].move()

            # Check if enemy crossed the danger line
            if enemy[i].enemy_Y >= DANGER_LINE_Y:
                player_lives -= 1
                enemy.pop(i)

                if player_lives <= 0:
                    game_over_state = True
                    pygame.mixer.music.stop()  # Stop background music on game over
                continue

            # Remove enemies that went off screen
            if enemy[i].enemy_Y > screen_height:
                enemy.pop(i)

        # Update bullets and check for collisions
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet_idx, bullet in enumerate(bullets):
            bullet.bulletMove()

            # Mark bullets that went off screen for removal
            if bullet.bullet_Y < 0:
                bullets_to_remove.append(bullet_idx)
                continue

            # Check collision with enemies
            for enemy_idx, current_enemy in enumerate(enemy):
                if isCollision(current_enemy.enemy_X, current_enemy.enemy_Y,
                               bullet.bullet_X, bullet.bullet_Y):

                    # Play hit sound
                    if hit_sound:
                        hit_sound.play()

                    # Mark both bullet and enemy for removal
                    if bullet_idx not in bullets_to_remove:
                        bullets_to_remove.append(bullet_idx)
                    if enemy_idx not in enemies_to_remove:
                        enemies_to_remove.append(enemy_idx)

                    score += 10
                    break

        # Remove bullets and enemies (in reverse order to maintain indices)
        for idx in sorted(bullets_to_remove, reverse=True):
            if idx < len(bullets):
                bullets.pop(idx)

        for idx in sorted(enemies_to_remove, reverse=True):
            if idx < len(enemy):
                enemy.pop(idx)

        # Respawn enemies if all are destroyed
        if len(enemy) == 0:
            no_of_enemies = random.randint(4, 8)
            for i in range(no_of_enemies):
                enemy_X = random.randint(0, 736)
                enemy_Y = random.randint(-400, -50)
                enemy.append(Enemy(ufo_img, enemy_X, enemy_Y))

    # Draw everything
    for current_enemy in enemy:
        current_enemy.drawEnemy(screen)

    for bullet in bullets:
        bullet.drawBullet(screen)

    player.drawPlayer(screen)

    show_lives()
    show_score()

    if game_over_state:
        game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()