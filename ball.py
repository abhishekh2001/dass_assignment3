from component import Component
import config
import glob


class Ball(Component):
    def __init__(self, x, y, xvel, yvel, representation=[['o']], free=0, speed=1):
        """
        Ball component
        :param x: x position
        :param y: y position
        :param xvel: velocity in the x direction
        :param yvel: velocity in the y direction
        :param representation: representation of ball in matrix
        :param speed: interval between ball movements. Keep it less than input timeout
        """
        super().__init__(x, y, representation)
        self._xvel = xvel
        self._yvel = yvel
        self._speed = speed
        self.is_free = free

    def set_is_free(self, free):
        self.is_free = free

    def get_is_free(self):
        return self.is_free

    def set_speed(self, speed):
        self._speed = min(max(speed, 0.09), 0.6)

    def get_speed(self):
        return self._speed

    def set_xvel(self, xvel):
        self._xvel = max(-2, min(xvel, 2))

    def get_xvel(self):
        return self._xvel

    def set_yvel(self, yvel):
        self._yvel = yvel

    def get_yvel(self):
        return self._yvel

    def move_relative(self, board, x_diff=0, y_diff=0):
        """
        Sets new position relative to current position of paddle
        :param board: matrix storing the board
        :param x_diff: delta by which the position of ball changes in the x-axis
        :param y_diff: delta by which the position of ball changes in the y-axis
        """
        self.clear(board)

        new_pos_x = self._x + x_diff
        if new_pos_x >= 0 and new_pos_x + self._width <= config.board_width:
            self.set_x(new_pos_x)

        if new_pos_x <= 0 or new_pos_x >= config.board_width:
            self.set_xvel(-self._xvel)

        new_pos_y = self._y + y_diff
        if new_pos_y >= 0 and new_pos_y + self._height <= config.board_height:
            self.set_y(new_pos_y)

        if new_pos_y == 0:
            self.set_yvel(-self._yvel)

    def handle_paddle_collision(self, paddle):
        """
        Sets the velocities of the ball after collision
        :param paddle: the paddle instance
        :return: False if ball is lost and true otherwise
        """
        if paddle.get_x() <= self._x <= paddle.get_x() + paddle.get_width() and \
                self._y == paddle.get_y() - 1:
            self.set_yvel(-self._yvel)
            self.set_relative_velocity(x_vel_diff=(self._x - paddle.get_center_x_coordinate()))
            if paddle.get_grab():
                paddle.hold_ball(self)
            if glob.bricks_fall:
                glob.move_all_bricks_down()
            return True
        elif self._y >= paddle.get_y():
            return False

        return True

    def set_relative_velocity(self, x_vel_diff=0, y_vel_diff=0):
        """
        Sets change in relative velocity of ball from current velocity
        :param x_vel_diff: Difference by which x-velocity is to be changed
        :param y_vel_diff: Difference by which y-velocity is to be changed
        """
        # self._xvel += x_vel_diff
        self.set_xvel(self.get_xvel() + x_vel_diff)
        self._yvel += y_vel_diff
