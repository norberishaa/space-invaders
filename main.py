import pygame
import os
import random

pygame.init()

#  WINDOW SETUP
WIDTH, HEIGHT = 700, 1020
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(False)
FPS = 60

# IMAGES
BACKGROUND = pygame.image.load(os.path.join('images', 'background.png'))
OVERLAP = pygame.image.load(os.path.join('images', 'background_1.png'))
SHIP_IMAGE = pygame.image.load(os.path.join('images', 'space_ship.png'))
ROCK1 = pygame.image.load(os.path.join('images', 'rock.png'))
ROCK2 = pygame.image.load(os.path.join('images', 'rock_2.png'))
ROCK3 = pygame.image.load(os.path.join('images', 'rock_3.png'))
ROCK_IMAGES = [ROCK1, ROCK2, ROCK3]
WHITE = (255, 255, 25)
BLACK = (0, 0, 0)

# SHIP
SHIP_WIDTH, SHIP_HEIGHT = 50, 50
VEL = 6

# BULLET
BULLET_VEL = 10


# DRAWd
def draw(ship, bullets, rocks, score, lives_left):

    WIN.blit(score, (WIDTH // 2, HEIGHT // 2))
    WIN.blit(lives_left, (WIDTH // 2 - lives_left.get_width() // 2, 0))

    for bullet in bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    WIN.blit(SHIP_IMAGE, (ship.x, ship.y))

    for rock, rock_image in rocks:
        WIN.blit(rock_image, (rock.x, rock.y))


# MOVEMENT
def move(ship, keys_pressed):
    if keys_pressed[pygame.K_a] and ship.x+VEL >= 0:
        ship.x -= VEL
    if keys_pressed[pygame.K_d] and ship.x <= WIDTH - SHIP_WIDTH:
        ship.x += VEL
    if keys_pressed[pygame.K_w] and ship.y >= HEIGHT // 2:
        ship.y -= VEL
    if keys_pressed[pygame.K_s] and ship.y <= HEIGHT - SHIP_HEIGHT:
        ship.y += VEL


# BULLET
def create_bullet(ship):
    new_bullet = pygame.Rect(ship.x + SHIP_WIDTH // 2, ship.y, 4, 8)
    return new_bullet


def bullet_movement(bullets):
    for bullet in bullets:
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            bullet.y -= BULLET_VEL


# ROCK
def choose_rock(rock_images):
    rock_image = random.choices(rock_images, weights=[1, 2, 2], k=1)[0]
    return rock_image


def create_rock(rock_image):
    new_rock = rock_image.get_rect()
    new_rock.x = random.randint(0, WIDTH-new_rock.width)
    new_rock.y = 0-new_rock.height

    return new_rock


def rock_movement(rocks):
    for rock, rock_image in rocks:
        if rock.y >= HEIGHT:
            rocks.remove((rock, rock_image))
            return True
        else:
            rock.y += 5


def is_hit(rocks, bullets):
    for rock, rock_image in rocks:
        rock_mask = pygame.mask.from_surface(rock_image)
        for bullet in bullets:
            bullet_surface = pygame.Surface((bullet.width, bullet.height))
            bullet_mask = pygame.mask.from_surface(bullet_surface)
            offset = (rock.x - bullet.x, rock.y - bullet.y)
            if bullet_mask.overlap(rock_mask, offset):
                rocks.remove((rock, rock_image))
                bullets.remove(bullet)
                return True
    return False


def is_collision(rocks, ship):
    ship_mask = pygame.mask.from_surface(SHIP_IMAGE)
    for rock, rock_image in rocks:
        rock_mask = pygame.mask.from_surface(rock_image)
        offset = (ship.x - rock.x, ship.y - rock.y)
        if rock_mask.overlap(ship_mask, offset):
            rocks.remove((rock, rock_image))
            return True
    return False


def main():
    ship = pygame.Rect(WIDTH // 2 - SHIP_WIDTH // 2, HEIGHT - SHIP_HEIGHT - 10, SHIP_WIDTH, SHIP_HEIGHT)
    bullets = []

    rocks = []
    rock_timer = 0

    clock = pygame.time.Clock()
    point = 0
    lives = 5
    b_pos = 0
    o_pos = 1020
    speed = 2
    while lives > 0:
        if b_pos <= -HEIGHT:
            b_pos = HEIGHT
        if o_pos <= - HEIGHT:
            o_pos = HEIGHT

        b_pos -= speed
        o_pos -= speed

        WIN.blit(BACKGROUND, (0, b_pos))
        WIN.blit(OVERLAP, (0, o_pos))

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                lives = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(bullets) <= 5:
                new_bullet = create_bullet(ship)
                bullets.append(new_bullet)

        if rock_timer == 0:
            rock_image_choice = choose_rock(ROCK_IMAGES)
            rock = create_rock(rock_image_choice)
            rocks.append((rock, rock_image_choice))
            rock_timer = 50
        else:
            rock_timer -= 1

        bullet_movement(bullets)
        rock_movement(rocks)
        keys_pressed = pygame.key.get_pressed()
        move(ship, keys_pressed)

        if is_hit(rocks, bullets):
            point += 1

        if is_collision(rocks, ship):
            lives -= 1

        score_font = pygame.font.SysFont('Franklin Gothic Medium', 50)
        lives_font = pygame.font.SysFont('Franklin Gothic Medium', 20)
        score = score_font.render(str(point), False, (255, 255, 255))
        lives_left = lives_font.render(f'LIVES LEFT: {str(lives)}', False, (255, 255, 255))

        draw(ship, bullets, rocks, score, lives_left)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
