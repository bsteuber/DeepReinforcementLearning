import numpy as np
import loggers as lg
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

ALL_PIECES=[
        LEFT_LION, LEFT_CHICKEN, LEFT_GIRAFFE, LEFT_ELEPHANT, LEFT_CHICK,
        RIGHT_LION, RIGHT_CHICKEN, RIGHT_GIRAFFE, RIGHT_ELEPHANT, RIGHT_CHICK
]

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
		self.grid_shape = (3,4)
		self.input_shape = (20,3,4) # for each field and piece type, store if the piece is there and the number of pieces in hand
                self.pieces = {'1':'L', '0': '-', '-1':'R'}
		self.name = 'animalshogi'
		self.state_size = len(self.gameState.binary)
                self.action_shape = (12+3,12) # 3 extra for chicks, elephants, giraffe's in hand
		self.action_size = 15*12

	def reset(self):
		self.gameState = GameState(np.array([
                        [LEFT_ELEPHANT, EMPTY,      EMPTY,       RIGHT_GIRAFFE],
                        [LEFT_LION,     LEFT_CHICK, RIGHT_CHICK, RIGHT_LION],
                        [LEFT_GIRAFFE,  EMPTY,      EMPTY,       RIGHT_ELEPHANT]
                ], dtype=np.int), empty_captures() , LEFT, 0)
		return self.gameState

	def step(self, action):
		next_state, value, done = self.gameState.takeAction(action)
		self.gameState = next_state
                return ((next_state, value, done, None))

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
	def __init__(self, board, captures, playerTurn, moveNumber):
                self.moveNumber = moveNumber
		self.board = board
                self.captures = captures
		self.playerTurn = playerTurn
		self.id = self._convertStateToId()
                self.binary = self._binary()

                self.pieces = {'1':'L', '0': '-', '-1':'R'}

                self.allowedActions = self._allowedActions()
                self.result = self._result()

                currentPlayerWin = self.result[1] * self.playerTurn
                self.score = (currentPlayerWin, -currentPlayerWin)

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
		return map(lambda move: self.moveToInt(move), allowed)

        def _piece_for_current_player(self, piece):
                if self.playerTurn == LEFT:
                        return piece
                else:
                        return -piece

        def _point_for_current_player(self, y, x):
                if self.playerTurn == LEFT:
                        return (y, x)
                else:
                        return (2-y, 3-x)

	def _binary(self):
                bin_array = []
                for piece in ALL_PIECES:
                        real_piece = self._piece_for_current_player(piece)
                        position = np.zeros(12, dtype=np.int)
                        for y in range(3):
                                for x in range(4):
                                        (real_y, real_x) = self._point_for_current_player(y, x)
                                        if self.board[real_y][real_x]==real_piece:
                                                position[y*4+x]=1
                        captures = np.full(12, self.captures.get(real_piece) or 0, dtype=np.int)
                        bin_array = np.append(bin_array, position)
                        bin_array = np.append(bin_array, captures)
                return bin_array

        def pointToInt(self, y, x):
                ret = y*4+x
                if self.playerTurn == LEFT:
                        return ret
                else:
                        return 11-ret

        def intToPoint(self, i):
                realI = i if self.playerTurn == LEFT else 11-i
                y = realI // 4
                x = realI % 4
                return (y, x)

        def moveToInt(self, move):
                [[sourceY, sourceX], [targetY, targetX]] = move
                if sourceY != -1:
                        sourceI = self.pointToInt(sourceY, sourceX)
                else:
                        sourceI = {
                                LEFT_CHICK: 12,
                                RIGHT_CHICK: 12,
                                LEFT_GIRAFFE: 13,
                                RIGHT_GIRAFFE: 13,
                                LEFT_ELEPHANT: 14,
                                RIGHT_ELEPHANT: 14
                        }.get(sourceX)
                targetI = self.pointToInt(targetY, targetX)
                return sourceI*12 + targetI

        def intToMove(self, i):
                sourceI = i // 12
                targetI = i % 12
                if sourceI < 12:
                        sourceP = self.intToPoint(sourceI)
                else:
                        if self.playerTurn == LEFT:
                                piece = {
                                        12: LEFT_CHICK,
                                        13: LEFT_GIRAFFE,
                                        14: LEFT_ELEPHANT
                                }.get(sourceI)
                        else:
                                piece = {
                                        12: RIGHT_CHICK,
                                        13: RIGHT_GIRAFFE,
                                        14: RIGHT_ELEPHANT
                                }.get(sourceI)
                        sourceP = (-1, piece)
                targetP = self.intToPoint(targetI)
                return (sourceP, targetP)

	def _convertStateToId(self):
                return str(self.board) + str(self.captures)

	def _result(self):
                if self.moveNumber > 150:
                        return (1, 0)
                if self.captures.get(LEFT_LION) > 0:
                        return (1, LEFT)
                elif self.captures.get(RIGHT_LION) > 0:
                        return (1, RIGHT)
		else:
                        for y in range(3):
                                if self.board[y][3] == LEFT_LION and self.playerTurn == LEFT:
                                        return (1, LEFT)
                                elif self.board[y][0] == RIGHT_LION and self.playerTurn == RIGHT:
                                        return (1, RIGHT)
                        return (0, 0)

	def takeAction(self, action):
                move = self.intToMove(action)
                newBoard = np.array(self.board)
                newCaptures = self.captures.copy()
                source, target = move
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

		newState = GameState(newBoard, newCaptures, -self.playerTurn, self.moveNumber + 1)
                current_value = newState.score[0]
                done = newState.result[0] != 0
		return (newState, current_value, done)

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
                if self.result[1] != 0:
                        logger.info(render_player(self.result[1]) + " has won!")
                elif self.result[0] != 0:
                        logger.info(render_player("Draw game!"))
                else:
                        logger.info(render_player(self.playerTurn) + " to play")
