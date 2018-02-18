import unittest
import game as gm
import loggers as lg
import numpy as np
from testfixtures import LogCapture

class MyTest(unittest.TestCase):
    def test_player(self):
        self.assertEqual(gm.other_player(gm.LEFT), gm.RIGHT)
        self.assertEqual(gm.other_player(gm.RIGHT), gm.LEFT)

    def test_pieces(self):
        self.assertEqual(gm.render_piece(gm.EMPTY),       '   ')
        self.assertEqual(gm.render_piece(gm.LEFT_LION),   ' L>')
        self.assertEqual(gm.render_piece(gm.RIGHT_CHICK), '<c ')

    def test_owner(self):
        self.assertEqual(gm.piece_owner(gm.LEFT_LION), gm.LEFT)
        self.assertEqual(gm.piece_owner(gm.RIGHT_CHICK), gm.RIGHT)
        self.assertEqual(gm.piece_owner(gm.EMPTY), 0)


    def test_game(self):
        game = gm.Game()
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L> c><c <L "),
                    ('logger_main', "INFO", " G>      <E "),
                    ('logger_main', "INFO", "Captures: "),
                    ('logger_main', "INFO", "Left to play"),
            )
        self.assertTrue(state.isEmpty(0,1))
        self.assertTrue(state.isEmpty(0,2))
        self.assertFalse(state.isEmpty(1,0))
        allowed = state.allowedActions
        expectedAllowed = [[[1, 1], [1, 2]],
                           [[1, 0], [0, 1]],
                           [[1, 0], [2, 1]],
                           [[2, 0], [2, 1]]]
        self.assertEqual(sorted(allowed), sorted(expectedAllowed))
        game.step([[1, 1], [1, 2]])
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L>    c><L "),
                    ('logger_main', "INFO", " G>      <E "),
                    ('logger_main', "INFO", "Captures:  c>"),
                    ('logger_main', "INFO", "Right to play"),
            )
        allowed = state.allowedActions
        expectedAllowed = [[[0, 3], [0, 2]],
                           [[1, 3], [0, 2]],
                           [[1, 3], [1, 2]],
                           [[1, 3], [2, 2]],
                           [[2, 3], [1, 2]]]
        self.assertEqual(sorted(allowed), sorted(expectedAllowed))
        game.step([[2, 3], [1, 2]])
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L>   <E <L "),
                    ('logger_main', "INFO", " G>         "),
                    ('logger_main', "INFO", "Captures:  c><c "),
                    ('logger_main', "INFO", "Left to play"),
            )
        allowed = state.allowedActions
        expectedAllowed = [[[0, 0], [1, 1]],
                           [[1, 0], [0, 1]],
                           [[1, 0], [1, 1]],
                           [[1, 0], [2, 1]],
                           [[2, 0], [2, 1]],
                           [[-1, gm.LEFT_CHICK], [0, 1]],
                           [[-1, gm.LEFT_CHICK], [0, 2]],
                           [[-1, gm.LEFT_CHICK], [1, 1]],
                           [[-1, gm.LEFT_CHICK], [2, 1]],
                           [[-1, gm.LEFT_CHICK], [2, 2]]]
        self.assertEqual(sorted(allowed), sorted(expectedAllowed))
        game.step([[-1, gm.LEFT_CHICK], [2, 2]])
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L>   <E <L "),
                    ('logger_main', "INFO", " G>    c>   "),
                    ('logger_main', "INFO", "Captures: <c "),
                    ('logger_main', "INFO", "Right to play"),
            )
        game.step([[-1, gm.RIGHT_CHICK], [1, 1]])
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L><c <E <L "),
                    ('logger_main', "INFO", " G>    c>   "),
                    ('logger_main', "INFO", "Captures: "),
                    ('logger_main', "INFO", "Left to play"),
            )
        game.step([[2, 2], [2, 3]])
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L><c <E <L "),
                    ('logger_main', "INFO", " G>       C>"),
                    ('logger_main', "INFO", "Captures: "),
                    ('logger_main', "INFO", "Right to play"),
            )
        game.step([[1, 3], [2, 3]])
        state = game.gameState
        savedState = state
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", " L><c <E    "),
                    ('logger_main', "INFO", " G>      <L "),
                    ('logger_main', "INFO", "Captures: <c "),
                    ('logger_main', "INFO", "Left to play"),
            )
        game.step([[2, 0], [2, 1]])
        game.step([[1, 1], [1, 0]])
        state = game.gameState
        with LogCapture() as l:
            state.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", "<C    <E    "),
                    ('logger_main', "INFO", "    G>   <L "),
                    ('logger_main', "INFO", "Captures: <c <L "),
                    ('logger_main', "INFO", "Right has won!"),
            )
        game.gameState = savedState
        game.step([[1, 0], [1, 3]])
        with LogCapture() as l:
            game.gameState.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", "   <c <E  L>"),
                    ('logger_main', "INFO", " G>      <L "),
                    ('logger_main', "INFO", "Captures: <c "),
                    ('logger_main', "INFO", "Right to play"),
            )
        self.assertEqual(game.gameState.winner, 0)
        savedState = game.gameState
        game.step([[2, 3], [1, 3]])
        with LogCapture() as l:
            game.gameState.render(lg.logger_main)
            l.check(('logger_main', "INFO", " E>      <G "),
                    ('logger_main', "INFO", "   <c <E <L "),
                    ('logger_main', "INFO", " G>         "),
                    ('logger_main', "INFO", "Captures: <c <L "),
                    ('logger_main', "INFO", "Right has won!"),
            )
        self.assertEqual(game.gameState.winner, gm.RIGHT)
        game.gameState = savedState
        game.step([[2, 3], [2, 2]])
        self.assertEqual(game.gameState.winner, gm.LEFT)

    def test_id(self):
        id = gm.Game().gameState.id
        print("\nID: " + id)

    def test_binary(self):
        game = gm.Game()
        res = np.reshape(game.gameState.binary, (10, 2, 3, 4))
        self.assertEqual(res[0][0][1][0], 1)
        self.assertEqual(res[4][0][1][1], 1)
        game.step([[1, 1], [1, 2]])
        res = np.reshape(game.gameState.binary, (10, 2, 3, 4))
        self.assertEqual(res[9][0][1][2], 0)
        self.assertEqual(res[9][0][1][1], 1)
        self.assertEqual(res[9][1][1][2], 1)

    def test_move_ints(self):
        state = gm.Game().gameState
        for i in range(15*12):
            self.assertEqual(i, state.moveToInt(state.intToMove(i)))
