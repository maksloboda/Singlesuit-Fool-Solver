import unittest
import legacy.solvers
from typing import List, Tuple
from test_util.random_state_picker import generate_random_state
from test_util.game_tracker import GameTracker

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
  

class TestLegacySolversCompvComp(unittest.TestCase):

  def test_fool(self):
    test_legacy_compvcomp(self, legacy.solvers.OdnomastkaDurak)
  
  def test_dfool(self):
    test_legacy_compvcomp(self, legacy.solvers.OdnomastkaD_Durak)


if __name__ == "__main__":
  unittest.main()