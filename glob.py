import random
from board import Board
from paddle import Paddle
from brick import Brick
import time
from powerup import PowerUp, ExpandPaddle, ShrinkPaddle, PaddleGrab, type_repr_map, \
    FastBall, ThruBall, BallMultiplier, ShootingPaddle
import config
from player import Player
from balls import Balls
from laser import Lasers
from explodingBricks import ExplodingBrick
from boss import Boss
from bomb import Bomb


player = Player()
max_points = 0

can_spawn_powerups = True
board = Board()
paddle = None
balls = Balls()
lasers = Lasers()
powerups = []
to_activate_powerups = []
active_powerups = []
bricks = []
boss_bricks = []
level = 1


boss = None
bomb = None

prev_ball_timestamp = time.time()
prev_powerup_timestamp = time.time()
time_attack = time.time()
bricks_fall = False

gravity_timestamp = 0
accel_y = 1


def clear_screen():
    global bomb
    global boss
    if paddle:
        paddle.clear(board.matrix)
    for ball in balls.get_balls():
        ball.clear(board.matrix)
    for powerup in powerups:
        powerup.clear(board.matrix)
    for laser in lasers.get_lasers():
        laser.clear(board.matrix)
    for brick in bricks:
        brick.clear(board.matrix)
    if bomb:
        bomb.clear(board.matrix)
        bomb = None
    if boss:
        boss.clear(board.matrix)
        boss = None

def init():
    global paddle
    global bricks
    global powerups
    global can_spawn_powerups
    global active_powerups
    global to_activate_powerups
    global balls
    global prev_ball_timestamp
    global prev_powerup_timestamp
    global active_powerups
    global time_attack
    global bricks_fall
    global gravity_timestamp
    global boss
    global boss_bricks

    clear_screen()
    balls.remove_all()
    lasers.remove_all()

    paddle = Paddle(8, width=5)
    balls.add_ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2,
                   free=True)
    paddle.hold_ball(balls.get_balls()[0])

    powerups = []
    to_activate_powerups = []
    active_powerups = []

    bricks = []
    if level == 1:
        for y, j in zip(range(4, 13, 2), range(10, 40, 6)):
            bricks.append(Brick(j, y, random.choice([-1, 1, 2, 3]), ['BBBB']))
        for y, j in zip(range(12, 3, -2), range(40, 70, 6)):
            bricks.append(Brick(j, y, random.choice([-1, 1, 2, 3]), ['BBBB']))

        for brick in bricks:
            if random.random() < 0.3:
                brick.set_rainbow(True)

    if level == 2:
        for y in range(4, 9, 4):
            for j in range(10, 100, 10):
                # bricks.append(Brick(j, y, -1, ['BBBBB']))
                bricks.append(Brick(j, y, random.choice([-1, 1, 2, 3]), ['BBBB']))

        for x in range(40, 55, 4):
            bricks.append(ExplodingBrick(x, 14))
        bricks.append(ExplodingBrick(36, 13))
        bricks.append(ExplodingBrick(56, 13))
        bricks.append(Brick(45, 13, 2, ['BBBB']))

    if level == 3:
        for y, j in zip(range(8, 17, 2), range(10, 50, 11)):
            bricks.append(Brick(j, y, -1, ['BBBB']))
        for y, j in zip(range(14, 7, -2), range(60, 110, 11)):
            bricks.append(Brick(j, y, -1, ['BBBB']))

        can_spawn_powerups = False
        boss = Boss(paddle.get_x(), 0)
        
        for b in boss_bricks:
            b.clear(board.matrix)
        boss_bricks = []

    prev_ball_timestamp = time.time()  # Improve
    prev_powerup_timestamp = time.time()
    time_attack = time.time()
    bricks_fall = False

    gravity_timestamp = time.time()


def start_new_life():
    global balls
    global powerups
    global to_activate_powerups
    global active_powerups
    global paddle
    global boss_bricks
    clear_screen()

    balls.remove_all()

    paddle = Paddle(8, width=5)
    balls.add_ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2,
                   free=True)
    paddle.hold_ball(balls.get_balls()[0])

    powerups = []
    to_activate_powerups = []
    active_powerups = []

    for b in boss_bricks:
        b.clear(board.matrix)
    boss_bricks = []


