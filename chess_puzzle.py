import copy
import random


def create_dict_of_letters_to_num():  # Need to add type hints in Codio
    import string

    count = 1
    list_of_letters = list(string.ascii_lowercase)
    dict_of_num_to_letter = {}

    for letter in list_of_letters:
        dict_of_num_to_letter[letter] = count
        count = count + 1
    return dict_of_num_to_letter


def location2index(loc: str) -> tuple[int, int]:
    """converts chess location to corresponding x and y coordinates"""

    list_of_coords = []
    for elem in loc:
        list_of_coords.append(elem)
    dict_to_convert_letter_to_num = create_dict_of_letters_to_num()
    x = dict_to_convert_letter_to_num[list_of_coords[0]]
    y = loc[1:]
    tuple_of_coords = (x, int(y))
    return tuple_of_coords


def index2location(x: int, y: int) -> str:
    """converts  pair of coordinates to corresponding location"""
    dict_to_convert_letter_to_num = create_dict_of_letters_to_num()
    x = list(dict_to_convert_letter_to_num.keys())[
        list(dict_to_convert_letter_to_num.values()).index(x)
    ]  # finds the dictionary key (the letters) based on value
    y = str(y)
    x = str(x)
    return x + y


class Piece:
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values"""

        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.side_ = side_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    """checks if there is piece at coordinates pox_X, pos_Y of board B"""
    for piece in B[1]:
        if piece.pos_X == pos_X and piece.pos_Y == pos_Y:
            return True
    else:
        return False


def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    """
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    """
    if is_piece_at(pos_X, pos_Y, B) == True:
        for piece in B[1]:
            if piece.pos_X == pos_X and piece.pos_Y == pos_Y:
                return piece


class Rook(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule4](see section Intro)
        Hint: use is_piece_at
        """
        diff_for_pos_x = abs(self.pos_X - pos_X)
        diff_for_pos_y = abs(self.pos_Y - pos_Y)

        piece_at_coords = None

        if is_piece_at(pos_X, pos_Y, B):
            piece_at_coords = piece_at(pos_X, pos_Y, B)

        if diff_for_pos_x == 0 or diff_for_pos_y == 0:
            if piece_at_coords != None and piece_at_coords.side_ == self.side_:
                return False

            elif diff_for_pos_x != 0 and pos_X > self.pos_X:
                for i in range(1, diff_for_pos_x + 1):
                    if (
                        is_piece_at(self.pos_X + i, self.pos_Y, B)
                        and piece_at(self.pos_X + i, self.pos_Y, B) != piece_at_coords
                    ):
                        return False
                else:
                    return True

            elif diff_for_pos_x != 0 and pos_X < self.pos_X:
                for i in range(1, diff_for_pos_x + 1):
                    if (
                        is_piece_at(self.pos_X - i, self.pos_Y, B)
                        and piece_at(self.pos_X - i, self.pos_Y, B) != piece_at_coords
                    ):
                        return False
                else:
                    return True

            elif diff_for_pos_y != 0 and pos_Y > self.pos_Y:
                for i in range(1, diff_for_pos_y + 1):
                    if (
                        is_piece_at(self.pos_X, self.pos_Y + i, B)
                        and piece_at(self.pos_X, self.pos_Y + i, B) != piece_at_coords
                    ):
                        return False
                else:
                    return True

            elif diff_for_pos_y != 0 and pos_Y < self.pos_Y:
                for i in range(1, diff_for_pos_y + 1):
                    if (
                        is_piece_at(self.pos_X, self.pos_Y - i, B)
                        and piece_at(self.pos_X, self.pos_Y - i, B) != piece_at_coords
                    ):
                        return False
                else:
                    return True
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule2] and [Rule4] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule5], use is_check on new board
        """
        if self.can_reach(pos_X, pos_Y, B):
            self.move_to(pos_X, pos_Y, B)
            if is_check(self.side_, B):
                return False
            else:
                return True

    def move_to(self, pos_X, pos_Y, B):
        piece_to_replace = None
        piece_to_replace = piece_at(pos_X, pos_Y, B)
        piece_to_add = piece_at(self.pos_X, self.pos_Y, B)
        index_PTA = 0
        changed_piece = False
        if piece_to_replace != None:
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    index_PTA = i
                    changed_piece = True
            if changed_piece:
                for i in range(len(B[1])):
                    if B[1][i] == piece_to_replace:
                        B[1][i] = piece_to_add
            del B[1][index_PTA]
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    B[1][i].pos_X = pos_X
                    B[1][i].pos_Y = pos_Y
            return B
        elif piece_to_replace == None:
            for piece in B[1]:
                if piece == self:
                    piece.pos_X = pos_X
                    piece.pos_Y = pos_Y
            return B


class Bishop(Piece):
    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """checks if this bishop can move to coordinates pos_X, pos_Y on board B according to rule [Rule1] and [Rule4]"""
        diff_for_x = abs(pos_X - self.pos_X)
        diff_for_y = abs(pos_Y - self.pos_Y)
        if diff_for_x == diff_for_y:
            if is_piece_at(pos_X, pos_Y, B):
                x = piece_at(pos_X, pos_Y, B)
                if self.side_ != x.side_:
                    for i in range(1, diff_for_x + 1):
                        if pos_X < self.pos_X and pos_Y > self.pos_Y:
                            if (
                                piece_at(self.pos_X - i, self.pos_Y + i, B)
                                and piece_at(self.pos_X - i, self.pos_Y + i, B) != x
                            ):
                                return False
                        elif pos_X > self.pos_X and pos_Y > self.pos_Y:
                            if (
                                piece_at(self.pos_X + i, self.pos_Y + i, B)
                                and piece_at(self.pos_X + i, self.pos_Y + i, B) != x
                            ):
                                return False
                        elif pos_X < self.pos_X and pos_Y < self.pos_Y:
                            if (
                                piece_at(self.pos_X - i, self.pos_Y - i, B)
                                and piece_at(self.pos_X - i, self.pos_Y - i, B) != x
                            ):
                                return False
                        elif pos_X > self.pos_X and pos_Y < self.pos_Y:
                            if (
                                piece_at(self.pos_X + i, self.pos_Y - i, B)
                                and piece_at(self.pos_X + i, self.pos_Y - i, B) != x
                            ):
                                return False
                    else:
                        return True
                return False
            elif is_piece_at(pos_X, pos_Y, B) == False:
                for i in range(1, diff_for_x + 1):
                    if pos_X < self.pos_X and pos_Y > self.pos_Y:
                        if is_piece_at(self.pos_X - i, self.pos_Y + i, B):
                            return False
                    elif pos_X > self.pos_X and pos_Y > self.pos_Y:
                        if is_piece_at(self.pos_X + i, self.pos_X + i, B):
                            return False
                    elif pos_X < self.pos_X and pos_Y < self.pos_Y:
                        if is_piece_at(self.pos_X - i, self.pos_Y - i, B):
                            return False
                    elif pos_X > self.pos_X and pos_Y < self.pos_Y:
                        if is_piece_at(self.pos_X + i, self.pos_Y - i, B):
                            return False
                else:
                    return True
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule2] and [Rule4] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule5], use is_check on new board
        """
        if self.can_reach(pos_X, pos_Y, B):
            self.move_to(pos_X, pos_Y, B)
            if is_check(self.side_, B):
                return False
            else:
                return True

    def move_to(self, pos_X, pos_Y, B):
        piece_to_replace = None
        piece_to_replace = piece_at(pos_X, pos_Y, B)
        piece_to_add = piece_at(self.pos_X, self.pos_Y, B)
        index_PTA = 0
        changed_piece = False
        if piece_to_replace != None:
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    index_PTA = i
                    changed_piece = True
            if changed_piece:
                for i in range(len(B[1])):
                    if B[1][i] == piece_to_replace:
                        B[1][i] = piece_to_add
            del B[1][index_PTA]
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    B[1][i].pos_X = pos_X
                    B[1][i].pos_Y = pos_Y
            return B
        elif piece_to_replace == None:
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    B[1][i].pos_X = pos_X
                    B[1][i].pos_Y = pos_Y
            return B


