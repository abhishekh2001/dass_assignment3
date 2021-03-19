from ball import Ball
import glob
import time
from boss import Boss


def bounce_ball(brick, ball):
    """
    Given a brick and a ball, determine motion of ball and consequence of hitting the brick
    :param brick: brick instance
    :param ball: ball instance
    :return: True on impact and False otherwise
    """
    if brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width() - 1 and ball.get_y() != brick.get_y():
        if ball.get_y() <= brick.get_y():
            if not glob.is_thru_ball():
                if ball.get_yvel() > 0:
                    ball.set_yvel(-abs(ball.get_yvel()))
                    glob.handle_impact(brick)
            else:
                glob.handle_impact(brick)
            return True
        elif ball.get_y() >= brick.get_y() + brick.get_height():
            if not glob.is_thru_ball():
                if ball.get_yvel() <= 0:
                    ball.set_yvel(abs(ball.get_yvel()))
                    glob.handle_impact(brick)
            else:
                glob.handle_impact(brick)
            return True
    elif brick.get_y() <= ball.get_y() <= brick.get_y() + brick.get_height() - 1 and \
            (not brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width()):
        if ball.get_x() <= brick.get_x():
            if not glob.is_thru_ball():
                ball.set_xvel(-abs(ball.get_xvel()))
            glob.handle_impact(brick)
            return True
        elif ball.get_x() >= brick.get_x() + brick.get_width():
            if not glob.is_thru_ball():
                ball.set_xvel(abs(ball.get_xvel()))
            glob.handle_impact(brick)
            return True
    elif (brick.get_x() <= ball.get_x() + ball.get_xvel() <= brick.get_x() + brick.get_width() - 1 and
            brick.get_y() <= ball.get_y() + ball.get_yvel() <= brick.get_y() + brick.get_height() - 1) or \
            (brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width() - 1 and
             brick.get_y() <= ball.get_y() <= brick.get_y() + brick.get_height() - 1):
        if not glob.is_thru_ball():
            ball.set_xvel(-ball.get_xvel())
            ball.set_yvel(-ball.get_yvel())
        glob.handle_impact(brick)
        return True


def bounce_ball_boss(brick, ball):
    """
    Given a brick and a ball, determine motion of ball and consequence of hitting the brick
    :param brick: boss instance
    :param ball: ball instance
    :return: True on impact and False otherwise
    """
    if brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width() - 1 and ball.get_y() != brick.get_y():
        if ball.get_y() <= brick.get_y():
            if ball.get_yvel() > 0:
                ball.set_yvel(-abs(ball.get_yvel()))
            return True
        elif ball.get_y() >= brick.get_y() + brick.get_height():
            if ball.get_yvel() <= 0:
                ball.set_yvel(abs(ball.get_yvel()))
            return True
    elif brick.get_y() <= ball.get_y() <= brick.get_y() + brick.get_height() - 1 and \
            (not brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width()):
        if ball.get_x() <= brick.get_x():
            ball.set_xvel(-abs(ball.get_xvel()))
            return True
        elif ball.get_x() >= brick.get_x() + brick.get_width():
            ball.set_xvel(abs(ball.get_xvel()))
            glob.handle_impact(brick)
            return True
    elif (brick.get_x() <= ball.get_x() + ball.get_xvel() <= brick.get_x() + brick.get_width() - 1 and
            brick.get_y() <= ball.get_y() + ball.get_yvel() <= brick.get_y() + brick.get_height() - 1) or \
            (brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width() - 1 and
             brick.get_y() <= ball.get_y() <= brick.get_y() + brick.get_height() - 1):
        ball.set_xvel(-ball.get_xvel())
        ball.set_yvel(-ball.get_yvel())
        return True


def handle_ball_brick_collision(ball):
    """
    For any given ball, determine if ball collides with any brick
    :param ball:
    :return:
    """
    for brick in glob.bricks:
        if brick.get_x() - 1 <= ball.get_x() <= brick.get_x() + brick.get_width() and \
                brick.get_y() - 1 <= ball.get_y() <= brick.get_y() + brick.get_height():
            if bounce_ball(brick, ball):
                break
    glob.bricks = list(filter(lambda b: b.get_health(), glob.bricks))


def handle_ball_ufo_collision(ball):
    """
    For any given ball, determine if ball collides with any brick
    :param ball:
    :return:
    """
    if glob.boss.get_x() - 1 <= ball.get_x() <= glob.boss.get_x() + glob.boss.get_width() and \
            glob.boss.get_y() - 1 <= ball.get_y() <= glob.boss.get_y() + glob.boss.get_height():
        if bounce_ball_boss(glob.boss, ball):
            glob.boss.lose_health()
    glob.bricks = list(filter(lambda b: b.get_health(), glob.bricks))


class Balls:
    def __init__(self):
        self._balls = []

    def add_ball(self, x, y, xvel, yvel, representation=[['o']], free=0, speed=1):
        ball = Ball(x, y, xvel, yvel, representation, free, speed)
        self._balls.append(ball)

    def remove_all(self):
        self._balls = []

    def get_number_balls(self):
        return len(self._balls)

    def get_balls(self):
        return self._balls

    def remove_half(self):
        self._balls = self._balls[:max(1, len(self._balls)//2)]

    def move_all(self):
        pbt = glob.prev_ball_timestamp
        flag = False
        for ball in list(self._balls):
            if ball.is_free and time.time() - pbt >= ball.get_speed():
                flag = True
                handle_ball_brick_collision(ball)
                handle_ball_ufo_collision(ball)
                ball.move_relative(glob.board.matrix, ball.get_xvel(), ball.get_yvel())
                ret = ball.handle_paddle_collision(glob.paddle)
                if not ret:
                    self._balls.remove(ball)
            if not len(self._balls):
                glob.player.lose_life()
                glob.player.set_points(0)
                glob.init()
        # TODO: use handle_ball_ufo_collision
        if flag:
            pbt = time.time()
        glob.prev_ball_timestamp = pbt
        return pbt

    def render_all(self, board):
        for ball in self._balls:
            ball.render(board)

    def clear_all(self, board):
        for ball in self._balls:
            ball.clear(board)