def spawn_powerup(x, y):
    if  can_spawn_powerups and random.random() <= config.prob_powerup:
        p_type = random.choice([1, 2, 3, 4, 5, 6])
        p_type = 7
        xvel, yvel = 1, -1
        if p_type == 1:
            powerups.append(ExpandPaddle(x, y, xvel, yvel))
        elif p_type == 2:
            powerups.append(ShrinkPaddle(x, y, xvel, yvel))
        elif p_type == 3:
            powerups.append(BallMultiplier(x, y, xvel, yvel))
        elif p_type == 4:
            powerups.append(FastBall(x, y, xvel, yvel))
        elif p_type == 5:
            powerups.append(ThruBall(x, y, xvel, yvel))
        elif p_type == 6:
            powerups.append(PaddleGrab(x, y, xvel, yvel))
        elif p_type == 7:
            powerups.append((ShootingPaddle(x, y, xvel, yvel)))


def spawn_bomb(x, y):
    global bomb
    bomb = Bomb(x, y)


def deactivate_powerups():
    for powerup in list(active_powerups):
        if time.time() - powerup.get_activation_time() >= powerup.get_deactivation_time():
            powerup.deactivate()
            active_powerups.remove(powerup)


def activate_powerups():
    global to_activate_powerups
    global active_powerups

    for powerup in to_activate_powerups:
        to_append = powerup.activate()
        if to_append:
            powerup.set_activation_time()
            active_powerups.append(powerup)

    to_activate_powerups = []


def is_thru_ball():
    return 5 in map(lambda x: x.get_type(), active_powerups)


def handle_impact(brick):
    """
    Behavior of brick on successful impact with ball
    :param brick: brick instance
    """
    if brick.get_rainbow():
        brick.set_rainbow(False)
    if brick.get_brick_type() == 4:
        brick.chain_explosions()
    elif is_thru_ball():  # if thru-ball is active, destroy brick
        brick.destroy(board.matrix)
        spawn_powerup(brick.get_x(), brick.get_y())
        player.increment_points_by(brick.get_score())  # increase points
    elif brick.got_hit(board.matrix):  # Brick has zero health -> is destroyed
        spawn_powerup(brick.get_x(), brick.get_y())
        player.increment_points_by(brick.get_score())  # increase player points


def move_powerups(ppt):
    """
    Responsible for moving all powerups and handling cases when user misses the powerup or catches it.
    :param ppt: previous powerup timestamp
    :return: value of powerup timestamp after current iteration
    """
    global powerups
    global gravity_timestamp
    flag = False
    for powerup in powerups:
        if time.time() - ppt >= powerup.get_speed():
            flag = True
            if powerup.is_caught_by_paddle(paddle):  # Check if powerup is caught
                to_activate_powerups.append(powerup)  # temporarily store powerups to activate
                powerup.set_status(config.powerup_status['ACTIVE'])  # Update status of caught powerup
            # powerup.move_relative(board.matrix, powerup.get_xvel(), powerup.get_yvel())
            # board.matrix[0][0] = str(powerup.get_yvel())
            if powerup.go_down(board.matrix):  # ** checks if powerup hit the board **
                powerup.set_status(config.powerup_status['MISSED'])  # User has missed the powerup
    if flag:
        ppt = time.time()

    # for powerup in powerups:
    #     if time.time() - powerup.get_last_moved_timestamp() >= 3:
    #         powerup.set_last_moved_timestamp(time.time())
    #         t = time.time() - powerup.get_grav_timestamp()
    #         powerup.clear(board.matrix)
    #         powerup.set_x(int(powerup.get_x() + powerup.get_xvel() * t))
    #         powerup.set_y(int(powerup.get_y() + powerup.get_yvel() * t + 0.5 * accel_y * t * t))

    powerups = list(filter(lambda p: p.get_status() == config.powerup_status['SPAWNED'], powerups))

    activate_powerups()

    return ppt


def move_all_bricks_down():
    for brick in bricks:
        brick.clear(board.matrix)
    for brick in bricks:
        brick.set_y(brick.get_y() + 1)


def trigger_time_attack():
    global bricks_fall
    if time.time() - time_attack >= config.time_attack_limit[level]:  # start time attack
        bricks_fall = True

