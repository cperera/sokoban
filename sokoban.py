#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
import copy
import os

# We decided to use letters for input
class Sokoboard:
    moves = {
            "n": [-1,0],
            "s": [1,0],
            "e": [0,1],
            "w": [0,-1]
    }

    def __init__(self,raw):
        self.board = []
        self.player = [0,0]
        start = 0
        row_num = 0
        line = raw.find('\n')
        
        while line != -1:
            row = raw[start:line]
            player_x = row.find("@")
            if player_x > 0:
                self.player = [row_num,player_x]
            else:
                player_x = row.find("+")
                if player_x > 0:
                    self.player = [row_num,player_x]

            row.find("+") != -1
            self.board = self.board + [[char for char in row]]
            start = line + 1
            row_num += 1
            line = raw.find('\n',start)
        self.board += [[char for char in raw[start:]]]

    def is_valid_move(self, direction):
        next_location = add_vectors(self.player, self.moves[direction])
        if (self.get_square_at_location(next_location) == "$"):
            next_next_location = add_vectors(next_location, self.moves[direction])
            if self.get_square_at_location(next_next_location) == "$":
                return False
            elif self.get_square_at_location(next_next_location) == "#":
                return False
        return self.get_square_at_location(next_location) != "#"

    def get_square_at_location(self, location):
        return self.board[location[0]][location[1]]

    def won(self):
        for row in self.board[1:-1]:
            if "$" in row:
                return False
        return True

    def move(self, direction):
        newBoard = copy.deepcopy(self.board)
        player_destination = "@"
        player_origin = " "
        if self.get_square_at_location(self.player) == "+":
            player_origin = "."
        self._set_location(newBoard, self.player, player_origin)
        next_location = add_vectors(self.player, self.moves[direction])
        if self.get_square_at_location(next_location) == "$":
            next_next_location = add_vectors(next_location, self.moves[direction])
            box_destination = "$"
            if self.get_square_at_location(next_next_location) == ".":
                box_destination = "*"
            self._set_location(newBoard, next_next_location, box_destination)
        elif self.get_square_at_location(next_location) == ".":
            player_destination = "+"
        self._set_location(newBoard, next_location, player_destination)
        return Sokoboard.from_board(newBoard)
        

    def _set_location(self, board, location, value):
        board[location[0]][location[1]] = value
        return board

    def to_string(self):
        return "\n".join(["".join(row) for row in self.board])

    @classmethod
    def from_board(cls, board):
        return cls("\n".join(["".join(row) for row in board]))


# When calls, prompts user for input and returns a valid (but not necessarily legal) direction
def next_step(board, message = ""):
    os.system('cls' if os.name == 'nt' else 'clear')
    print board.to_string()
    if message:
        print message
    test = raw_input("Please enter a letter for movement. One of n, s, e, w (representing north, south, east, and west)\n")
    if (not test in ["n", "s", "e", "w"]):
        return next_step(board, message = "That's not a valid input.")
    return test

def add_vectors(vector1, vector2):
    return [x + vector2[i] for (i, x) in enumerate(vector1)]

def run_test(message, actual, expected):
    if (actual != expected):
        print message

def main(level = ""):
    testboard8 = """######
#.$  #
#   @#
######"""
    if not level:
        level = testboard8
    sok = Sokoboard(level)

    while not sok.won():
        #print sok.to_string()
        step = next_step(sok)
        while not sok.is_valid_move(step):
            step = next_step(sok, message = "That is not a valid move")
        sok = sok.move(step)

    os.system('cls' if os.name == 'nt' else 'clear')
    print sok.to_string()    
    
    print "You won!!!"

if __name__ == '__main__':
    testlevel = """#####
#@$.#
#####"""
    print "We're going to try this level:"
    print testlevel

    sok = Sokoboard(testlevel)
    print "board \n", sok.board
    print "player at ", sok.player

    run_test("Should be able to move east into box with goal on other side", sok.is_valid_move("e"), True)
    run_test("Should not be able to move west into wall", sok.is_valid_move("w"), False)
    run_test("Should not be able to move south into wall", sok.is_valid_move("s"), False)

    run_test("This game is not yet won", sok.won(), False)

    testlevel1_1 = """#####
# @*#
#####"""
    sok1_1 = sok.move("e")
    run_test("After the move 'e', board should be\n" + testlevel1_1, sok1_1.to_string(), testlevel1_1)

    testlevel2 = """#####
#.$@#
#.$ #
#####"""
    sok2 = Sokoboard(testlevel2)
    run_test("Should not be able to move East into wall", sok2.is_valid_move("e"), False)
    run_test("Should be able to move West into box with goal on other side", sok2.is_valid_move("w"), True)
    run_test("Should not be able to move north into wall", sok2.is_valid_move("n"), False)
    run_test("Should be able to move south into empty space", sok2.is_valid_move("s"), True)

    testlevel3 = """#####
#.. #
#$$@#
#   #
#####"""
    sok3 = Sokoboard(testlevel3)
    run_test("Should not be able to move west into box when box on other side", sok3.is_valid_move("w"), False)
    testlevel4 = """####
#@$#
####"""
    sok4 = Sokoboard(testlevel4)
    run_test("Should not be able to move east into box when wall on other side", sok4.is_valid_move("e"), False)

    testlevel5 = """####
#@*#
####"""
    sok5 = Sokoboard(testlevel5)
    run_test("Game is won when all boxes are in goal squares", sok5.won(), True)

    testlevel6_0 = """######
#. $@#
######"""
    sok6 = Sokoboard(testlevel6_0)
    sok6_1 = sok6.move("w")
    run_test("If player moves off empty square, square becomes empty", sok6_1.get_square_at_location([1,4]), " ")
    run_test("If player moves off empty square, player moves", sok6_1.get_square_at_location([1,3]), "@")
    run_test("If player pushes box into empty square, box moves into empty square", sok6_1.get_square_at_location([1,2]), "$")

    testlevel7 = """######
#@.$ #
#    #
######"""
    sok7 = Sokoboard(testlevel7)
    sok7_1 = sok7.move("e")
    run_test("If player moves onto goal, goal is still there underneath", sok7_1.get_square_at_location([1,2]), "+")

    testlevel8 = """######
# +$ #
#    #
######"""
    sok8 = Sokoboard(testlevel8)
    sok8_1 = sok8.move("s")
    run_test("If player moves off of goal, goal is still in previous space", sok8_1.get_square_at_location([1,2]),".")

    # Restart input
    minicosmos01 = """  #####
###   #
# $ # ##
# #  . #
#    # #
## #   #
 #@  ###
 #####  """
    minicosmos02 = """  #####
###   #
# $ # ##
# #  . #
#    # #
##$#.  #
 #@  ###
 #####  """
    levels = [minicosmos01, minicosmos02]
    for level in levels:
        main(level)