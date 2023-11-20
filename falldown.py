import uvage
import random

camera = uvage.Camera(800, 600)

player_width = 20
player_height = 20
player_speed = 10

screen_width = 800
gap_size = 30

floor_width = screen_width - gap_size
floor_gap = 40
floor_speed = -3

score = 0
frames_to_score_up = 0
game_on = True

player = uvage.from_color(400, 15, 'red', player_width, player_height)
floor = uvage.from_color(400, 300, 'black', 400, 20)
score_display = uvage.from_text(30, 30, str(score), 50, 'red')
game_over = uvage.from_text(400, 300, 'GAME OVER', 100, 'red', True)
player.speedx = 0
player.speedy = player_speed
floor.speedy = floor_speed


def player_move():
    player.move_speed()
    if player.touches(floor, 3):
        player.speedy = 0

    if not player.touches(floor, 3) and not player.y == 10:
        player.speedy = player_speed

    if player.y > 590:
        player.speedy = 0
        player.move_speed()

    if uvage.is_pressing('right arrow'):
        player.x += 5
    if uvage.is_pressing('left arrow'):
        player.x -= 5


def floor_move():
    if player.y == 10 and player.touches(floor):
        floor.speedy = 0
        player.speedy = 0
        floor.move_speed()
    if floor.y > 10:
        floor.move_speed()
        player.move_to_stop_overlapping(floor)
    else:
        floor.move_speed()


def spawn_floors():
    while game_on:
        floor1 = uvage.from_color(random.randint(0, floor_width), 300, 'black', 400, 20)
        camera.draw(floor)


def game_status():
    global game_on
    if player.y == 10:
        game_on = False




def score_counter():
    global score, score_display, frames_to_score_up
    if player.y > 10 and frames_to_score_up == 10:
        score += 1
        score_display = uvage.from_text(30, 30, str(score), 50, 'red')
        frames_to_score_up = 0
    else:
        frames_to_score_up += 1


def tick():
    camera.clear('white')
    game_status()
    if game_on is False:
        camera.draw(game_over)
    player_move()
    # spawn_floors()
    floor_move()
    score_counter()
    camera.draw(player)
    camera.draw(floor)
    camera.draw(score_display)
    camera.display()


uvage.timer_loop(30, tick)
