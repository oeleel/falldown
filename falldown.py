import uvage
import random

camera = uvage.Camera(800, 600)

player_width = 20
player_height = 20
player_speed = 10
floor_gap = 40
screen_width = 800
floor_speed = -1
player_on_floor_speed = 5
game_on = True

player = uvage.from_color(400, 15, 'red', player_width, player_height)
floor = uvage.from_color(400, 300, 'black', 400, 20)
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
        floor = uvage.from_color(400, 300, 'black', 400, 20)
        camera.draw(floor)

def game_status():
    if player.y == 10:
        game_on = False
        print(game_on)
def tick():
    camera.clear('white')
    game_status()
    player_move()
    #spawn_floors()
    floor_move()
    if camera.mouseclick:
        player.center = camera.mouse
    camera.draw(player)
    camera.draw(floor)
    camera.display()


uvage.timer_loop(30, tick)
