import json
import random
from os import path
from .agents import agents
from .collision_detection import (asteroid_colliding_projectile,
    asteroid_colliding_ship)
from .weapons import (fire_left_weapon, fire_right_weapon,
    hold_left_weapon, hold_right_weapon)


def get_ships_and_asteroids():
    """ get list of ships of players and list of asteroids """
    # define ships of players
    ships_of_players = []
    for i in range(2):
        ships_of_players.append({
            "currentPosition": {
                "x": random.random() * CANVAS_WIDTH,
                "y": CANVAS_HEIGHT - SHIP_FRAME["size"]["y"]
            },
            "leftWeaponReloadedAfter": 0,
            "platformCargoFilledSpace": 0,
            "platformColor": ASTEROIDS_COLORS[random.randint(0, len(ASTEROIDS_COLORS) - 1)],
            "playerNumber": i + 1,
            "projectiles": [],
            "rightWeaponReloadedAfter": 0,
            "score": 0
        })

    # define asteroids
    asteroids = []
    for i in range(random.randint(13, 17)):
        asteroids.append({
            "color": ASTEROIDS_COLORS[random.randint(0, len(ASTEROIDS_COLORS) - 1)],
            "size": random.randint(10, 13),
            "speed": random.randint(3, 5),
            "x": random.random() * CANVAS_WIDTH,
            "y": random.random() * CANVAS_HEIGHT
        })
    return ships_of_players, asteroids

def html_renderer():
    js_path = path.abspath(path.join(dir_path, "asteroids.js"))
    with open(js_path, encoding="utf-8") as js_file:
        return js_file.read()

def interpreter(state, env):
    player1 = state[0]
    player2 = state[1]
    player1.observation.lastOpponentAction = player2.action
    player2.observation.lastOpponentAction = player1.action

    # define some data, if it's a first step
    if len(env.steps) == 1:
        ships_of_players, asteroids = get_ships_and_asteroids()
        env.configuration.canvasSize = [CANVAS_WIDTH, CANVAS_HEIGHT]
        env.configuration.shipFrame = {
            "leftWeaponActions": {
                "fire": 0,
                "hold": 1
            },
            "moves": {
                "port": 0,
                "starboard": 1,
                "steady": 2
            },
            "platformCargoUnitSize": SHIP_FRAME["platformCargoUnitSize"],
            "platformSize": SHIP_FRAME["platformSize"],
            "projectileSize": SHIP_FRAME["projectileSize"],
            "rightWeaponActions": {
                "fire": 0,
                "hold": 1
            },
            "shipXCenter": SHIP_FRAME["shipXCenter"],
            "size": SHIP_FRAME["size"],
            "weaponSize": SHIP_FRAME["weaponSize"],
            "weaponXCenter": SHIP_FRAME["weaponXCenter"],
            "weaponYCenter": SHIP_FRAME["weaponYCenter"]
        }
        player1.observation.asteroids = asteroids
        player2.observation.asteroids = asteroids
        player1.observation.shipsOfPlayers = [ships_of_players[0], ships_of_players[1]]
        player2.observation.shipsOfPlayers = [ships_of_players[1], ships_of_players[0]]
    # otherwise get existing data
    else:
        asteroids = player1.observation.asteroids
        ships_of_players = player1.observation.shipsOfPlayers

    # process actions of players
    players = [player1, player2]
    for i in range(len(players)):
        if len(players[i].action) == 3:
            # player's ship movement
            if players[i].action[0] < len(SHIP_FRAME["move"]) and players[i].action[0] >= 0:
                ship_move = SHIP_FRAME["move"][players[i].action[0]]
                ship_x = ships_of_players[i]["currentPosition"]["x"] + ship_move
                # if ship is in the boundaries of the canvas
                if ship_x > 0 and ship_x < CANVAS_WIDTH:
                    ships_of_players[i]["currentPosition"]["x"] = ship_x
            # player's ship left weapon action
            if players[i].action[1] < len(SHIP_FRAME["leftWeapon"]["actions"]) and players[i].action[1] >= 0:
                SHIP_FRAME["leftWeapon"]["actions"][players[i].action[1]](ships_of_players[i], SHIP_FRAME)
            # player's ship right weapon action
            if players[i].action[2] < len(SHIP_FRAME["rightWeapon"]["actions"]) and players[i].action[2] >= 0:
                SHIP_FRAME["rightWeapon"]["actions"][players[i].action[2]](ships_of_players[i], SHIP_FRAME)

    # move asteroids
    for asteroid in asteroids:
        asteroid["y"] += asteroid["speed"]
        if asteroid["y"] > CANVAS_HEIGHT:
            reset_asteroid(asteroid)

    # move projectiles and check their collision with asteroids
    for ship in ships_of_players:
        for i in range(len(ship["projectiles"]) - 1, -1, -1):
            ship["projectiles"][i][1] -= SHIP_FRAME["projectileSpeed"]
            # remove projectile if it went out of canvas
            if ship["projectiles"][i][1] < 0:
                ship["projectiles"].pop(i)
            else:
                # check collision of the projectile with asteroids
                for asteroid in asteroids:
                    if asteroid_colliding_projectile(asteroid, ship["projectiles"][i]):
                        reset_asteroid(asteroid)
                        # remove projectile
                        ship["projectiles"].pop(i)
                        break

    # check collisions between ships and asteroids
    for ship in ships_of_players:
        for asteroid in asteroids:
            if asteroid_colliding_ship(asteroid, ship, SHIP_FRAME):
                # if colors of ship's platform and asteroid are the same
                if asteroid["color"] == ship["platformColor"]:
                    ship["platformCargoFilledSpace"] += 1
                    # if ship's cargo space is full
                    if ship["platformCargoFilledSpace"] == SHIP_FRAME["platformCargoSpace"]:
                        # increase ship's score
                        ship["score"] += 1
                        # reset ship's cargo space
                        ship["platformCargoFilledSpace"] = 0
                        # change ship's platform color
                        while True:
                            ship["platformColor"] = ASTEROIDS_COLORS[random.randint(0, len(ASTEROIDS_COLORS) - 1)]
                            if asteroid["color"] != ship["platformColor"]:
                                break
                else:
                    # reset ship's score
                    ship["score"] = 0
                reset_asteroid(asteroid)

    # Specification can fully handle the reset.
    if env.done:
        return state

    step = len(env.steps)
    player1.observation.step = step
    player2.observation.step = step

    # set rewards of players
    player1.reward = ships_of_players[0]["score"]
    player2.reward = ships_of_players[1]["score"]

    remaining_steps = env.configuration.episodeSteps - step - 1
    if remaining_steps <= 0:
        player1.status = "DONE"
        player2.status = "DONE"
    return state

