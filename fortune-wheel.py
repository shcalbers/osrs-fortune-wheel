from random import randrange
from datetime import datetime
from time import sleep
from osrsbox import items_api
import json
import re

def loadConfig():
    config_file = open(".\item_properties_template.json", "r")
    config_json = json.loads(config_file.read())
    config_file.close()
    return config_json

def tryLoadItemsWithConfig():
    items_dictionary: Dict[int, ItemProperties] = dict()
    item_config = loadConfig()

    current_id = 0
    for item in items_api.load():
        item_is_valid = True
        for property_name, regex in item_config.items():
            property_is_valid = re.search(str(regex), str(getattr(item, property_name))) != None
            item_is_valid = item_is_valid and property_is_valid
            
        if (item_is_valid):
            items_dictionary[current_id] = item
            current_id += 1

    return items_dictionary

def loadItems():
    items = None
    
    try:
        print("Loading items from OSRSBox Database...", end="\r")
        items = tryLoadItemsWithConfig()
        print("Items loaded!                         ", end="\r")
    except Exception as exception:
        print("Whoops! Something went wrong trying to load the items using the config!")
        print("An error message has been written to '.\error.log'!", end="\n\n")
        logError(exception)
        items = items_api.load()

    return items

ITEMS = loadItems()

def logError(error):
    error_log = open(".\error.log", "a")
    error_log.write(f"[{datetime.now()}]: {error}\n")
    error_log.close()    

def doSpinningAnimation(iterations = 6, fps = 120):
    ANIMATION_FRAMES = "                       ########                       "
    ANIMATION_FRAME_LENGTH = 31
    ANIMATION_TURNPOINT_LEFT = 0
    ANIMATION_TURNPOINT_RIGHT = 24
    ANIMATION_DIRECTION_FORWARD = +1
    ANIMATION_DIRECTION_BACKWARD = -1

    interval = 1.0 / fps;
    direction = ANIMATION_DIRECTION_BACKWARD
    next_turnpoint = ANIMATION_TURNPOINT_LEFT
    frame_pointer = ANIMATION_TURNPOINT_RIGHT
    for iteration in range(iterations):
        while True:
            print(ANIMATION_FRAMES[frame_pointer:frame_pointer+ANIMATION_FRAME_LENGTH], end="\r")
            if (frame_pointer != next_turnpoint):
                frame_pointer += direction
                sleep(interval)
            else:
                if (direction == ANIMATION_DIRECTION_BACKWARD):
                    direction = ANIMATION_DIRECTION_FORWARD
                    next_turnpoint = ANIMATION_TURNPOINT_RIGHT
                else:
                    direction = ANIMATION_DIRECTION_BACKWARD
                    next_turnpoint = ANIMATION_TURNPOINT_LEFT
                    
                break

def spinFortuneWheel():
    print("Spinning the Wheel of Fortune!")
    doSpinningAnimation()
    random_item_id = randrange(0, len(ITEMS))
    print(f"Your current objective is: {ITEMS[random_item_id].name}!", end="\n\n")

def playFortuneWheel():
    print("Welcome to the Wheel of Fortune!");
    print("Type 'spin' to spin for a random objective, or type 'stop' to end this session.")
    while True:
        print("Command: ", end="")
        command = input()
        if (command == "spin"):
            spinFortuneWheel()
        elif (command == "stop"):
            print("Goodbye!")
            sleep(1)
            break
        else:
            print("Unknown Command! Expected either 'spin' or 'stop'!")

def main():
    while True:
        try:
            playFortuneWheel()
        except Exception as exception:
            print("Whoops! Something went wrong! Restarting the wheel!")
            print("An error message has been written to '.\error.log'!")
            logError(exception)
            continue

        break
            
    
if __name__ == "__main__":
    main()
