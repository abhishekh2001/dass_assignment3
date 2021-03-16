from brick import Brick
import glob


class ExplodingBrick(Brick):
    def __init__(self, x, y):
        super(ExplodingBrick, self).__init__(x, y, 4, ['BBBB'])

    def get_nearby_bricks(self):
        """
        Given all an array of bricks, return all bricks that are in contact with current brick
        :return: array of bricks in contact with this one
        """
        return list(filter(lambda b: b != self and self.overlap(b), glob.bricks))

    def chain_explosions(self):
        self.destroy(glob.board.matrix)
        neighbors = self.get_nearby_bricks()
        for brick in neighbors:
            if brick.get_brick_type() == 4 and brick.get_health():
                glob.player.increment_points_by(brick.get_score())
                brick.chain_explosions()
            if brick.get_brick_type() != 4 and brick.get_health():
                glob.spawn_powerup(brick.get_x(), brick.get_y())
                glob.player.increment_points_by(brick.get_score())
            brick.destroy(glob.board.matrix)
