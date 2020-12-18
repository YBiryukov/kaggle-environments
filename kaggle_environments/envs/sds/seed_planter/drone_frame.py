def get_drone():
    """ get a standard drone """
    return {
        # should this drone be considered in the simulation
        "active": True,
        # drone's battery charge or fuel amount
        "charge": {
            # maximum charge capacity
            "max": 500,
            # current charge
            "current": 500,
            # recharge per step
            "recharge_speed": 50
        },
        # drone's cargo data
        "cargo": {
            # maximum cargo capacity
            "max": 13,
            # current load of seeds
            "seeds": 13
        },
        # index of this drone
        "index": None,
        "occupied_target_index": None,
        "position": {
            "x": 0,
            "y": 0
            # "z"
        },
        "size": {
            "width": 7
            # "height": 3,
            # "length": 4
        },
        "speed":{
            "horizontal": 3
            # "vertical": 2
        },
        # drone's current task
        "task": {"fun": None, "args": None}
    }
