import hlt, logging
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

# def locate_borders(square):
#     direction = STILL
#     current = square
#     N_BORDER = square.game_map.width
#     borders = [N_BORDER, E_BORDER, S_BORDER, W_BORDER]
#     for square in borders:

def check_enemy_border():
    enemy_border = False
    for square in game_map:
        if square.owner == myID:
            if any(neighbor.owner not in (0, myID) for neighbor in game_map.neighbors(square)):
                enemy_border = True

    return enemy_border

def target_enemy_production(square):
    direction = STILL
    current = square
    max_distance = min(game_map.width, game_map.height) / 15
    my_production_val = sum(neighbor.production for neighbor in game_map.neighbors(current))
    for square in game_map:
        if square.owner not in (0, myID):
            production_val = sum(neighbor.production for neighbor in game_map.neighbors(square))
            strength_val = sum(neighbor.strength for neighbor in game_map.neighbors(square))
            if production_val > my_production_val and square.strength > strength_val / 4 :
                for d in (NORTH, EAST, SOUTH, WEST):
                    distance = 0

                    # while current.owner == myID and distance < max_distance:
                    #     distance += 1
                    #     current = game_map.get_target(current, d)
                    #
                    # if distance < max_distance:
                    #     direction = d
                    #     max_distance = direction

                    current = game_map.get_target(current, d)
                    distance = game_map.get_distance(square, current)
                    if distance < max_distance:
                        direction = d

                    return direction
            else:
                direction = STILL
                return direction

#def attack_enemy(square):
    # 3 borders should begin attacking enemy, one border should continue expansion if possible (will need to account for if not)
    # consider distance between border where enemy is present
    # consider highest production areas near borders of my bot
        # potentially through find highest production areas
        # potentially through if production is greater than some arbitrary number...
        # potentially through adding sum of border production??
    # direction = STILL
    # current = square
    # square_production_val


def target_neutral_production(square):
    direction = STILL
    current = square
    max_distance = min(game_map.width, game_map.height) / 5
    my_production_val = sum(neighbor.production for neighbor in game_map.neighbors(current))

    for square in game_map:
        if square.owner not in (1, myID):
            production_val = sum(neighbor.production for neighbor in game_map.neighbors(square))
            strength_val = sum(neighbor.production for neighbor in game_map.neighbors(square))
            if production_val > my_production_val - 5 and square.strength > strength_val / 5 :
                for d in (NORTH, EAST, SOUTH, WEST):
                    distance = 0

                    while current.owner == myID and distance < max_distance:
                        distance += 1
                        current = game_map.get_target(current, d)

                    if distance < max_distance:
                        direction = d

                    return direction


def find_nearest_enemy_direction(square):
    direction = NORTH
    max_distance = min(game_map.width, game_map.height) / 2

    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square

        while current.owner == myID and distance < max_distance :
            distance+= 1
            current = game_map.get_target(current, d)

        if distance < max_distance :
            direction = d
            max_distance = direction

    return direction

def heuristic(square):
    if square.owner == 0 :
        return (pow(square.production, 2) + 1) / (square.strength + 1)
    else :
        return sum(neighbor.strength for neighbor in game_map.neighbors(square) if neighbor.owner not in (0, myID))

def assign_move(square):
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                             if neighbor.owner != myID),
                            default=(None,None),
                            key=lambda t: heuristic(t[0]))
    if direction is not None and target.strength < square.strength:
        enemy_border = check_enemy_border()
        if enemy_border:
            direction = target_enemy_production(square)
            return Move(square,direction)
        else :
            return Move(square,direction)
    elif square.strength < square.production * 3:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        # direction = target_neutral_production(square)
        # if direction is not STILL:
        #     return Move(square,direction)
        # else:
        #     direction = target_enemy_production(square)
        #     if direction is not None:
        #         return Move(square, direction)

        # direction = target_enemy_production(square)
        # if direction is not None:
        #     return Move(square, direction)

        if square.strength < square.production * 3 :
            return Move(square, STILL)
        direction = find_nearest_enemy_direction(square)
        if direction is not None:
            return Move(square, direction)

    else :
        return Move(square, STILL)



while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)