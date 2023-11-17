"""
Tic Tac Toe Player
"""

import math
import copy 

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == [[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]:
        return X
        
    count_x = 0
    count_o = 0

    for i in board:
        for j in i:
            if j == X:
                count_x += 1
            elif j == O:
                count_o += 1
    if count_x > count_o:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    free = set()
    i1 = 0
    i2 = 0 
    for i in board:
        for j in i: 
            if j == EMPTY:
                x = (i1,i2)
                free.add(x)
            i2 += 1
        i1 += 1
        i2 = 0 
    return free
    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if not any(action==i for i in actions(board)):
        raise Exception("Invalid Play")
    
    board_ = copy.deepcopy(board)
    whois = player(board)
    board_[action[0]][action[1]] = whois
    return board_


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    b = list(map(lambda *x: list(x), *board))
    d1 = [board[0][0], board[1][1], board[2][2]]
    d2 = [board[0][2], board[1][1], board[2][0]]

    for i in board:
        if i == [X,X,X]:
            return X 
        if i == [O,O,O]:
            return O
    for i in b:
        if i == [X,X,X]:
            return X 
        if i == [O,O,O]:
            return O
        
    if d1 == [X,X,X]:
        return X
    if d2 == [X,X,X]:
        return X
    
    if d1 == [O,O,O]:
        return O
    if d2 == [O,O,O]:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True     
    for i in board: 
        for j in i: 
            if j == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0

def _max(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, _min(result(board, action)))
    return v

def _min(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, _max(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    
    elif player(board) == X:
        plays = []
        for action in actions(board):
            plays.append([_min(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    
    elif player(board) == O:
        plays = []
        for action in actions(board):
            plays.append([_max(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=False)[0][1]
    
