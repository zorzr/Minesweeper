from random import randint
BOMB = 100


class Tile:
    def __init__(self):
        self.value = 0
        self.covered = True
        self.marked = False

    def is_bomb(self):
        return bool(self.value == BOMB)


class Board:
    def __init__(self, rows, cols, bombs=None):
        self.rows = rows
        self.cols = cols
        self.tiles = [Tile() for _ in range(rows*cols)]

        self.bombs = []
        self.marks = []
        self.exploded = None
        self.init(bombs) if bombs else None

    def get(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            return self.tiles[i*self.cols + j]
        return None

    def init(self, bombs):
        if bombs < 0 or bombs > self.rows * self.cols:
            return

        n = 0
        while n < bombs:
            x = randint(0, self.rows-1)
            y = randint(0, self.cols-1)
            picked = self.tiles[x * self.cols + y]

            if picked.is_bomb():
                continue
            else:
                picked.value = BOMB
                self.bombs.append((x, y))
                n += 1

        for bomb in self.bombs:
            i = bomb[0]
            j = bomb[1]
            for x in range(max(i-1, 0), min(i+2, self.rows)):
                for y in range(max(j-1, 0), min(j+2, self.cols)):
                    current = self.tiles[x*self.cols + y]
                    if not current.is_bomb():
                        current.value += 1

    def expose(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            tile = self.tiles[i*self.cols + j]
            tile.covered = False

            if tile.is_bomb():
                self.exploded = (i, j)
                return

            if tile.value == 0:
                for x in range(max(i-1, 0), min(i+2, self.rows)):
                    for y in range(max(j-1, 0), min(j+2, self.cols)):
                        self.expose(x, y) if self.tiles[x*self.cols + y].covered else None

    def mark(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            tile = self.tiles[i*self.cols + j]

            if tile.covered:
                self.marks.remove((i, j)) if tile.marked else self.marks.append((i, j))
                tile.marked = not tile.marked

    def status(self):
        if self.exploded:
            return -1
        if set(self.bombs) == set(self.marks):
            return 1
        return 0
