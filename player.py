class Player:
    def __init__(self):
        self._lives = 5
        self._points = 0

    def get_lives(self):
        return self._lives

    def set_lives(self, value):
        self._lives = value

    def lose_life(self):
        self._lives -= 1

    def get_points(self):
        return self._points

    def set_points(self, value):
        self._points = value

    def increment_points_by(self, value):
        self._points += value

    def increment_points(self):
        self._points += 1
