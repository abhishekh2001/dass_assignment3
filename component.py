
class Component:
    def __init__(self, x, y, representation):
        self._x = x
        self._y = y
        self._width = len(representation[0])
        self._height = len(representation)
        self._representation = representation

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_representation(self):
        return self._representation

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_pos(self, x, y):
        self._x = x
        self._y = y

    def set_representation(self, repr):
        self._width = len(repr[0])
        self._height = len(repr)
        self._representation = repr

    def clear(self, board):
        for row in range(self._height):
            for col in range(self._width):
                board[self._y + row][self._x + col] = ' '

    def render(self, board):
        for row in range(self._height):
            for col in range(self._width):
                board[self._y + row][self._x + col] = self._representation[row][col]
