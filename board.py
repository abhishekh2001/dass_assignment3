import config


class Board:
    def __init__(self):
        self._height = config.board_height
        self._width = config.board_width
        self.matrix = [[' ' for _ in range(self._width)] for __ in range(self._height)]

    def render(self):
        print('—'*self._width)
        print('\n'.join(''.join(self.matrix[row]) for row in range(self._height)))
        print('—'*self._width)
