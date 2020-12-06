def fire_left_weapon(ship, SHIP_FRAME):
    """ add projectile from left weapon to the list of ship's projectiles """
    if ship["leftWeaponReloadedAfter"] == 0:
        ship["projectiles"].append([
            ship["currentPosition"]["x"] + SHIP_FRAME["weaponXCenter"],
            ship["currentPosition"]["y"]
        ])
        ship["leftWeaponReloadedAfter"] = SHIP_FRAME["leftWeapon"]["steps_for_reload"]
    else:
        hold_left_weapon(ship, SHIP_FRAME)

def fire_right_weapon(ship, SHIP_FRAME):
    """ add projectile from right weapon to the list of ship's projectiles """
    if ship["rightWeaponReloadedAfter"] == 0:
        ship["projectiles"].append([
            ship["currentPosition"]["x"] + SHIP_FRAME["size"]["x"] - SHIP_FRAME["weaponXCenter"],
            ship["currentPosition"]["y"]
        ])
        ship["rightWeaponReloadedAfter"] = SHIP_FRAME["rightWeapon"]["steps_for_reload"]
    else:
        hold_right_weapon(ship, SHIP_FRAME)

def hold_left_weapon(ship, SHIP_FRAME):
    """ reload left weapon instead of firing """
    if ship["leftWeaponReloadedAfter"] > 0:
        ship["leftWeaponReloadedAfter"] -= 1

def hold_right_weapon(ship, SHIP_FRAME):
    """ reload right weapon instead of firing """
    if ship["rightWeaponReloadedAfter"] > 0:
        ship["rightWeaponReloadedAfter"] -= 1
