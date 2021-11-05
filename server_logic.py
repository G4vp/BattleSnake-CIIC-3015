import random
from typing import List, Dict

#https://battle-snake-g4vp.herokuapp.com/ | https://git.heroku.com/battle-snake-g4vp.git

def avoid_walls(my_head: Dict[str,int], widthWall:int,heigthWall:int) -> str:
  possibleMove = 'right'
  if my_head['y'] == 0 and not my_head['x'] == 0:
    possibleMove = 'left'
  elif my_head['x'] == heigthWall and not my_head['y'] == 0:
    possibleMove = 'down'
  elif my_head['y'] == 4 and my_head['x'] == 0:
    possibleMove = 'right'
  elif my_head['x'] == 0 and not my_head['y']+1 == heigthWall:
    possibleMove = 'up'
  else:
    possibleMove = 'down'

  print('---------',my_head)
  return possibleMove


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:

    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def choose_move(data: dict) -> str:

    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)


    move = 'up'

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
