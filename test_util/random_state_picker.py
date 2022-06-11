import random
from typing import List, Tuple

def generate_random_state(allowed_sizes: List[int]) -> Tuple[List[int], int]:
  """
  Get a list of allowed card counts and returns a random state
  """
  is_valid = False
  card_ownership : List[int] = []
  first_player : int = 0
  while not is_valid:
    size_idx = random.randrange(0, len(allowed_sizes))
    size = allowed_sizes[size_idx]

    card_ownership = []
    for _ in range(size):
      card_ownership.append(random.randrange(0, 2))
    first_player = random.randrange(0, 2)
    
    if is_state_valid(card_ownership, first_player):
      return (card_ownership, first_player)

def is_state_valid(card_ownership: List[int], player: int) -> bool:
  if len(card_ownership) == 0:
    return False
  
  first_card_owner = card_ownership[0]

  is_all_owned_by_one = all(
    map(
      lambda owner: owner == first_card_owner,
      card_ownership
    )
  )
  return not is_all_owned_by_one