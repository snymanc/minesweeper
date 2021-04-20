import random
import re

# create a board object to start a new game


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # creating board
        # helper functions!
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initialize a set to keep track of which locations that has bee uncovered
        # save (row,col) tuples into this set
        self.dug = set()  # if we dig at 0,0, then self.dug = {(0,0)}

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # construct the list of lists (2-D board)

        # generate a new board
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]
        # array representation that represents a board:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None]]

        # plant bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            # return a random integer N suc tat a <= N <= b
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # bomb already planted
                continue

            board[row][col] = '*'  # plant bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # assgin a number 0-8 for all empty spaces, this represents number of neighboring bombs
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # don't calculate if bomb is present
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # iterate through each neighboring position and sum number of bombs
        # top left: (row-1, col-1)    | top middle: (row-1, col)    | top right: (row-1, col+1)
        # left: (row, col-1)          | current index               | right: (row, col+1)
        # bottom left: (row+1, col-1) | bottom middle: (row+1, col) | bottom right: (row+1, col+1)

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # current index
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location
        # return False if bomb else True

        # scenarios:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors

        self.dug.add((row, col))  # keeping track of dig

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue  # already dugged
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # magic function that prints this objects
        # prints what function returns
        # returns a string that shows a board to the player

        # create a new array that represents what the user would see
        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


# play the game
def play(dim_size=10, num_bombs=10):
    # 1) create the board and plant bombs
    board = Board(dim_size, num_bombs)

    # 2) show the user the the board and ask where the want to dig
    # 3-a) if location is a bomb, show game over message
    # 3-b) if location is not a bomb, dig recursively until each square is at least next to a bomb
    # 4) repeat 2 and 3 until there are no more place to dig

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location Try again?")
            continue

        # dig if valid
        safe = board.dig(row, col)
        if not safe:
            break  # bomb, game over!

    # break out of loop
    if safe:
        print("You have cleared this land of all it bombs!!!")
    else:
        print("o+< :(")
        # reveal the board
        board.dug = [(r, c) for r in range(board.dim_size)
                     for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    play()
