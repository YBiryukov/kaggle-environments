import math


def clear_drone_task(drone):
    """ set to None fun and args in drone's task """
    drone["task"]["fun"] = None
    drone["task"]["args"] = None

def load_seeds(player, drone, args):
    """ load seeds to the drone's cargo hold """
    seed_storage = player.observation.seedStorage
    # if drone is at seed storage
    if (drone["position"]["x"] > seed_storage["x"] and
            drone["position"]["x"] < (seed_storage["x"] + seed_storage["size"]["x"]) and
            drone["position"]["y"] > seed_storage["y"] and
            drone["position"]["y"] < (seed_storage["y"] + seed_storage["size"]["y"])):
        drone["cargo"]["seeds"] = drone["cargo"]["max"]
        clear_drone_task(drone)

def move(player, drone, args):
    """ move the drone towards new coordinates """
    target_x = args[0]
    target_y = args[1]
    target_size = args[2]
    angle = math.atan2(target_y - drone["position"]["y"], target_x - drone["position"]["x"])
    x_velocity = drone["speed"]["horizontal"] * math.cos(angle)
    y_velocity = drone["speed"]["horizontal"] * math.sin(angle)
    drone["position"]["x"] += x_velocity
    drone["position"]["y"] += y_velocity
    distance_to_target = math.sqrt((drone["position"]["x"] - target_x) ** 2 + (drone["position"]["y"] - target_y) ** 2)
    # if target is reached
    if distance_to_target < target_size:
        clear_drone_task(drone)

def occupy_planting_site(player, drone, args):
    """ if possible, mark chosen planting site as occupied by this drone """
    target_index = args[0]
    target = player.observation.targets[args[0]]
    if target["index"] == target_index and target["drone_index"] == None:
        target["drone_index"] = drone["index"]
        drone["occupied_target_index"] = target_index
    clear_drone_task(drone)

def plant_seeds(player, drone, args):
    """ plant seeds from the drone's cargo """
    # if the drone is aimed at some target and has some seeds
    if drone["occupied_target_index"] != None and drone["cargo"]["seeds"] > 0:
        planting_site = player.observation.targets[drone["occupied_target_index"]]
        target_x = planting_site["x"]
        target_y = planting_site["y"]
        distance_to_target = math.sqrt((drone["position"]["x"] - target_x) ** 2 + (drone["position"]["y"] - target_y) ** 2)
        # if drone is at planting site
        if distance_to_target < planting_site["size"]:
            planting_site["seeds_to_plant"] -= 1
            drone["cargo"]["seeds"] -= 1
            # if more seeds must be planted at this planting site
            if planting_site["seeds_to_plant"] > 0:
                # to launch this function in the next step as well
                return
            else:
                planting_site["drone_index"] = None
                drone["occupied_target_index"] = None
    clear_drone_task(drone)

def recharge(player, drone, args):
    """ recharge/refuel the drone """
    recharge_station = player.observation.rechargeStation
    # if drone is at recharge station
    if (drone["position"]["x"] > recharge_station["x"] and
            drone["position"]["x"] < (recharge_station["x"] + recharge_station["size"]["x"]) and
            drone["position"]["y"] > recharge_station["y"] and
            drone["position"]["y"] < (recharge_station["y"] + recharge_station["size"]["y"])):
        drone["charge"]["current"] += drone["charge"]["recharge_speed"]
        # if the drone is fully recharged/refuelled
        if drone["charge"]["current"] >= drone["charge"]["max"]:
            drone["charge"]["current"] = drone["charge"]["max"]
        else:
            # to launch this function in the next step as well
            return
    clear_drone_task(drone)


drone_actions = {
    "load_seeds": load_seeds,
    "move": move,
    "occupy_planting_site": occupy_planting_site,
    "plant_seeds": plant_seeds,
    "recharge": recharge
}
