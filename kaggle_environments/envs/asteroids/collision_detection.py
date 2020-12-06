def asteroid_colliding_projectile(asteroid, projectile):
    """ check if asteroid has collided with projectile """
    if ((asteroid["x"] + asteroid["size"]) >= projectile[0] and
            (asteroid["x"] - asteroid["size"]) <= projectile[0] and
            (asteroid["y"] + asteroid["size"]) >= projectile[1] and
            (asteroid["y"] - asteroid["size"]) <= projectile[1]):
        return True
    else:
        return False

def asteroid_colliding_ship(asteroid, ship, ship_frame):
    """ check if asteroid has collided with the ship """
    if ((asteroid["x"] + asteroid["size"]) >= ship["currentPosition"]["x"] and
            (asteroid["x"] - asteroid["size"]) <= (ship["currentPosition"]["x"] + ship_frame["size"]["x"]) and
            (asteroid["y"] + asteroid["size"]) >= ship["currentPosition"]["y"] and
            (asteroid["y"] - asteroid["size"]) <= (ship["currentPosition"]["y"] + ship_frame["size"]["y"])):
        return True
    else:
        return False
