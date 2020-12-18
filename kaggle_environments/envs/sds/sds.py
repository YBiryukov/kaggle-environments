import json
from os import path
# import seed planter simulation
from .seed_planter.seed_planter import interpreter as seed_planter_interpreter
from .seed_planter.basic_drone import seed_planter_basic_drone


def html_renderer(env):
    """ html_renderer(environment) -> JavaScript HTML renderer function """
    # get path to the renderer.js of the chosen simulationType
    js_path = path.abspath(path.join(dir_path, env.configuration.simulationType, "renderer.js"))
    with open(js_path, encoding="utf-8") as js_file:
        return js_file.read()

def interpreter(state, env):
    """ interpreter(state, environment) -> new_state """
    # call the interpreter corresponding with the chosen simulationType
    state = interpreters[env.configuration.simulationType](state, env)

    # Specification can fully handle the reset.
    if env.done:
        return state

    # get player state
    player = state[0]
    step = len(env.steps)
    player.observation.step = step

    # if it was the last step of the simulation
    remaining_steps = env.configuration.episodeSteps - step - 1
    if remaining_steps <= 0:
        player.status = "DONE"
    # return new state
    return state

def renderer(state, env):
    return ""


# specification is the JSON Schema representing the environment
dir_path = path.dirname(__file__)
json_path = path.abspath(path.join(dir_path, "sds.json"))
with open(json_path) as json_file:
    specification = json.load(json_file)

agents = {
    "seed_planter_basic_drone": seed_planter_basic_drone
}

# dictionary of interpreter functions of different simulations
interpreters = {
    "seed_planter": seed_planter_interpreter
}
