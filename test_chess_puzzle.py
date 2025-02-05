import copy
from chess_puzzle import *


def test_location2index1():
    assert location2index("e2") == (5,2)
    assert location2index("z26") == (26,26)
    assert location2index("a1") == (1,1)
    assert location2index("g26") == (7,26)

def test_index2location1():
    assert index2location(5,2) == "e2"
    assert index2location(26,26) == "z26"
    assert index2location(1,1) == "a1"
    assert index2location(7,26) == "g26" 

wb1 = Bishop(1,1,True)
wr1 = Rook(1,2,True)
wb2 = Bishop(5,2, True)
bk = King(2,3, False)
br1 = Rook(4,3,False)
br2 = Rook(2,4,False)
br3 = Rook(5,4, False)
wr2 = Rook(1,5, True)
wk = King(3,5, True)

B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
'''
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖   ♗
♗    
'''

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False
    assert is_piece_at(1,1, B1) == True 
    assert is_piece_at(5,5, B1) == False
    assert is_piece_at(4,3, B1) == True
    assert is_piece_at(4,4, B1) == False


def test_piece_at1():
    assert piece_at(4,3, B1) == br1
    assert piece_at(1,1, B1) == wb1

def test_can_reach1():
    assert wr2.can_reach(4,5, B1) == False
    #assert wb1.can_reach(2,2, B1) == True 
    assert wr2.can_reach(1,2, B1) == False #Tests if when piece moved to a place of its own side the function - Should be false
    assert wr2.can_reach(1,4, B1) == True #Tests when only Y value changed and Y value is less than original Y value - Should be True as moving from (1,5)
    assert br1.can_reach(5,3, B1) == True #Tests when only X value changed and X value is more than original X value - Should be True as moving from (4,3)
    assert br3.can_reach(5,5, B1) == True #Working now - should output True as moving from (5,4)
    assert br1.can_reach(3,2,B1) == False #Outputs none instead of false (now outputs False)
    assert br3.can_reach(5,2,B1) == True #Should be true (I think) as the Rook is moving to a square of opposite side
    assert wb2.can_reach(4, 3, B1) == True #Should be true as moves up diagonally to a cell that contains a Black rook br1 - origin (5,2)
    assert wb2.can_reach(4, 1, B1) == True #Should be true as moves down diagonally to an empty space - origin (5,2)
    assert wb2.can_reach(4, 2, B1) == False #Should be false as moves sideways and not diagonally - origin (5,2)
    assert wb1.can_reach(5, 5, B1) == True #Should be true as moves up diagonally through multiple empty cells - origin (1,1)
    assert wb1.can_reach(5, 4, B1) == False #Should be false as moves non diagonally - origin (1,1)
    assert wb2.can_reach(3, 4, B1) == False #Should be false as moves up diagonally past a cell that contains a Black rook br1 - origin (5,2)
    assert bk.can_reach(2,4,B1) == False #Should be false as the king moves to a space occupied by it's own side 
    assert wk.can_reach(2,4,B1) == True #Should be true as the white king moves to a space occupied by a black rook
    assert wk.can_reach(4,5,B1) == True #Should be true as king moves to an empty space 
    assert wk.can_reach(5,5,B1) == False  #Should be false as king moves two cells sideways (can only move in a radius of one)


br2a = Rook(1,5,False)
wr2a = Rook(2,5,True)

def test_can_move_to1():
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
    assert wr2a.can_move_to(2,4, B2) == False

def test_move_to1():
    assert br3.move_to(5, 2, B1) == (5, [wb1, wr1, br3, bk, br1, br2, wr2, wk])
    


def test_is_check1():
    wr2b = Rook(2,4,True)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(True, B2) == True
    assert is_check(False, B2) == True

def test_is_check2():
    wr2b = Rook(1,4, True)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(False, B2) == False


def test_is_checkmate1():
    br2b = Rook(4,5,False)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert is_checkmate(True, B2) == True
    assert is_checkmate(False, B2) == False

def test_is_checkmate2():
    wk3 = King(1,1, True)
    wb3 = Bishop(4,2, True)

    bk3 = King(4,3, False)
    bb3 = Bishop(2,2, False)

    B3 = (5, [wk3, wb3, bk3, bb3])

    '''

    |  |  |  |  |  |
    |  |  |  |  |  |
    |  |  |  |♚|  |
    |  |♝|  |♗|  |
    |♔|  |  |  |  |
    '''
    assert is_checkmate(True, B3) == True #Should equal True as Black Bishop can take White King
    assert is_checkmate(False, B3) == False #Should equal False as no piece can reach Black King 

def test_read_board1():
    B = read_board(r"C:\Users\thoma\Documents\POP Coursework\csm090-pop-apr22-chess-puzzle-bobbobdude\csm090-pop-apr22-chess-puzzle-bobbobdude\board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side_ == piece1.side_ and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side_ == piece1.side_ and type(piece) == type(piece1):
                found = True
        assert found
        
def test_conf2unicode1():
    assert conf2unicode(B1) == "♖ ♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "
    
