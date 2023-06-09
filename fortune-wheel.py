from random import randrange
from datetime import datetime
from time import sleep
from osrsbox import items_api
import json
import re

# ERROR LOGGING
def logError(error):
    error_log = open(".\error.log", "a")
    error_log.write(f"[{datetime.now()}]: {error}\n")
    error_log.close()

# ITEM LOADING
def tryLoadItemPropertiesTemplate():
    template_file = open(".\item_properties_template.json", "r")
    template_json = json.loads(template_file.read())
    template_file.close()
    return template_json

def loadItemPropertiesTemplate():
    try:
        return tryLoadItemPropertiesTemplate()
    except Exception as exception:
        print("Whoops! Something went wrong trying to load the item properties template!")
        print("An error message has been written to '.\error.log'!", end="\n\n")
        logError(exception)
        return json.loads("{}")

def itemMatchesTemplate(item, item_template):
    item_matches = True
    
    for property_name, regex in item_template.items():
        property_matches = re.search(str(regex), str(getattr(item, property_name))) != None
        item_matches = item_matches and property_matches

    return item_matches

def loadItems():
    print("Loading items from OSRSBox Database...", end="\r")
    items = []
    item_template = loadItemPropertiesTemplate()
    
    for item in items_api.load():
        if (itemMatchesTemplate(item, item_template)):
            items.append(item)
            
    print("Items loaded!                         ", end="\r")
    return items

ITEMS = loadItems()

# FORTUNE WHEEL
def doSpinningAnimation(iterations = 4, fps = 120):
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
