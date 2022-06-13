import unittest
from typing import List, Tuple
from classtypes.game_state import GameState

EMPTY_FIELD = -1

class GameTracker:
  """
  Used to track state of the game
  Checks that all the moves are correct
  """
  test_case: unittest.TestCase
  cards: List[int]
  current_player: int
  field: int
  scores: List[int]

  def __init__(self, test_case_: unittest.TestCase,
      cards_: List[int], current_player_: int) -> None:
    self.test_case = test_case_
    self.cards = cards_
    self.current_player = current_player_
    self.field = EMPTY_FIELD
  
  def get_state(self) -> GameState:
    card_info = list(enumerate(self.cards))
    # Find numbers of cards owned by the first player
    first_player_set = list(map(lambda x: x[0],
      filter(lambda x: x[1] == 0, card_info)
    ))
    # Find numbers of cards owned by the second player
    second_player_set = list(map(lambda x: x[0],
      filter(lambda x: x[1] == 1, card_info)
    ))

    field = self.field - 1 if self.field != EMPTY_FIELD else EMPTY_FIELD

    return GameState(self.current_player, first_player_set, second_player_set, field)

  def apply_move(self, move_value):
    # Card should be valid
    self.test_case.assertTrue(1 <= move_value <= len(self.cards))
    if self.field == move_value:
      # Try to take the card
      # There should be a card on the field
      self.test_case.assertNotEqual(self.field, -1)
      self.cards[self.field - 1] = self.current_player
      self.current_player = 1 - self.current_player
      self.field = EMPTY_FIELD
    else:
      # Try to put card down
      # This player should own the card
      self.test_case.assertEqual(self.cards[move_value - 1], self.current_player)
      # Card should be greater then one on the field
      self.test_case.assertGreater(move_value, self.field)
      if self.field == EMPTY_FIELD:
        # Put the card down
        self.field = move_value
        self.current_player = 1 - self.current_player
      else:
        # Beat the card
        self.field = EMPTY_FIELD
      self.cards[move_value - 1] = None

  def is_end(self):
    values = set(self.cards)
    has_zero = (0 in values)
    has_one = (1 in values)
    if (not has_zero or not has_one) and self.field == EMPTY_FIELD:
      return True
    return False
