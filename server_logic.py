import random
import math
from typing import List, Dict


#Function to avoid walls
def avoid_wall(my_head: Dict[str,int], height: int,width:int,possible_moves: List[str]) -> List[str]:
    if my_head['x'] == 0 and 'left' in possible_moves: #Avoid the left wall
        possible_moves.remove('left')
    elif my_head['x'] == width-1 and 'right' in possible_moves: #Avoid the right wall
        possible_moves.remove('right') 
    if my_head["y"] == 0 and 'down' in possible_moves: #Avoid the bottom wall
        possible_moves.remove('down') 
    elif my_head['y'] == height-1 and 'up' in possible_moves: #Avoid the top wall
        possible_moves.remove('up')
    
# Function to avoid break my neck and collide with my body.
def avoid_my_neck(my_head:List[dict],my_body: List[dict], possible_moves: List[str]) -> List[str]:
    
    for i in range(1,len(my_body)):
        if (my_head['x']-1,my_head['y']) == (my_body[i]['x'],my_body[i]['y']) and 'left' in possible_moves:  
            possible_moves.remove("left")

        elif (my_head['x']+1,my_head['y']) == (my_body[i]['x'],my_body[i]['y']) and 'right' in possible_moves:  
            possible_moves.remove("right")

        if (my_head['x'],my_head['y']-1) == (my_body[i]['x'],my_body[i]['y']) and 'down' in possible_moves:  
            possible_moves.remove("down")

        elif (my_head['x'],my_head['y']+1) == (my_body[i]['x'],my_body[i]['y']) and 'up' in possible_moves:  
            possible_moves.remove("up")
    
    
#Avoid enemy snakes
def avoid_snakes(my_head: Dict[str, int], snakes:List[Dict[str,str]], possible_moves: List[str],my_body:List[Dict],myID:str) -> List[str]:
    lst = possible_moves[:]
    for i in range(len(snakes)):
      if snakes[i]['id'] != myID:
        for j in range(len(snakes[i]['body'])):
            
            snakeCood = (snakes[i]['body'][j]['x'],snakes[i]['body'][j]['y'])
            if (my_head['x']+1,my_head['y']) == snakeCood and 'right' in possible_moves:
                possible_moves.remove('right')
            if (my_head['x']-1,my_head['y']) == snakeCood  and 'left' in possible_moves:
                possible_moves.remove('left')
            if (my_head['x'],my_head['y']-1) == snakeCood  and 'down' in possible_moves:
                possible_moves.remove('down')
            if (my_head['x'],my_head['y']+1) == snakeCood  and 'up' in possible_moves:
                possible_moves.remove('up')
    

      # This block of code it is to know if a snake is going to intercept me.
      if len(snakes[i]["body"]) >= len(my_body):
        enemySnake = {'x':snakes[i]['body'][0]['x'],'y':snakes[i]['body'][0]['y']}
        dist = 1
        if(enemySnake['x']-dist,enemySnake['y']) == (my_head['x']+dist,my_head['y']) and 'right' in possible_moves:
              possible_moves.remove('right')
        if(enemySnake['x']+dist,enemySnake['y']) == (my_head['x']-dist,my_head['y']) and 'left' in possible_moves:
              possible_moves.remove('left')
        if(enemySnake['x'],enemySnake['y']-dist) == (my_head['x'],my_head['y']+dist) and 'up' in possible_moves:
              possible_moves.remove('up')
        if(enemySnake['x'],enemySnake['y']+dist) == (my_head['x'],my_head['y']-dist) and 'down' in possible_moves:
              possible_moves.remove('down')
              
        
        if((enemySnake['x'],enemySnake['y']+dist) == (my_head['x']+dist,my_head['y']) or (enemySnake['x'],enemySnake['y']-dist) == (my_head['x']+dist,my_head['y'])) and 'right' in possible_moves:
              possible_moves.remove('right')
        if((enemySnake['x'],enemySnake['y']+dist) == (my_head['x']-dist,my_head['y']) or (enemySnake['x'],enemySnake['y']-dist) == (my_head['x']-dist,my_head['y'])) and 'left' in possible_moves:
              possible_moves.remove('left')
        if((enemySnake['x']-dist,enemySnake['y']) == (my_head['x'],my_head['y']+dist) or (enemySnake['x']+dist,enemySnake['y']) == (my_head['x'],my_head['y']+dist)) and 'up' in possible_moves:
              possible_moves.remove('up')
        if((enemySnake['x']-dist,enemySnake['y']) == (my_head['x'],my_head['y']-dist) or (enemySnake['x']+dist,enemySnake['y']) == (my_head['x'],my_head['y']-dist)) and 'down' in possible_moves:
            possible_moves.remove('down')

        if(len(possible_moves) < 1):
          possible_moves += lst


#Look for the closest food coordinate and return it.
def CloseFood(data:Dict) -> tuple:
    foodCord = data['board']['food']
    head = data["you"]["head"]
    nearestNum = None
    coordinateFood = None
    for i in foodCord:
        tempX = abs(head['x']-i['x'])
        tempY = abs(head['y'] - i['y'])
        totalTemp = tempX + tempY        
        if nearestNum == None or totalTemp < nearestNum:
            nearestNum = totalTemp
            coordinateFood = {'x':i['x'],'y':i['y']}
    return {"coord":coordinateFood,"distance":nearestNum}

# With the closest food coordinate, the snake decides where to go.
def food_finder(my_head:Dict[str,int],closerFood:tuple,possible_moves:List[str]):
  lst = possible_moves[:]
  if my_head['x']+1 > closerFood['coord']['x'] and 'right' in possible_moves:
    possible_moves.remove('right')
  if  my_head['x']-1 < closerFood['coord']['x'] and 'left' in possible_moves:
    possible_moves.remove('left')
  if  my_head['y']-1 < closerFood['coord']['y'] and 'down' in possible_moves:
    possible_moves.remove('down')
  if  my_head['y']+1 > closerFood['coord']['y'] and 'up' in possible_moves:
    possible_moves.remove('up')


  
  #If something weird happen and the possible_moves's len is 0, 
  if len(possible_moves) < 1:
    possible_moves += lst


def avoid_collisions(my_head: Dict[str,int], my_body: Dict[str,int],height:int,width:int,snakes:List[Dict[str,str]] ,possible_moves:List[str],myID: str) -> List[str]:

    avoid_wall(my_head,height,width,possible_moves)
    avoid_my_neck(my_head,my_body,possible_moves)

    if(len(snakes) > 1):
        avoid_snakes(my_head,snakes,possible_moves,my_body,myID)
    return possible_moves

#Main function 
def choose_move(data: dict) -> str:
  
      my_head = data["you"]["head"]
      my_body = data["you"]["body"]  
      myID = data["you"]["id"]

      width = data["board"]["width"]
      height = data["board"]["height"]

      snakes = data["board"]["snakes"]
      health = data['you']['health']
      


      #print(f"All board data this turn: {data}")


      possible_moves = ["up", "down", "left", "right"]

      # Don't allow your Battlesnake to move back in on it's own neck
      avoid_collisions(my_head,my_body,height,width,snakes,possible_moves,myID)

      
      if len(data["board"]["food"]) > 0:
        close_food = CloseFood(data)
        food_finder(my_head,close_food,possible_moves)


      move = random.choice(possible_moves)
      

      print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

      return move

