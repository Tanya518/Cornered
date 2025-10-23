# Pygame Web Version - Adapted for pygbag

import asyncio
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
import sys
import platform

# Check if running in browser
if platform.system() == "Emscripten" or sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

pygame.init()

# Adaptive screen size for browser
WIDTH = 1200
HEIGHT = 800

FONT = pygame.font.SysFont('Verdana', 30)

CURSE_PHRASES = [
    "Ой лишенько!",
    "Та що за халепа!",
    "Ану ж бо!",
    "От тобі й на!",
    "Та йой-йой-йой!",
    "Капець повний!",
    "Мамо рідна!",
    "Та ну шо за дєлов!",
    "Хренасе!",
    "Пипець!",
]

SARCASTIC_PHRASES = [
    "Ну звісно, чого ще чекати!",
    "Якась магія просто!",
    "О, як несподівано!",
    "Ну класно ж!",
    "От це поворот!",
    "Аха, ну-ну!",
    "Може ще разок?",
    "Чудово, нема слів!",
    "Браво, просто браво!",
    "Ну і дива!",
]

HAPPY_PHRASES = [
    "Ням-ням!",
    "Ммм, смакота!",
    "От це так!",
    "Кайф!",
    "Хрум-хрум!",
    "Ото добре!",
    "Красота!",
    "Ось це діло!",
    "Смачно!",
    "Чудово!",
]

COLOR_GREEN = (166, 240, 96)
COLOR_BLACK = (0, 0, 0)
COLOR_ORANGE = (232, 100, 33)
COLOR_RED = (0x78, 0x1F, 0x1F)
COLOR_DARK_GRAY = (0x15, 0x15, 0x15)
COLOR_WHITE = (255, 255, 255)
COLOR_SNOWFLAKE = (0xF4, 0xEF, 0xE5)
COLOR_LIGHT_GREEN = (0x9A, 0xD3, 0x70)

main_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Cornered - Моя Перша Гра")

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.Surface(enemy_size)
    enemy.fill(COLOR_ORANGE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, HEIGHT - 50), *enemy_size)
    enemy_move = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (40, 40)
    bonus_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    bonus = pygame.Surface(bonus_size, pygame.SRCALPHA)
    pygame.draw.polygon(bonus, bonus_color, [(20, 0), (0, 40), (40, 40)])
    bonus_rect = pygame.Rect(random.randint(50, WIDTH - 50), 0, *bonus_size)
    bonus_move = [0, random.randint(2, 6)]
    return [bonus, bonus_rect, bonus_move]

def create_diamond():
    diamond_size = (40, 40)
    diamond = pygame.Surface(diamond_size, pygame.SRCALPHA)
    pygame.draw.polygon(diamond, COLOR_RED, [(20, 0), (40, 20), (20, 40), (0, 20)])
    diamond_rect = pygame.Rect(WIDTH, random.randint(50, HEIGHT - 50), *diamond_size)
    diamond_move = [random.randint(-6, -1), 0]
    return [diamond, diamond_rect, diamond_move]

def create_snow_hexagon(bonuses):
    hex_size = (30, 30)
    hex_surf = pygame.Surface(hex_size, pygame.SRCALPHA)
    center = 15
    radius = 14
    points = []
    for i in range(6):
        angle = i * 60 * 3.14159 / 180
        x = center + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x
        y = center + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
        points.append((x, y))
    pygame.draw.polygon(hex_surf, COLOR_WHITE, points)

    rotation_angle = random.uniform(0, 360)
    hex_surf = pygame.transform.rotate(hex_surf, rotation_angle)

    spawn_x = random.randint(50, WIDTH - 50)
    if bonuses:
        while any(abs(spawn_x - bonus[1].centerx) < 50 and abs(0 - bonus[1].centery) < 50 for bonus in bonuses):
            spawn_x = random.randint(50, WIDTH - 50)

    hex_rect = pygame.Rect(spawn_x, 0, *hex_size)
    hex_move = [0, 3]
    vibration = random.uniform(0, 6.28)
    vibration_direction = random.uniform(-1, 1)
    return [hex_surf, hex_rect, hex_move, vibration, vibration_direction]

def create_green_hexagon(bonuses):
    hex_size = (30, 30)
    hex_surf = pygame.Surface(hex_size, pygame.SRCALPHA)
    center = 15
    radius = 14
    points = []
    for i in range(6):
        angle = i * 60 * 3.14159 / 180
        x = center + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x
        y = center + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
        points.append((x, y))
    pygame.draw.polygon(hex_surf, COLOR_LIGHT_GREEN, points)

    rotation_angle = random.uniform(0, 360)
    hex_surf = pygame.transform.rotate(hex_surf, rotation_angle)

    spawn_x = random.randint(50, WIDTH - 50)
    if bonuses:
        while any(abs(spawn_x - bonus[1].centerx) < 50 and abs(0 - bonus[1].centery) < 50 for bonus in bonuses):
            spawn_x = random.randint(50, WIDTH - 50)

    hex_rect = pygame.Rect(spawn_x, 0, *hex_size)
    hex_move = [0, 3]
    vibration = random.uniform(0, 6.28)
    vibration_direction = random.uniform(-1, 1)
    return [hex_surf, hex_rect, hex_move, vibration, vibration_direction]

