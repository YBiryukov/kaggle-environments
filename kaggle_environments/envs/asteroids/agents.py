import random


def random_bot(obs, conf):
    """ all actions of this bot are random """
    ship_frame = conf.shipFrame
    # ship movement action
    moves = list(ship_frame["moves"].keys())
    ship_movement_action = ship_frame["moves"][moves[random.randint(0, len(moves) - 1)]]
    # left weapon action
    left_weapon_actions = list(ship_frame["leftWeaponActions"].keys())
    left_weapon_action = ship_frame["leftWeaponActions"][left_weapon_actions[random.randint(0, len(left_weapon_actions) - 1)]]
    # right weapon action
    right_weapon_actions = list(ship_frame["rightWeaponActions"].keys())
    right_weapon_action = ship_frame["rightWeaponActions"][right_weapon_actions[random.randint(0, len(right_weapon_actions) - 1)]]
    return [ship_movement_action, left_weapon_action, right_weapon_action]


agents = {
    "random_bot": random_bot
}
