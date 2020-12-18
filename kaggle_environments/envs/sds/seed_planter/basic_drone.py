import math


def at_occupied_planting_site(obs, conf, drone):
    """ this drone's actions at planting site occupied by this drone """
    if drone["occupied_target_index"] != None:
        target_x = obs["targets"][drone["occupied_target_index"]]["x"]
        target_y = obs["targets"][drone["occupied_target_index"]]["y"]
        distance_to_target = math.sqrt((drone["position"]["x"] - target_x) ** 2 + (drone["position"]["y"] - target_y) ** 2)
        if distance_to_target < obs["targets"][drone["occupied_target_index"]]["size"]:
            return [drone["index"], "plant_seeds", []]
    return None

def at_recharge_station(obs, conf, drone):
    """ this drone's actions at recharge station """
    recharge_station = obs["rechargeStation"]
    if (drone["position"]["x"] > recharge_station["x"] and
            drone["position"]["x"] < (recharge_station["x"] + recharge_station["size"]["x"]) and
            drone["position"]["y"] > recharge_station["y"] and
            drone["position"]["y"] < (recharge_station["y"] + recharge_station["size"]["y"]) and
            drone["charge"]["current"] < drone["charge"]["max"]):
        return [drone["index"], "recharge", []]
    return None

def at_seed_storage(obs, conf, drone):
    """ this drone's actions at seed storage """
    seed_storage = obs["seedStorage"]
    if (drone["position"]["x"] > seed_storage["x"] and
            drone["position"]["x"] < (seed_storage["x"] + seed_storage["size"]["x"]) and
            drone["position"]["y"] > seed_storage["y"] and
            drone["position"]["y"] < (seed_storage["y"] + seed_storage["size"]["y"]) and
            drone["cargo"]["seeds"] < drone["cargo"]["max"]):
        return [drone["index"], "load_seeds", []]
    return None

def check_seeds_load(obs, conf, drone):
    """ check if this drone has enough seeds """
    if drone["cargo"]["seeds"] <= 0:
        seed_storage = obs["seedStorage"]
        return [drone["index"], "move", [seed_storage["beacon"]["x"], seed_storage["beacon"]["y"], seed_storage["beacon"]["size"]]]
    return None

def find_new_task(obs, conf, drone):
    """ find new task for a drone """
    for task in tasks:
        action = task(obs, conf, drone)
        if action != None:
            return action
    return None

def occupy_planting_site(obs, conf, drone):
    """ get closest to this drone unoccupied planting site """
    the_target = None
    distance_to_the_target = None
    # search through unoccupied planting sites with not all seeds planted
    for target in [t for t in obs["targets"] if t["drone_index"] == None and t["seeds_to_plant"] > 0]:
        dist = math.sqrt((drone["position"]["x"] - target["x"]) ** 2 + (drone["position"]["y"] - target["y"]) ** 2)
        if distance_to_the_target == None or dist < distance_to_the_target:
            the_target = target
            distance_to_the_target = dist
    if the_target != None:
        return [drone["index"], "occupy_planting_site", [the_target["index"]]]
    return None

def proceed_to_occupied_planting_site(obs, conf, drone):
    """ proceed to previously occupied planting site, if any """
    if drone["occupied_target_index"] != None:
        the_target = obs["targets"][drone["occupied_target_index"]]
        return [drone["index"], "move", [the_target["x"], the_target["y"], the_target["size"]]]
    return None

def seed_planter_basic_drone(obs, conf):
    """ self-management of seed_planter_basic_drone """
    # actions of the Swarm
    actions = []
    # get active drones
    drones = [drone for drone in obs.drones if drone["active"]]
    recharge_station = obs.rechargeStation
    # consider every drone as seed_planter_basic_drone
    for drone in drones:
        # distance to recharge station
        dist = math.sqrt((drone["position"]["x"] - recharge_station["beacon"]["x"]) ** 2 + (drone["position"]["y"] - recharge_station["beacon"]["y"]) ** 2)
        # check if the drone doesn't have enough charge to continue
        if ((dist + recharge_station["beacon"]["size"]) >= (drone["speed"]["horizontal"] * drone["charge"]["current"]) and
                dist > recharge_station["beacon"]["size"]):
            # send the drone to recharge station
            # append this drone's action to actions of the Swarm
            actions.append([drone["index"], "move", [recharge_station["beacon"]["x"], recharge_station["beacon"]["y"], recharge_station["beacon"]["size"]]])
        elif drone["task"]["fun"] == None:
            # find new task for the drone
            # append this drone's action to actions of the Swarm
            actions.append(find_new_task(obs, conf, drone))
        else:
            # continue with current task
            # append this drone's action to actions of the Swarm
            actions.append([drone["index"], drone["task"]["fun"], drone["task"]["args"]])
    return actions


tasks = [
    at_recharge_station,
    at_seed_storage,
    check_seeds_load,
    at_occupied_planting_site,
    proceed_to_occupied_planting_site,
    occupy_planting_site
]