class King(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        super().__init__(pos_X, pos_Y, side_)
        """sets initial values by calling the constructor of Piece"""

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]"""
        """checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]"""
        if (
            is_piece_at(pos_X, pos_Y, B) == True
            and piece_at(pos_X, pos_Y, B).side_ != self.side_
            or is_piece_at(pos_X, pos_Y, B) == False
        ):
            if abs(self.pos_X - pos_X) == 1 or abs(self.pos_X - pos_X) == 0:
                if abs(self.pos_Y - pos_Y) == 1 or abs(self.pos_Y - pos_Y) == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule2] and [Rule4] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule5], use is_check on new board
        """
        if self.can_reach(pos_X, pos_Y, B):
            self.move_to(pos_X, pos_Y, B)
            if is_check(self.side_, B):
                return False
            else:
                return True

    def move_to(self, pos_X, pos_Y, B):
        piece_to_replace = None
        piece_to_replace = piece_at(pos_X, pos_Y, B)
        piece_to_add = piece_at(self.pos_X, self.pos_Y, B)
        index_PTA = 0
        changed_piece = False
        if piece_to_replace != None:
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    index_PTA = i
                    changed_piece = True
            if changed_piece:
                for i in range(len(B[1])):
                    if B[1][i] == piece_to_replace:
                        B[1][i] = piece_to_add
            del B[1][index_PTA]
            for i in range(len(B[1])):
                if B[1][i] == piece_to_add:
                    B[1][i].pos_X = pos_X
                    B[1][i].pos_Y = pos_Y
            return B
        elif piece_to_replace == None:
            for piece in B[1]:
                if piece == self:
                    piece.pos_X = pos_X
                    piece.pos_Y = pos_Y
            return B