def renderer(state, env):
    return ""

def reset_asteroid(asteroid):
    """ redefine all asteroid's data and place it at the top of the canvas """
    asteroid["color"]: ASTEROIDS_COLORS[random.randint(0, len(ASTEROIDS_COLORS) - 1)]
    asteroid["size"]: random.randint(10, 14)
    asteroid["speed"]: random.randint(3, 5)
    asteroid["x"] = random.random() * CANVAS_WIDTH
    asteroid["y"] = 0


dir_path = path.dirname(__file__)
json_path = path.abspath(path.join(dir_path, "asteroids.json"))
with open(json_path) as json_file:
    specification = json.load(json_file)

# define constants
ASTEROIDS_COLORS = ["#a30404", "#63534b", "#1e4701"]
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 450
# define standard ship frame
SHIP_FRAME = {
    "leftWeapon": {
        "steps_for_reload": 20,
        "actions": [
            fire_left_weapon,
            hold_left_weapon
        ]
    },
    "move": [
        -3,
        3,
        0
    ],
    "platformCargoSpace": 3,
    "platformCargoUnitSize": {"x": 25, "y": 25},
    "platformSize": {"x": 75, "y": 25},
    "projectileSize": {"x": 1, "y": 12},
    "projectileSpeed": 10,
    "rightWeapon": {
        "steps_for_reload": 20,
        "actions": [
            fire_right_weapon,
            hold_right_weapon
        ]
    },
    "shipXCenter": 64,
    "size": {"x": 125, "y": 50},
    "weaponSize": {"x": 25, "y": 50},
    "weaponXCenter": 12,
    "weaponYCenter": 25
}
