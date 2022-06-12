
from typing import List, Tuple

EMPTY_FIELD = -1

class GameState:
  # 0 or 1
  current_player: int
  # Lists of cards that players own
  first_player_set: List[int]
  second_player_set: List[int]
  # card currently on the field
  field: int

  def __init__(self,
    current_player_: int,
    first_player_set_: List[int],
    second_player_set_: List[int],
    field_: int) -> None:
    self.current_player = current_player_
    self.first_player_set = first_player_set_
    self.second_player_set = second_player_set_
    self.field = field_