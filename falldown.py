import uvage
import random

camera = uvage.Camera(800, 600)

player_width = 20
player_height = 20
player_speed = 5

screen_width = 800
gap_size = 40

floor_width = screen_width - gap_size
floor_gap = 40
floor_speed = -1
floor_height = 20
floors = []
temp_floors = []


score = 0
frames_to_score_up = 0
frames_to_spawn_floor = 50
gravity = 0.4
game_on = True

floor1 = uvage.from_color(random.randint(0, int(floor_width)), 600, 'black', floor_width, floor_height)
floor2 = uvage.from_color(random.randint(int(floor_width + gap_size), 800), 600, 'black', floor_width, floor_height)

player = uvage.from_color(400, 15, 'red', player_width, player_height)
score_display = uvage.from_text(30, 30, str(score), 50, 'red')
game_over = uvage.from_text(400, 300, 'GAME OVER', 100, 'red', True)
player.speedx = 0
player.speedy = player_speed


def player_move():
    global floors
    right_boundary = screen_width
    left_boundary = 0
    player.move_speed()
    touching_floor = False

    for floor in floors:
        if player.bottom_touches(floor):
            touching_floor = True
            player.speedy = 0

    if not touching_floor and not player.y == 10:
        player.speedy += gravity

    if player.y > 590:
        player.speedy = 0
        player.move_speed()

    if uvage.is_pressing('right arrow'):
        if player.x + player_width / 2 < right_boundary:  # Check right boundary
            player.x += player_speed
    if uvage.is_pressing('left arrow'):
        if player.x - player_width / 2 > left_boundary:  # Check left boundary
            player.x -= player_speed


def floor_move():
    global floors

    for floor in floors:
        if player.y == 10 and player.touches(floor):
            floor.speedy = 0
            player.speedy = 0
        elif floor.y > 10:
            floor.speedy = floor_speed

        floor.move_speed()
        if player.touches(floor):
            player.move_to_stop_overlapping(floor)


def game_status():
    global game_on
    if player.y == 10:
        game_on = False


def score_counter():
    global score, score_display, frames_to_score_up
    if player.y > 10 and frames_to_score_up == 60:
        score += 1
        score_display = uvage.from_text(30, 30, str(score), 50, 'red')
        frames_to_score_up = 0
    else:
        frames_to_score_up += 1

def tick():
    global frames_to_spawn_floor
    camera.clear('white')
    game_status()

    if game_on:
        player_move()

        if frames_to_spawn_floor >= 50:
            floor1_x = random.randint(int(-floor_width/2), int(floor_width/2))
            floor2_x = floor1_x + floor_width + gap_size

            new_floor1 = uvage.from_color(floor1_x, 600, 'black', floor_width, floor_height)
            new_floor2 = uvage.from_color(floor2_x, 600, 'black', floor_width, floor_height)

            floors.append(new_floor1)
            floors.append(new_floor2)

            frames_to_spawn_floor = 0
        else:
            frames_to_spawn_floor += 1

        temp_floors = []
        for floor in floors:
            floor.y -= 1
            if floor.y + floor_height > 0:
                temp_floors.append(floor)
            camera.draw(floor)

        floors[:] = temp_floors


        floor_move()


        score_counter()
        camera.draw(player)
        camera.draw(score_display)
    else:
        camera.draw(game_over)

    camera.display()

uvage.timer_loop(60, tick)
