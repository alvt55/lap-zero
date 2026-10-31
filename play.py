
import pygame
import math
import handlers
from game import Game

pygame.init()

# Screen settings
WIDTH = 1000
HEIGHT = 750
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAP ZERO")
clock = pygame.time.Clock()

# Colours
GRASS = (37, 91, 54)
GRASS_LIGHT = (43, 101, 60)
ASPHALT = (48, 51, 56)
ASPHALT_LIGHT = (57, 60, 65)
WHITE = (240, 240, 235)
RED = (220, 55, 55)
DARK = (20, 23, 28)
YELLOW = (245, 190, 55)

# Track geometry
OUTER_TRACK = pygame.Rect(100, 75, 800, 600)
INNER_TRACK = pygame.Rect(260, 195, 480, 360)

# Fonts
FONT = pygame.font.SysFont("Arial", 22, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 15)
TITLE_FONT = pygame.font.SysFont("Arial", 30, bold=True)


def draw_background():
    screen.fill(GRASS)

    # Subtle grass pattern
    for x in range(0, WIDTH, 50):
        for y in range(0, HEIGHT, 50):
            pygame.draw.circle(
                screen,
                GRASS_LIGHT,
                (x + 12, y + 15),
                2
            )


def draw_track():
    # Outer kerb
    pygame.draw.ellipse(
        screen, WHITE, OUTER_TRACK.inflate(18, 18)
    )

    # Red kerb border
    pygame.draw.ellipse(
        screen, RED, OUTER_TRACK.inflate(10, 10)
    )

    # Asphalt
    pygame.draw.ellipse(
        screen, ASPHALT, OUTER_TRACK
    )

    # Inner kerb
    pygame.draw.ellipse(
        screen, RED, INNER_TRACK.inflate(10, 10)
    )

    pygame.draw.ellipse(
        screen, WHITE, INNER_TRACK
    )

    # Inner grass
    pygame.draw.ellipse(
        screen, GRASS, INNER_TRACK.inflate(-10, -10)
    )

    # Road edge lines
    pygame.draw.ellipse(
        screen, WHITE, OUTER_TRACK, 3
    )

    pygame.draw.ellipse(
        screen, WHITE, INNER_TRACK, 3
    )

    # Dashed racing line
    pygame.draw.arc(
        screen,
        (130, 133, 137),
        pygame.Rect(125, 100, 750, 550),
        0,
        math.tau,
        2
    )

    # Start / finish line
    draw_start_line()


def draw_start_line():
    # Place the start line on the left side of the track
    x = 105
    y = 270

    square_size = 12

    for row in range(8):
        for col in range(2):
            color = WHITE if (row + col) % 2 == 0 else DARK

            pygame.draw.rect(
                screen,
                color,
                (
                    x + col * square_size,
                    y + row * square_size,
                    square_size,
                    square_size
                )
            )


def draw_car(car):
    center = pygame.Vector2(car.x, car.y)

    # Forward direction
    forward = pygame.Vector2(1, 0).rotate_rad(car.heading)
    side = pygame.Vector2(-forward.y, forward.x)

    # Car shadow
    shadow = [
        center + forward * 25 + side * 13 + pygame.Vector2(4, 5),
        center + forward * 25 - side * 13 + pygame.Vector2(4, 5),
        center - forward * 25 - side * 13 + pygame.Vector2(4, 5),
        center - forward * 25 + side * 13 + pygame.Vector2(4, 5),
    ]

    pygame.draw.polygon(screen, DARK, shadow)

    # Car body
    corners = [
        center + forward * 27 + side * 14,
        center + forward * 27 - side * 14,
        center - forward * 27 - side * 14,
        center - forward * 27 + side * 14,
    ]

    pygame.draw.polygon(screen, RED, corners)

    # Body outline
    pygame.draw.polygon(screen, WHITE, corners, 2)

    # Cockpit / windshield
    cockpit = [
        center + forward * 13 + side * 9,
        center + forward * 13 - side * 9,
        center - forward * 12 - side * 9,
        center - forward * 12 + side * 9,
    ]

    pygame.draw.polygon(screen, (35, 45, 58), cockpit)
    pygame.draw.polygon(screen, (115, 145, 165), cockpit, 1)

    # Wheels
    for longitudinal in [-17, 17]:
        for lateral in [-15, 15]:
            wheel_center = (
                center
                + forward * longitudinal
                + side * lateral
            )

            pygame.draw.circle(
                screen,
                DARK,
                wheel_center,
                6
            )

    # Front lights
    for lateral in [-9, 9]:
        light_pos = center + forward * 25 + side * lateral

        pygame.draw.circle(
            screen,
            YELLOW,
            light_pos,
            3
        )


def draw_hud(car):
    # HUD background
    hud = pygame.Rect(20, 20, 220, 110)

    pygame.draw.rect(
        screen, DARK, hud, border_radius=12
    )

    pygame.draw.rect(
        screen, (75, 80, 90), hud, 1, border_radius=12
    )

    # Title
    title = TITLE_FONT.render("LAP ZERO", True, WHITE)
    screen.blit(title, (35, 28))

    # Speed
    speed = int(car.speed)

    speed_label = SMALL_FONT.render(
        "SPEED", True, (160, 165, 175)
    )

    speed_value = FONT.render(
        f"{speed} km/h", True, WHITE
    )

    screen.blit(speed_label, (35, 72))
    screen.blit(speed_value, (35, 88))

    # Controls panel
    controls = SMALL_FONT.render(
        "WASD / ARROWS  |  R: RESET",
        True,
        WHITE
    )

    screen.blit(
        controls,
        (WIDTH - controls.get_width() - 25, 25)
    )


def main():
    game = Game()
    running = True

    while running:

        # 1. Handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()

        # 2. Calculate frame time
        dt = min(clock.tick(FPS) / 1000, 0.05)

        # 3. Get keyboard controls
        steering, acceleration = handlers.get_controls()

        # 4. Update physics
        game.car.update(
            steering,
            acceleration,
            dt
        )

        # 5. Render
        draw_background()
        draw_track()
        draw_car(game.car)
        draw_hud(game.car)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
