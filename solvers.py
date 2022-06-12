import legacy.solvers
from classtypes.game_state import GameState, EMPTY_FIELD
from typing import Any, Tuple, List
import itertools

def prepare_legacy_solver(state: GameState, solver_class) -> Tuple[Any, List[int]]:
  """
  Returns a solver that is in the provided state and a sorted list of cards
  """
  other_player = 1 - state.current_player
  extra_card = [(state.field - 1, other_player)] if state.field is not EMPTY_FIELD else []
  # An array of (card_number, owner)
  card_info = list(
      sorted(
          itertools.chain(
              zip(state.first_player_set, [0] * len(state.first_player_set)),
              zip(state.second_player_set, [1] * len(state.second_player_set)),
              extra_card
          )
      )
  )

  card_owners = list(map(lambda x: x[1], card_info))
  # Decide if we should make the fake move
  start_player = other_player if extra_card else state.current_player

  solver = solver_class(card_owners, start_player)

  if extra_card:
    # make the fake move
    card_index = card_info.index(extra_card[0])
    assert(card_index != -1)
    ret_val = solver.move_by_player(card_index + 1)
    assert(ret_val != -1)
    # print("Player move card index", card_index)

  card_names = list(map(lambda x: x[0], card_info))

  return (solver, card_names)

def find_optimal_move_generic(state: GameState, solver_class) -> int:
  """
  Find an optional move for provided state using the provided solver.
  Returns the optimal card_number
  """
  solver, cards = prepare_legacy_solver(state, solver_class)
  idx = solver.move_by_computer()
  # print("Solved value", cards[idx - 1])
  assert(idx != -1)
  return cards[idx - 1]

def find_optimal_move_fool(state: GameState) -> int:
  return find_optimal_move_generic(state, legacy.solvers.OdnomastkaDurak)

def find_optimal_move_dfool(state: GameState) -> int:
  return find_optimal_move_generic(state, legacy.solvers.OdnomastkaD_Durak)