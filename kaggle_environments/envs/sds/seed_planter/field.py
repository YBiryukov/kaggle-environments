from .drone_frame import get_drone


def get_planting_sites(sim_conf):
    """ get planting sites of the field """
    # apply custom configuration to the planting site
    if "seeds_to_plant" in sim_conf:
        seeds_to_plant = sim_conf["seeds_to_plant"]
    else:
        seeds_to_plant = 10
    planting_sites = []
    x_offset = 100
    y_offset = 100
    x_step = 40
    y_step = 60
    index = 0
    # 10x5 grid of planting sites
    for i in range(5):
        this_row_x = x_offset
        for j in range(10):
            planting_sites.append({
                "index": index,
                "drone_index": None,
                "seeds_to_plant": seeds_to_plant,
                "size": 15,
                "x": this_row_x,
                "y": y_offset
            })
            index += 1
            this_row_x += x_step
        y_offset += y_step
    return planting_sites

def get_recharge_station():
    """ get recharge station, where drones can recharge/refuel """
    recharge_station = {
        "size": {
            "x": 50,
            "y": 100
        },
        "x": 515,
        "y": 150
    }
    # place to aim for the drones
    recharge_station["beacon"] = {
        "size": recharge_station["size"]["x"] // 2,
        "x": recharge_station["x"] + recharge_station["size"]["x"] // 2,
        "y": recharge_station["y"] + recharge_station["size"]["y"] // 2
    }
    return recharge_station

def get_seed_storage():
    """ get seed storage, where drones can replenish their load of seeds """
    seed_storage = {
        "size": {
            "x": 50,
            "y": 100
        },
        "x": 15,
        "y": 150
    }
    # place to aim for the drones
    seed_storage["beacon"] = {
        "size": seed_storage["size"]["x"] // 2,
        "x": seed_storage["x"] + seed_storage["size"]["x"] // 2,
        "y": seed_storage["y"] + seed_storage["size"]["y"] // 2
    }
    return seed_storage

def release_drones(drones, drones_amount, sim_conf):
    """ release drones to the field """
    if len(drones) < drones_amount:
        drone = get_drone()
        drone_index = len(drones)
        drone["index"] = drone_index
        # apply custom configuration to the drone
        if "cargo" in sim_conf:
            if "max" in sim_conf["cargo"]:
                drone["cargo"]["max"] = sim_conf["cargo"]["max"]
                drone["cargo"]["seeds"] = drone["cargo"]["max"]
        if "charge" in sim_conf:
            if "max" in sim_conf["charge"]:
                drone["charge"]["max"] = sim_conf["charge"]["max"]
                drone["charge"]["current"] = drone["charge"]["max"]
            if "recharge_speed" in sim_conf["charge"]:
                drone["charge"]["recharge_speed"] = sim_conf["charge"]["recharge_speed"]
        if "speed" in sim_conf:
            if "horizontal" in sim_conf["speed"]:
                drone["speed"]["horizontal"] = sim_conf["speed"]["horizontal"]
        drones.append(drone)