def is_check(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is check for side
    Hint: use can_reach
    """
    king_of_side = None
    for pieces in B[1]:
        x = piece_at(pieces.pos_X, pieces.pos_Y, B)
        if isinstance(x, King) and x.side_ == side:
            king_of_side = x
    for pieces1 in B[1]:
        if pieces1.side_ != side:
            if pieces1.can_reach(king_of_side.pos_X, king_of_side.pos_Y, B):
                return True
    else:
        return False


def is_checkmate(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is checkmate for side

    Hints:
    - use is_check
    - use can_reach
    """
    piece_to_block = None
    king_of_side = None
    for pieces in B[1]:
        x = piece_at(pieces.pos_X, pieces.pos_Y, B)
        if isinstance(x, King) and x.side_ == side:
            king_of_side = x
    for pieces1 in B[1]:
        if pieces1.side_ != side:
            if pieces1.can_reach(king_of_side.pos_X, king_of_side.pos_Y, B):
                piece_to_block = pieces1
    for pieces2 in B[1]:
        if piece_to_block != None:
            if (
                pieces2.can_reach(piece_to_block.pos_X, piece_to_block.pos_Y, B)
                and pieces2.side_ != piece_to_block.side_
                and isinstance(pieces2, King) == False
            ):
                return False, 1
    if piece_to_block != None:
        for X in range(0, 6):
            for y in range(0, 6):
                for pieces3 in B[1]:
                    if pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X + X, pieces3.pos_Y + y, B
                    ):
                        Bnew = copy.deepcopy(B)
                        pieces3.move_to(pieces3.pos_X + X, pieces3.pos_Y + y, Bnew)
                        if is_check(side, Bnew):
                            return True
                    elif pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X - X, pieces3.pos_Y - y, B
                    ):
                        Bnew = copy.deepcopy(B)
                        pieces3.move_to(pieces3.pos_X - X, pieces3.pos_Y - y, Bnew)
                        if is_check(side, Bnew):
                            return True
                    elif pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X + X, pieces3.pos_Y - y, B
                    ):
                        Bnew = copy.deepcopy(B)
                        pieces3.move_to(pieces3.pos_X + X, pieces3.pos_Y - y, Bnew)
                        if is_check(side, Bnew):
                            return True
                    elif pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X - X, pieces3.pos_Y + y, B
                    ):
                        Bnew = copy.deepcopy(B)
                        pieces3.move_to(pieces3.pos_X - X, pieces3.pos_Y + y, Bnew)
                        if is_check(side, Bnew):
                            return True
    else:
        return False


