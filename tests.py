import unittest
from classtypes.game_state import GameState
import legacy.solvers
from typing import List, Tuple
from test_util.random_state_picker import generate_random_state
from test_util.game_tracker import GameTracker
from solvers import find_optimal_move_generic, find_optimal_move_fool

tested_sizes = [2, 3, 4, 5, 6]
repeats = 10000


def test_legacy_compvcomp(test_case: unittest.TestCase, solver_class):
  """
  Generic function to test legacy solvers
  Tests for correct winner prediction
  """
  for _ in range(repeats):
    state = generate_random_state(tested_sizes)
    solver = solver_class(*state)
    tracker = GameTracker(test_case, *state)
    predicted_winner = solver.who_wins()
    winning_score = solver.winning_score()
    move: int = solver.move_by_computer()
    test_case.assertNotEqual(move, -1)
    while move != -1:
      tracker.apply_move(move)
      test_case.assertEqual(predicted_winner, solver.who_wins())
      test_case.assertEqual(winning_score, solver.winning_score())
      move = solver.move_by_computer()
    test_case.assertTrue(tracker.is_end())

def test_new_solver(test_case: unittest.TestCase, solver_class):
  """
  Tests find_optimal_move_generic for some solver class.
  Verifies that predictions of the function are the same as legacy solvers
  """
  for _ in range(repeats):
    state = generate_random_state(tested_sizes)
    solver = solver_class(*state)
    tracker = GameTracker(test_case, *state)
    def check_new_solver_validity(expected_move):
      card_name = find_optimal_move_generic(tracker.get_state(), solver_class)
      # Only holds if cards are named as a sequence [0, 1, 2, ...]
      test_case.assertEqual(card_name + 1, expected_move)
    move: int = solver.move_by_computer()
    test_case.assertNotEqual(move, -1)
    while move != -1:
      check_new_solver_validity(move)
      tracker.apply_move(move)
      move = solver.move_by_computer()
    test_case.assertTrue(tracker.is_end())

class TestLegacySolversCompvComp(unittest.TestCase):

  def test_fool(self):
    test_legacy_compvcomp(self, legacy.solvers.OdnomastkaDurak)
  
  def test_dfool(self):
    test_legacy_compvcomp(self, legacy.solvers.OdnomastkaD_Durak)

class TestNewSolver(unittest.TestCase):

  def test_simple_fool(self):
    gs = GameState(0, [1, 3], [2, 4], -1)
    self.assertEqual(find_optimal_move_fool(gs), 3)
    gs = GameState(1, [1], [2, 4], 3)
    self.assertEqual(find_optimal_move_fool(gs), 4)
    gs = GameState(1, [1], [2], -1)
    self.assertEqual(find_optimal_move_fool(gs), 2)
    gs = GameState(0, [1], [], 2)
    self.assertEqual(find_optimal_move_fool(gs), 2)

  def test_fool(self):
    test_new_solver(self, legacy.solvers.OdnomastkaDurak)
  
  def test_dfool(self):
    test_new_solver(self, legacy.solvers.OdnomastkaD_Durak)

if __name__ == "__main__":
  unittest.main()