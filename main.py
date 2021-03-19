from modules import *
import colorama
from glob import board, prev_powerup_timestamp, move_powerups, \
    deactivate_powerups
import glob
import user_action
import config

colorama.init()
glob.init()
start_time = time.time()
max_points = 0

while glob.player.get_lives() and glob.level <= 3:
    # Move paddle
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')

    # Perform motion and functionalities
    glob.trigger_time_attack()
    glob.balls.move_all()
    glob.lasers.move_all()
    prev_powerup_timestamp = move_powerups(prev_powerup_timestamp)
    glob.paddle.shoot()
    if glob.boss:
        glob.boss.move_with_paddle()
    deactivate_powerups()

    for brick in glob.bricks:
        if brick.get_rainbow():
            brick.set_brick_type(random.choice([1, 2, 3]))

    # Render screen elements
    glob.balls.render_all(board.matrix)
    glob.lasers.render_all(board.matrix)
    for brick in glob.bricks:
        brick.render(board.matrix)
    for brick in glob.boss_bricks:
        brick.render(board.matrix)
    for powerup in glob.powerups:
        powerup.render(board.matrix)
    if glob.boss:
        glob.boss.render(board.matrix)
        glob.boss.drop_bomb()
    if glob.bomb:
        glob.bomb.clear(board.matrix)
        glob.bomb.render(board.matrix)
        to_disappear = glob.bomb.move_down()
        if to_disappear:
            glob.bomb.clear(board.matrix)
            glob.bomb = None

    glob.paddle.render(board.matrix)

    glob.max_points = max(glob.player.get_points(), glob.max_points)

    print('Life: ', glob.player.get_lives())
    print('Score: ', glob.player.get_points())
    print('Time: ', str(int(time.time() - start_time)), 's')
    if not glob.paddle.get_shooting():
        print()
    else:
        print('Time left:', int(config.shooting_duration - (time.time() - glob.paddle.get_shooting_start())))
    if glob.boss:
        print("Boss HP", glob.boss.get_health(), end=' ')
        print("▇"*glob.boss.get_health())
    else:
        print()

    glob.board.render()

    if glob.level == 3 and glob.boss.get_health() <= 0:
        glob.player.set_points(glob.player.get_points() + 100)
        glob.max_points = max(glob.player.get_points() + 100, glob.max_points)
        break

    if not len(list(filter(lambda b: b.get_brick_type() != -1, glob.bricks))):
        if glob.level < 3:
            glob.level += 1
            glob.init()

    if glob.level < 3 and (len(glob.bricks) and max(list(map(lambda x: x.get_y(), glob.bricks))) >= config.board_height - 2):
        print('quitting here')
        break

# os.system('clear')
print('Game over')
print('Max score is ', glob.max_points)
