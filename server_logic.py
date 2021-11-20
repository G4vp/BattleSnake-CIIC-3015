import random
from typing import List, Dict

#https://battle-snake-g4vp.herokuapp.com/ | https://git.heroku.com/battle-snake-g4vp.git
def avoid_wall(my_head: Dict[str,int], height: int,width:int,possible_moves: List[str]) -> List[str]:
    if my_head['x'] == 0 and 'left' in possible_moves: #Avoid the left wall
        print('wall left')
        possible_moves.remove('left')
    elif my_head['x'] == width-1 and 'right' in possible_moves: #Avoid the right wall
        print('wall right')
        possible_moves.remove('right') 
    if my_head["y"] == 0 and 'down' in possible_moves: #Avoid the bottom wall
        print('wall down')
        possible_moves.remove('down') 
    elif my_head['y'] == height-1 and 'up' in possible_moves: #Avoid the top wall
        print('wall up')
        possible_moves.remove('up')
    
    
def avoid_my_neck(my_body: List[dict], possible_moves: List[str]) -> List[str]:
    
    for i in range(1,len(my_body)):
        if my_body[i]["x"] < my_body[0]["x"] and my_body[i]["y"] == my_body[0]["y"]and 'left' in possible_moves: 
            print('neck left')
            possible_moves.remove("left")

        elif my_body[i]["x"] > my_body[0]["x"] and my_body[i]["y"] == my_body[0]["y"] and 'right' in possible_moves:  
            print('neck right')
            possible_moves.remove("right")

        if my_body[i]["y"] < my_body[0]["y"] and my_body[i]["x"] == my_body[0]["x"] and 'down' in possible_moves:  
            print('neck down')
            possible_moves.remove("down")

        elif my_body[i]["y"] > my_body[0]["y"] and my_body[i]["x"] == my_body[0]["x"] and 'up' in possible_moves:  
            print('neck up')
            possible_moves.remove("up")
    
    
def avoid_snakes(my_head: Dict[str, int], snakes:List[Dict[str,str]], possible_moves: List[str]) -> List[str]:
    for i in range(1,len(snakes)):
        for j in range(len(snakes[i]['body'])):
            snakeCood = (snakes[i]['body'][j]['x'],snakes[i]['body'][j]['y'])
            if (my_head['x']+1,my_head['y']) == snakeCood:
                print('snakeavoid remove right')
                possible_moves.remove('right')
            if (my_head['x']-1,my_head['y']) == snakeCood:
                print('snakeavoid remove left')
                possible_moves.remove('left')
            if (my_head['x'],my_head['y']-1) == snakeCood:
                print('snakeavoid remove down')
                possible_moves.remove('down')
            if (my_head['x'],my_head['y']+1) == snakeCood:
                print('snakeavoid remove up')
                possible_moves.remove('up')
def CloseFood(data:Dict) -> tuple:
    foodCord = data['board']['food']
    head = (data['board']['snakes'][0]["head"])
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

def foodseeker(my_head:Dict[str,int],closerFood:tuple,possible_moves:List[str]):

    if abs((my_head['x']-1)-closerFood['coord']['x']) +  abs(my_head['y'] - closerFood['coord']['y']) <   closerFood['distance'] and 'right' in possible_moves:
        print('food remove right')
        possible_moves.remove('right')
    elif abs((my_head['x']+1)-closerFood['coord']['x']) +  abs(my_head['y'] - closerFood['coord']['y']) <   closerFood['distance']  and 'left' in possible_moves:
        print('food remove left')
        possible_moves.remove('left')
    if abs(my_head['x']-closerFood['coord']['x']) +  abs((my_head['y']+1) - closerFood['coord']['y']) <   closerFood['distance']  and 'down' in possible_moves:
        print('food remove down')
        possible_moves.remove('down')
    elif abs(my_head['x']-closerFood['coord']['x']) +  abs((my_head['y']-1) - closerFood['coord']['y']) <   closerFood['distance'] and 'up' in possible_moves:
        print('food remove up')
        possible_moves.remove('up')

def avoid_collisions(my_head: Dict[str,int], my_body: Dict[str,int],height:int,width:int,snakes:List[Dict[str,str]] ,possible_moves:List[str]) -> List[str]:
    avoid_wall(my_head,height,width,possible_moves)
    avoid_my_neck(my_body,possible_moves)

    if(len(snakes) > 1):
        avoid_snakes(my_head,snakes,possible_moves)
    return possible_moves


def choose_move(data: dict) -> str:

    my_head = data["you"]["head"]
    my_body = data["you"]["body"]  

    width = data["board"]["width"]
    height = data["board"]["height"]

    snakes = data["board"]["snakes"]

    


    #print(f"All board data this turn: {data}")


    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    avoid_collisions(my_head,my_body,height,width,snakes,possible_moves,)

    
    if(len(data["board"]["food"]) > 0 ):
        close_food = CloseFood(data)
        print(foodseeker(my_head,close_food,possible_moves))


    move = random.choice(possible_moves)

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