async def main():
    FPS = pygame.time.Clock()

    player_size = (60, 60)
    player = pygame.Surface(player_size, pygame.SRCALPHA)
    player.fill(COLOR_GREEN)
    pygame.draw.circle(player, COLOR_BLACK, (48, 12), 5)
    player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    player_speed = 6

    CREATE_ENEMY = pygame.USEREVENT + 1
    CREATE_BONUS = pygame.USEREVENT + 2
    CHANGE_DIFFICULTY = pygame.USEREVENT + 3
    CREATE_DIAMOND = pygame.USEREVENT + 4
    CREATE_SNOW_CIRCLE = pygame.USEREVENT + 5
    CREATE_GREEN_CIRCLE = pygame.USEREVENT + 6

    enemy_timer = 1200
    bonus_timer = 1500
    diamond_timer = 4500
    snow_circle_timer = 2500
    green_circle_timer = 2500

    pygame.time.set_timer(CREATE_ENEMY, enemy_timer)
    pygame.time.set_timer(CREATE_BONUS, bonus_timer)
    pygame.time.set_timer(CHANGE_DIFFICULTY, 5000)
    pygame.time.set_timer(CREATE_DIAMOND, diamond_timer)
    pygame.time.set_timer(CREATE_SNOW_CIRCLE, snow_circle_timer)
    pygame.time.set_timer(CREATE_GREEN_CIRCLE, green_circle_timer)

    enemies = []
    bonuses = []
    diamonds = []
    snow_circles = []
    green_circles = []
    snowflakes = []

    score = 0
    best_score = 0

    playing = True
    enemy_collision_occurred = False
    diamond_collision_occurred = False
    snow_collision_occurred = False
    knockback_velocity = pygame.math.Vector2(0, 0)
    rotation_angle = 0
    rotation_speed = 0
    is_enlarged = False
    is_snowing = False
    wind_force = pygame.math.Vector2(0, 0)
    original_player_size = (60, 60)
    enlarged_player_size = (90, 90)
    current_phrase = ""
    phrase_timer = 0

    while playing:
        FPS.tick(120)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CREATE_DIAMOND:
                diamonds.append(create_diamond())
            if event.type == CREATE_SNOW_CIRCLE:
                snow_circles.append(create_snow_hexagon(bonuses))
            if event.type == CREATE_GREEN_CIRCLE:
                green_circles.append(create_green_hexagon(bonuses))
            if event.type == CHANGE_DIFFICULTY:
                if enemy_timer > 400:
                    enemy_timer -= 50
                    pygame.time.set_timer(CREATE_ENEMY, enemy_timer)
                if bonus_timer > 800:
                    bonus_timer -= 50
                    pygame.time.set_timer(CREATE_BONUS, bonus_timer)
                if diamond_timer > 1500:
                    diamond_timer -= 100
                    pygame.time.set_timer(CREATE_DIAMOND, diamond_timer)

        main_display.fill(COLOR_BLACK)

        # Simple snowflakes - just circles, no rotation
        if is_snowing:
            if random.random() < 0.1 and len(snowflakes) < 50:
                snowflake_x = random.randint(0, WIDTH)
                snowflake_y = 0
                snowflake_size = random.randint(3, 6)
                snowflake_rotation = random.uniform(0, 6.28)  # Initial rotation
                snowflake_rotation_speed = random.uniform(-0.02, 0.02)  # Slow rotation
                snowflakes.append([snowflake_x, snowflake_y, snowflake_size, snowflake_rotation, snowflake_rotation_speed])

            for snowflake in snowflakes:
                snowflake[0] += wind_force.x
                snowflake[1] += 2
                snowflake[3] += snowflake[4]  # Update rotation slowly

                if snowflake[1] < HEIGHT and 0 < snowflake[0] < WIDTH:
                    # Draw simple rotating snowflake (4-pointed star)
                    size = snowflake[2]
                    angle = snowflake[3]
                    center_x, center_y = int(snowflake[0]), int(snowflake[1])

                    # Draw 4 points of star
                    for i in range(4):
                        point_angle = angle + i * 1.57  # 90 degrees in radians
                        end_x = center_x + size * pygame.math.Vector2(1, 0).rotate_rad(point_angle).x
                        end_y = center_y + size * pygame.math.Vector2(1, 0).rotate_rad(point_angle).y
                        pygame.draw.line(main_display, COLOR_SNOWFLAKE, (center_x, center_y), (int(end_x), int(end_y)), 2)

            snowflakes = [s for s in snowflakes if s[1] < HEIGHT and 0 < s[0] < WIDTH]

        if knockback_velocity.length() > 0.5:
            new_x = player_rect.x + knockback_velocity.x
            new_y = player_rect.y + knockback_velocity.y

            if new_x < 0:
                player_rect.x = 0
                knockback_velocity.x = -knockback_velocity.x * 0.6
                rotation_speed += knockback_velocity.y * 1.0
            elif new_x > WIDTH - player_rect.width:
                player_rect.x = WIDTH - player_rect.width
                knockback_velocity.x = -knockback_velocity.x * 0.6
                rotation_speed -= knockback_velocity.y * 1.0
            else:
                player_rect.x = int(new_x)

            if new_y < 0:
                player_rect.y = 0
                knockback_velocity.y = -knockback_velocity.y * 0.6
                rotation_speed -= knockback_velocity.x * 1.0
            elif new_y > HEIGHT - player_rect.height:
                player_rect.y = HEIGHT - player_rect.height
                knockback_velocity.y = -knockback_velocity.y * 0.6
                rotation_speed += knockback_velocity.x * 1.0
            else:
                player_rect.y = int(new_y)

            knockback_velocity *= 0.95
        else:
            knockback_velocity = pygame.math.Vector2(0, 0)

            keys = pygame.key.get_pressed()
            move_x = 0
            move_y = 0

            if keys[K_DOWN] and player_rect.bottom < HEIGHT:
                move_y += player_speed
            if keys[K_RIGHT] and player_rect.right < WIDTH:
                move_x += player_speed
            if keys[K_UP] and player_rect.top > 0:
                move_y -= player_speed
            if keys[K_LEFT] and player_rect.left > 0:
                move_x -= player_speed

            if is_snowing:
                move_x += wind_force.x
                move_y += wind_force.y

            new_x = player_rect.x + move_x
            new_y = player_rect.y + move_y

            if 0 <= new_x <= WIDTH - player_rect.width:
                player_rect.x = int(new_x)
            if 0 <= new_y <= HEIGHT - player_rect.height:
                player_rect.y = int(new_y)

        if abs(rotation_speed) > 0.05:
            rotation_angle += rotation_speed
            rotation_speed *= 0.98
        else:
            rotation_speed = 0

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]) and not enemy_collision_occurred:
                if random.random() < 0.5:
                    current_phrase = random.choice(SARCASTIC_PHRASES)
                else:
                    current_phrase = random.choice(CURSE_PHRASES)
                phrase_timer = 120
                score -= 1
                enemy_collision_occurred = True

                collision_direction = pygame.math.Vector2(player_rect.centerx - enemy[1].centerx,
                                                          player_rect.centery - enemy[1].centery)

                if collision_direction.length() > 0:
                    collision_direction = collision_direction.normalize()
                else:
                    collision_direction = pygame.math.Vector2(1, 0)

                enemy_speed = abs(enemy[2][0])
                knockback_force = 10 + enemy_speed * 2
                knockback_velocity = collision_direction * knockback_force

                offset_y = (enemy[1].centery - player_rect.centery) / (player_rect.height / 2)
                offset_x = (enemy[1].centerx - player_rect.centerx) / (player_rect.width / 2)
                rotation_speed = (offset_y * knockback_velocity.x - offset_x * knockback_velocity.y) * 1.5

            if score < 0:
                playing = False

            if not any(player_rect.colliderect(enemy[1]) for enemy in enemies):
                enemy_collision_occurred = False

        for diamond in diamonds:
            diamond[1] = diamond[1].move(diamond[2])
            main_display.blit(diamond[0], diamond[1])

            if player_rect.colliderect(diamond[1]) and not diamond_collision_occurred:
                current_phrase = random.choice(SARCASTIC_PHRASES)
                phrase_timer = 120
                diamond_collision_occurred = True
                is_enlarged = True

                player_center = player_rect.center
                player = pygame.Surface(enlarged_player_size, pygame.SRCALPHA)
                player.fill(COLOR_DARK_GRAY)
                pygame.draw.circle(player, COLOR_BLACK, (72, 18), 7)
                player_rect = player.get_rect(center=player_center)

                collision_direction = pygame.math.Vector2(player_rect.centerx - diamond[1].centerx,
                                                          player_rect.centery - diamond[1].centery)

                if collision_direction.length() > 0:
                    collision_direction = collision_direction.normalize()
                else:
                    collision_direction = pygame.math.Vector2(1, 0)

                diamond_speed = abs(diamond[2][0])
                knockback_force = 10 + diamond_speed * 2
                knockback_velocity = collision_direction * knockback_force

                offset_y = (diamond[1].centery - player_rect.centery) / (player_rect.height / 2)
                offset_x = (diamond[1].centerx - player_rect.centerx) / (player_rect.width / 2)
                rotation_speed = (offset_y * knockback_velocity.x - offset_x * knockback_velocity.y) * 1.5

            if not any(player_rect.colliderect(diamond[1]) for diamond in diamonds):
                diamond_collision_occurred = False

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += 1
                current_phrase = random.choice(HAPPY_PHRASES)
                phrase_timer = 120
                bonus_color = bonus[0].get_at((20, 20))

                if is_enlarged:
                    player_center = player_rect.center
                    player = pygame.Surface(original_player_size, pygame.SRCALPHA)
                    player.fill(bonus_color)
                    pygame.draw.circle(player, COLOR_BLACK, (48, 12), 5)
                    player_rect = player.get_rect(center=player_center)
                    is_enlarged = False
                else:
                    player.fill(bonus_color)
                    pygame.draw.circle(player, COLOR_BLACK, (48, 12), 5)

                bonuses.pop(bonuses.index(bonus))

        for snow_circle in snow_circles:
            snow_circle[3] += 0.25
            vibration_amplitude = 3.5
            vibration_x = vibration_amplitude * pygame.math.Vector2(1, 0).rotate_rad(snow_circle[3]).x * snow_circle[4]

            snow_circle[1] = snow_circle[1].move([0, snow_circle[2][1]])

            draw_x = snow_circle[1].x + vibration_x
            draw_y = snow_circle[1].y
            main_display.blit(snow_circle[0], (draw_x, draw_y))

            if player_rect.colliderect(snow_circle[1]) and not snow_collision_occurred:
                current_phrase = random.choice(CURSE_PHRASES)
                phrase_timer = 120
                snow_collision_occurred = True
                is_snowing = True
                wind_force = pygame.math.Vector2(random.uniform(-3, 3), random.uniform(-1, 1))

            if not any(player_rect.colliderect(snow_circle[1]) for snow_circle in snow_circles):
                snow_collision_occurred = False

        for green_circle in green_circles:
            green_circle[3] += 0.25
            vibration_amplitude = 3.5
            vibration_x = vibration_amplitude * pygame.math.Vector2(1, 0).rotate_rad(green_circle[3]).x * green_circle[4]

            green_circle[1] = green_circle[1].move([0, green_circle[2][1]])

            draw_x = green_circle[1].x + vibration_x
            draw_y = green_circle[1].y
            main_display.blit(green_circle[0], (draw_x, draw_y))

            if player_rect.colliderect(green_circle[1]):
                current_phrase = random.choice(HAPPY_PHRASES)
                phrase_timer = 120
                score += 3
                is_snowing = False
                wind_force = pygame.math.Vector2(0, 0)
                snowflakes.clear()
                green_circles.pop(green_circles.index(green_circle))

        if phrase_timer > 0:
            phrase_timer -= 1
            phrase_surface = FONT.render(current_phrase, True, COLOR_GREEN)
            main_display.blit(phrase_surface, (20, 60))

        score_color = COLOR_GREEN if score >= 0 else COLOR_ORANGE
        main_display.blit(FONT.render(f'Score: {score}', True, score_color), (20, 20))

        if abs(rotation_angle) > 0.5:
            rotated_player = pygame.transform.rotate(player, rotation_angle)
            rotated_rect = rotated_player.get_rect(center=player_rect.center)
            main_display.blit(rotated_player, rotated_rect)
        else:
            main_display.blit(player, player_rect)

        pygame.display.flip()
        await asyncio.sleep(0)  # Critical for pygbag!

        enemies = [enemy for enemy in enemies if enemy[1].left > 0]
        bonuses = [bonus for bonus in bonuses if bonus[1].top <= HEIGHT]
        diamonds = [diamond for diamond in diamonds if diamond[1].left > 0]
        snow_circles = [sc for sc in snow_circles if sc[1].top <= HEIGHT]
        green_circles = [gc for gc in green_circles if gc[1].top <= HEIGHT]

    # Game Over screen
    if score > best_score:
        best_score = score

    main_display.fill(COLOR_BLACK)
    game_over_font = pygame.font.SysFont('Verdana', 60)
    game_over_text = game_over_font.render('GAME OVER', True, COLOR_ORANGE)
    score_text = FONT.render(f'Your Score: {score}', True, COLOR_GREEN)
    best_text = FONT.render(f'Best Score: {best_score}', True, COLOR_GREEN)
    restart_text = FONT.render('Reload page to restart', True, COLOR_GREEN)

    main_display.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    main_display.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    main_display.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 50))
    main_display.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 120))

    pygame.display.flip()

    # Wait for close
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                waiting = False
        await asyncio.sleep(0)

# Run the game
asyncio.run(main())
