import json
from os import path
from .field import (get_planting_sites, get_recharge_station, get_seed_storage,
    release_drones)
from .drone_actions import drone_actions


def interpreter(state, env):
    """ interpreter(state, environment) -> new_state """
    # get player state
    player = state[0]
    # if it's a first step
    if player.observation.step == 0:
        player.observation.targets = get_planting_sites(env.configuration.simulationConf)
        player.observation.rechargeStation = get_recharge_station()
        player.observation.seedStorage = get_seed_storage()
    drones = player.observation.drones
    planting_sites = player.observation.targets
    # apply actions of drones
    for action in player.action:
        if action != None:
            drone_index, fun, args = action
            # if the drone is out of charge
            if drones[drone_index]["charge"]["current"] <= 0:
                drones[drone_index]["active"] = False
                drones[drone_index]["task"]["fun"] = None
                drones[drone_index]["task"]["args"] = None
            elif drones[drone_index]["active"]:
                drones[drone_index]["task"]["fun"] = fun
                drones[drone_index]["task"]["args"] = args
                drones[drone_index]["charge"]["current"] -= 1
                drone_actions[fun](player, drones[drone_index], args)
    # release more drones, if possible
    release_drones(drones, env.configuration.dronesAmount, env.configuration.simulationConf)
    # if seeds are planted at all planting sites
    if all([ps["seeds_to_plant"] <= 0 for ps in planting_sites]):
        player.status = "DONE"
    return state
