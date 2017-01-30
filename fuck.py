def find_high_production_areas(square) :
    high_production_areas = []
    if len(high_production_areas) == 0:
        return []

    prod_val = 0
    x = 1
    y = 1

    for neighbor in game_map :
        if (neighbor.x == x) and (neighbor.y == y) :
            prod_val = sum((neighbor.production / neighbor.strength) for neighbor in game_map.neighbors(square) if neighbor.owner not in (0, myID))
            x +=3
            y +=3

        high_production_areas.append(prod_val)

    high_production_areas.sort()
    high_production_areas = high_production_areas[0:6]

    return high_production_areas