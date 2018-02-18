import numpy as np
import logging

from enum import Enum

LEFT=1
RIGHT=-1

def other_player(player):
        return -player

def render_player(player):
        return 'Left' if player==LEFT else 'Right'

EMPTY=0
LEFT_LION=1
LEFT_CHICKEN=2
LEFT_GIRAFFE=3
LEFT_ELEPHANT=4
LEFT_CHICK=5
RIGHT_LION=-1
RIGHT_CHICKEN=-2
RIGHT_GIRAFFE=-3
RIGHT_ELEPHANT=-4
RIGHT_CHICK=-5

PIECE_MAPPING = {
        EMPTY:         '   ',
        LEFT_LION:     ' L>',
        LEFT_CHICKEN:  ' C>',
        LEFT_GIRAFFE:  ' G>',
        LEFT_ELEPHANT: ' E>',
        LEFT_CHICK:    ' c>',
        RIGHT_LION:    '<L ',
        RIGHT_CHICKEN: '<C ',
        RIGHT_GIRAFFE: '<G ',
        RIGHT_ELEPHANT:'<E ',
        RIGHT_CHICK:   '<c '
}

def render_piece(piece):
        return PIECE_MAPPING.get(piece)

def piece_owner(piece):
        if piece > 0:
                return 1
        elif piece < 0:
                return -1
        else:
                return 0

def empty_captures():
        return {
                LEFT_LION:     0,
                LEFT_GIRAFFE:  0,
                LEFT_ELEPHANT: 0,
                LEFT_CHICK:    0,
                RIGHT_LION:    0,
                RIGHT_GIRAFFE: 0,
                RIGHT_ELEPHANT:0,
                RIGHT_CHICK:   0
        }


class Game:

	def __init__(self):
                self.reset()
		# self.actionSpace = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.int)
		# self.grid_shape = (3,4)
		# self.input_shape = (11,3,4)
		self.name = 'animalshogi'
		# self.state_size = len(self.gameState.binary)
		# self.action_size = len(self.actionSpace)

	def reset(self):
		self.gameState = GameState(np.array([
                        [LEFT_ELEPHANT, EMPTY,      EMPTY,       RIGHT_GIRAFFE],
                        [LEFT_LION,     LEFT_CHICK, RIGHT_CHICK, RIGHT_LION],
                        [LEFT_GIRAFFE,  EMPTY,      EMPTY,       RIGHT_ELEPHANT]
                ], dtype=np.int), empty_captures() , LEFT)
		return self.gameState

	def step(self, action):
		next_state = self.gameState.takeAction(action)
		self.gameState = next_state
		return next_state

	def identities(self, state, actionValues):
		identities = [(state,actionValues)]
		return identities


LION_MOVES = [[-1, -1], [-1, 0], [-1, 1],
              [ 0, -1],          [ 0, 1],
              [ 1, -1], [ 1, 0], [ 1, 1]]

GIRAFFE_MOVES = [        [-1, 0]         ,
                [ 0, -1],          [ 0, 1],
                         [ 1, 0]]

ELEPHANT_MOVES = [[-1, -1], [-1, 1],
                  [ 1, -1], [ 1, 1]]

LEFT_CHICKEN_MOVES = [          [-1, 0], [-1, 1],
                      [ 0, -1],          [ 0, 1],
                                [ 1, 0], [ 1, 1]]

RIGHT_CHICKEN_MOVES = [[-1, -1], [-1, 0]         ,
                       [ 0, -1],          [ 0, 1],
                       [ 1, -1], [ 1, 0]         ]

PIECE_MOVEMENTS = {
        LEFT_LION: LION_MOVES,
        RIGHT_LION: LION_MOVES,
        LEFT_GIRAFFE: GIRAFFE_MOVES,
        RIGHT_GIRAFFE: GIRAFFE_MOVES,
        LEFT_ELEPHANT: ELEPHANT_MOVES,
        RIGHT_ELEPHANT: ELEPHANT_MOVES,
        LEFT_CHICK: [[0, 1]],
        RIGHT_CHICK: [[0, -1]],
        LEFT_CHICKEN: LEFT_CHICKEN_MOVES,
        RIGHT_CHICKEN: RIGHT_CHICKEN_MOVES
}

