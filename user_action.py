from input import input_to, Get
import glob


def make_move():
    c = input_to(Get())

    if c == 'a':
        glob.paddle.move_relative(glob.board.matrix, -1)

    if c == 'd':
        glob.paddle.move_relative(glob.board.matrix, 1)

    if c == 'e':
        glob.paddle.release_ball()

    if c == 'y':
        glob.level += 1
        glob.init()

    if c == 'q':
        print('game aborted')
        quit()
