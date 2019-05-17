from random import randint
from game import Board
import argparse
import signal
import os


def show(board):
    for i in range(board.rows):
        for j in range(board.cols):
            tile = board.tiles[i*board.cols+j]
            tile_str = "□"
            if tile.marked:
                tile_str = "M"
            if not tile.covered:
                if tile.is_bomb():
                    tile_str = "X"
                else:
                    tile_str = str(tile.value)

            print(tile_str, end="\t")
        print()


def solution(board):
    for i in range(board.rows):
        for j in range(board.cols):
            tile = board.tiles[i*board.cols + j]
            tile_str = str(tile.value)
            if tile.is_bomb():
                tile_str = "X"

            print(tile_str, end="\t")
        print()


def safe_start(board):
    useful_tiles = []
    for i in range(board.rows*board.cols):
        if board.tiles[i].value == 0:
            x = int(i / board.cols)
            y = i % x
            useful_tiles.append((x, y))

    if len(useful_tiles) == 0:
        for i in range(board.rows * board.cols):
            if not board.tiles[i].is_bomb():
                x = int(i / board.cols)
                y = i % x
                useful_tiles.append((x, y))

    e = randint(0, len(useful_tiles)-1)
    tile = useful_tiles[e]
    board.expose(tile[0], tile[1])


def clear():
    os.system("cls" if os.name == 'nt' else "clear")


def interrupt(sig, fr):
    print()
    exit(1)


def check_value(value):
    integer = int(value)
    if integer < 2:
        raise argparse.ArgumentTypeError("Invalid value %s (must be greater than 2)" % value)
    return integer


def check_bombs():
    if args.bombs > args.rows*args.cols - 2 or args.bombs < 1:
        print("Invalid number of bombs: %s" % args.bombs)
        exit(0)


def run():
    game = Board(args.rows, args.cols, args.bombs)
    win = False

    while not game.exploded:
        clear()
        show(game)
        action = input("Action: ")
        command = action.split(" ")

        action = action.lower()
        if action == "q" or action == "quit" or action == "exit":
            exit(0)
        elif len(command) != 3:
            continue

        if command[0] == 'E':
            game.expose(int(command[1])-1, int(command[2])-1)
        elif command[0] == 'M':
            game.mark(int(command[1])-1, int(command[2])-1)

        if game.status() == 1:
            win = True
            break

    clear()
    show(game)
    print("Congratulations!") if win else print("Game over")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Minesweeper Python game')
    parser.add_argument('rows', metavar='rows', type=check_value, nargs='?', default=5,
                        help='number of rows of the game field (default: 5)')
    parser.add_argument('cols', metavar='cols', type=check_value, nargs='?', default=5,
                        help='number of columns of the game field (default: 5)')
    parser.add_argument('bombs', metavar='bombs', type=int, nargs='?', default=4,
                        help='number of bombs to discover (default: 4)')
    args = parser.parse_args()
    check_bombs()

    signal.signal(signal.SIGINT, interrupt)
    run()