class GameState():
	def __init__(self, board, captures, playerTurn):
		self.board = board
                self.captures = captures
		self.playerTurn = playerTurn
		self.id = self._convertStateToId()
		self.allowedActions = self._allowedActions()
                self.winner = self._winner()

        def isEmpty(self, y, x):
                return self.board[y][x] == EMPTY

	def _allowedActions(self):
		allowed = []
                for y in range(3):
                        for x in range(4):
                                piece = self.board[y][x]
                                def deltaToMove(d):
                                        return [[y, x],[y+d[0], x+d[1]]]
                                def isValid(m):
                                        y = m[1][0]
                                        x = m[1][1]
                                        return y >= 0 and y < 3 and x>= 0 and x<4 and piece_owner(self.board[y][x]) != self.playerTurn
                                if piece_owner(piece) == self.playerTurn:
                                        allowed += filter(isValid, map(deltaToMove, PIECE_MOVEMENTS.get(piece)))
                empties = []
                for y in range(3):
                        for x in range(4):
                                if self.isEmpty(y, x):
                                        empties.append([y, x])
                for piece, count in self.captures.iteritems():
                        if count > 0 and piece_owner(piece) == self.playerTurn:
                                insert_moves = map(lambda e: [[-1, piece], e], empties)
                                if piece == LEFT_CHICK:
                                        insert_moves = filter(lambda m: m[1][1] != 3, insert_moves)
                                elif piece == RIGHT_CHICK:
                                        insert_moves = filter(lambda m: m[1][1] != 0, insert_moves)
                                allowed += insert_moves
		return allowed

	# def _binary(self):
	# 	currentplayer_position = np.zeros(len(self.board), dtype=np.int)
	# 	currentplayer_position[self.board==self.playerTurn] = 1

	# 	other_position = np.zeros(len(self.board), dtype=np.int)
	# 	other_position[self.board==-self.playerTurn] = 1

	# 	position = np.append(currentplayer_position,other_position)

	# 	return (position)

	def _convertStateToId(self):
                id =
	# 	player1_position = np.zeros(len(self.board), dtype=np.int)
	# 	player1_position[self.board==1] = 1

	# 	other_position = np.zeros(len(self.board), dtype=np.int)
	# 	other_position[self.board==-1] = 1

	# 	position = np.append(player1_position,other_position)

	# 	id = ''.join(map(str,position))

	# 	return id

	def _winner(self):
                if self.captures.get(LEFT_LION) > 0:
                        return LEFT
                elif self.captures.get(RIGHT_LION) > 0:
                        return RIGHT
		else:
                        for y in range(3):
                                if self.board[y][3] == LEFT_LION and self.playerTurn == LEFT:
                                        return LEFT
                                elif self.board[y][0] == RIGHT_LION and self.playerTurn == RIGHT:
                                        return RIGHT
                        return 0

	def takeAction(self, action):
                newBoard = np.array(self.board)
                newCaptures = self.captures.copy()
                source, target = action
                sourceY, sourceX = source
                targetY, targetX = target
                isNotInsert = sourceY != -1
                piece = self.board[sourceY][sourceX] if isNotInsert else sourceX
                targetPiece = self.board[targetY][targetX]
                if isNotInsert:
                        newBoard[sourceY][sourceX] = EMPTY
                else:
                        newCaptures[piece]-=1
                if piece == LEFT_CHICK and targetX == 3:
                        newBoard[targetY][targetX] = LEFT_CHICKEN
                elif piece == RIGHT_CHICK and targetX == 0:
                        newBoard[targetY][targetX] = RIGHT_CHICKEN
                else:
                        newBoard[targetY][targetX] = piece
                if targetPiece != EMPTY:
                        capturedPiece = -targetPiece
                        if capturedPiece == LEFT_CHICKEN:
                                capturedPiece = LEFT_CHICK
                        elif capturedPiece == RIGHT_CHICKEN:
                                capturedPiece = RIGHT_CHICK
                        newCaptures[capturedPiece]+=1

		newState = GameState(newBoard, newCaptures, -self.playerTurn)

		return newState

	def render(self, logger):
		for y in range(3):
                        line = ""
                        for x in range(4):
                                line+= render_piece(self.board[y][x])
			logger.info(line)
                captures_line = "Captures: "
                for piece, count in self.captures.iteritems():
                        captures_line += count * render_piece(piece)
                logger.info(captures_line)
                if self.winner != 0:
                        logger.info(render_player(self.winner) + " has won!")
                else:
                        logger.info(render_player(self.playerTurn) + " to play")