def is_stalemate(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is stalemate for side

    Hints:
    - use is_check
    - use can_move_to
    """
    if is_check(side, B):
        return False
    elif is_check(side, B) == False:
        for X in range(0, 6):
            for y in range(0, 6):
                for pieces3 in B[1]:
                    if pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X + X, pieces3.pos_Y + y, B
                    ):
                        return False
                    elif pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X - X, pieces3.pos_Y - y, B
                    ):
                        return False
                    elif pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X + X, pieces3.pos_Y - y, B
                    ):
                        return False
                    elif pieces3.side_ == side and pieces3.can_reach(
                        pieces3.pos_X - X, pieces3.pos_Y + y, B
                    ):
                        return False
    else:
        return True


def read_board(filename: str) -> Board:
    """
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    """
    board_text = open(filename, "r")
    first_line = board_text.readline()
    second_line = board_text.readline()
    third_line = board_text.readline()
    board_text.close()

    if int(first_line) >= 2 and int(first_line) <= 26:
        grid_size = int(first_line)
        list_of_white_pieces = second_line.split(",")
        list_of_black_pieces = third_line.split(",")
    else:
        raise IOError

    new_list_remove_newline1 = []
    for piece in list_of_white_pieces:  # Removes new line character from list
        new_list_remove_newline1.append(piece.replace("\n", ""))
    list_of_white_pieces = copy.deepcopy(new_list_remove_newline1)

    new_list_remove_newline2 = []
    for piece in list_of_black_pieces:  # Removes new line character from list
        new_list_remove_newline2.append(piece.replace("\n", ""))
    list_of_black_pieces = copy.deepcopy(new_list_remove_newline2)

    new_list2 = []  # Removes all spaces from elements of list
    for piece in list_of_white_pieces:
        piece1 = piece.replace(" ", "")
        new_list2.append(piece1)
    list_of_white_pieces = copy.deepcopy(new_list2)

    new_list1 = []  # Removes all spaces from elements of list
    for piece in list_of_black_pieces:
        piece1 = piece.replace(" ", "")
        new_list1.append(piece1)
    list_of_black_pieces = copy.deepcopy(new_list1)

    for piece in list_of_white_pieces:
        if piece[0] != "K" or piece[0] != "R" or piece[0] != "B":
            if (
                piece[1].isalpha() == False or piece[2:].isnumeric() == False
            ):  # Checks to make sure last characters are num and first charcter is letter of each piece
                raise IOError

    for piece in list_of_black_pieces:
        if piece[0] != "K" or piece[0] != "R" or piece[0] != "B":
            if (
                piece[1].isalpha() == False or piece[2:].isnumeric() == False
            ):  # Checks to make sure last characters are num and first charcter is letter of each piece
                raise IOError

    new_list3 = []
    for piece in list_of_black_pieces:
        coords = location2index(piece[1:])
        if piece[0] == "K":
            piece = King(coords[0], coords[1], False)
            new_list3.append(piece)

        elif piece[0] == "B":
            piece = Bishop(coords[0], coords[1], False)
            # print(piece.pos_X, piece.pos_Y)
            new_list3.append(piece)

        elif piece[0] == "R":
            piece = Rook(coords[0], coords[1], False)
            new_list3.append(piece)
    list_of_black_pieces = copy.deepcopy(new_list3)

    new_list4 = []
    for piece in list_of_white_pieces:
        coords = location2index(piece[1:])
        if piece[0] == "K":
            piece = King(coords[0], coords[1], True)
            new_list4.append(piece)

        elif piece[0] == "B":
            piece = Bishop(coords[0], coords[1], True)
            # print(piece.pos_X, piece.pos_Y)
            new_list4.append(piece)

        elif piece[0] == "R":
            piece = Rook(coords[0], coords[1], True)
            new_list4.append(piece)
    list_of_white_pieces = copy.deepcopy(new_list4)

    combined_list = list_of_white_pieces + list_of_black_pieces

    generated_board = (grid_size, combined_list)

    B = generated_board

    return B


def save_board(filename: str, B: Board) -> None:
    """saves board configuration into file in current directory in plain format"""
    grid_to_str = str(B[0]) + "\n"
    line_of_white_pieces_for_PF = ""
    line_of_black_pieces_for_PF = ""
    for pieces in B[1]:
        if pieces.side_ == True:
            if isinstance(pieces, King):
                string_of_king = "K"
                x = pieces.pos_X
                y = pieces.pos_Y
                coords = index2location(x, y)
                comby = string_of_king + coords + "," + " "
                line_of_white_pieces_for_PF += comby
            if isinstance(pieces, Bishop):
                string_of_bishop = "B"
                x = pieces.pos_X
                y = pieces.pos_Y
                coords = index2location(x, y)
                comby = string_of_bishop + coords + "," + " "
                line_of_white_pieces_for_PF += comby
            if isinstance(pieces, Rook):
                string_of_rook = "R"
                x = pieces.pos_X
                y = pieces.pos_Y
                coords = index2location(x, y)
                comby = string_of_rook + coords + "," + " "
                line_of_white_pieces_for_PF += comby
        if pieces.side_ == False:
            if isinstance(pieces, King):
                string_of_king = "K"
                x = pieces.pos_X
                y = pieces.pos_Y
                coords = index2location(x, y)
                comby = string_of_king + coords + "," + " "
                line_of_black_pieces_for_PF += comby
            if isinstance(pieces, Bishop):
                string_of_bishop = "B"
                x = pieces.pos_X
                y = pieces.pos_Y
                coords = index2location(x, y)
                comby = string_of_bishop + coords + "," + " "
                line_of_black_pieces_for_PF += comby
            if isinstance(pieces, Rook):
                string_of_rook = "R"
                x = pieces.pos_X
                y = pieces.pos_Y
                coords = index2location(x, y)
                comby = string_of_rook + coords + "," + " "
                line_of_black_pieces_for_PF += comby
    new_line_of_black_pieces_for_PF = line_of_black_pieces_for_PF[:-2]
    file_to_write = open(filename, "w")
    file_to_write.write(grid_to_str)
    file_to_write.write(line_of_white_pieces_for_PF + "\n")
    file_to_write.write(new_line_of_black_pieces_for_PF)
    file_to_write.close()


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    """
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere

    Hints:
    - use methods of random library
    - use can_move_to
    """
    x = random.randint(1, B[0])
    y = random.randint(1, B[0])
    list_of_black_pieces_to_choose = []
    index_of_piece = 0
    for pieces in B[1]:
        if pieces.side_ == False:
            list_of_black_pieces_to_choose.append(pieces)
            print(list_of_black_pieces_to_choose)
    while pieces.can_move_to(x, y, B) == False:
        x = random.randint(1, B[0])
        y = random.randint(1, B[0])
        outer_range = len(list_of_black_pieces_to_choose)
        index_of_piece = random.randint(0, outer_range)
    return (list_of_black_pieces_to_choose[index_of_piece], x, y)


def conf2unicode(B: Board) -> str:
    """converts board cofiguration B to unicode format string (see section Unicode board configurations)"""
    lists_of_lists = []
    unicode_format_string = ""
    for x in range(1, B[0] + 1):
        lists_of_lists.append([])
    for lists in lists_of_lists:
        while len(lists) < B[0]:
            lists.append("\u2001")
    for piece in B[1]:
        if piece.side_ == True:
            if isinstance(piece, King):
                lists_of_lists[piece.pos_Y - 1][piece.pos_X - 1] = "♔"
            if isinstance(piece, Bishop):
                lists_of_lists[piece.pos_Y - 1][piece.pos_X - 1] = "♗"
            if isinstance(piece, Rook):
                lists_of_lists[piece.pos_Y - 1][piece.pos_X - 1] = "♖"
        if piece.side_ == False:
            if isinstance(piece, King):
                lists_of_lists[piece.pos_Y - 1][piece.pos_X - 1] = "♚"
            if isinstance(piece, Bishop):
                lists_of_lists[piece.pos_Y - 1][piece.pos_X - 1] = "♝"
            if isinstance(piece, Rook):
                lists_of_lists[piece.pos_Y - 1][piece.pos_X - 1] = "♜"

    # for i in range(B[0]-2, -1, -1):
    #     lists_of_lists[i].append("\n")

    for i in range(B[0] - 1, -1, -1):
        if i != 0:
            lists_of_lists[i].append("\n")
        for element in lists_of_lists[i]:
            unicode_format_string += element

    return unicode_format_string


# |white king | ♔ | \u2654 |
# |white rook | ♖ | \u2656 |
# |white bishop | ♗| \u2657 |
# |black king | ♚ | \u265A|
# |black rook | ♜ | \u265C|
# |black bishop | ♝ | \u265D|
# |space of matching width | |\u2001|


def main() -> None:
    """
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    """
    filename = input("File name for initial configuration: ")
    while filename != "QUIT":
        try:
            board_to_input = read_board(filename)
            break
        except FileNotFoundError:
            print("File is not valid, try again.")
            filename = input("File name for initial configuration: ")
    print("The initial configuration is:")
    print(conf2unicode(board_to_input))

    white_move = input(
        "First enter the row and column of piece and then the row and column of where you want piece to move:"
    )
    white_move_from = ""
    white_move_to = ""
    x = 0

    while white_move != "QUIT":
        for i in range(len(white_move) - 1, -1, -1):
            white_move_to += white_move[i]
            if white_move[i].isalpha():
                x = i
                break
        for i in range(0, x):
            white_move_from += white_move[i]
        break
    if white_move == "QUIT":
        name_of_save_file = input("Enter name you want to save current config as: ")
        save_board(name_of_save_file, board_to_input)

    elif white_move != "QUIT":
        white_move_to_reverse = white_move_to[::-1]
        white_move_from_coords = location2index(white_move_from)
        white_move_to_coords = location2index(white_move_to_reverse)

    new_board = ""
    if piece_at(white_move_from_coords[0], white_move_from_coords[1], board_to_input):
        # print(white_move_from_coords[0], white_move_from_coords[1])
        # print(white_move_to_coords[0], white_move_to_coords[1])
        piece_to_move = piece_at(
            white_move_from_coords[0], white_move_from_coords[1], board_to_input
        )
        if piece_to_move.can_move_to(
            white_move_to_coords[0], white_move_to_coords[1], board_to_input
        ):
            new_board = piece_to_move.move_to(
                white_move_to_coords[0], white_move_to_coords[1], board_to_input
            )
        print(conf2unicode(new_board))


if __name__ == "__main__":  # keep this in
    main()
