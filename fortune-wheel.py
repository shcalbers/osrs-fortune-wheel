from random import randrange
from datetime import datetime
from time import sleep
from osrsbox import items_api

print("Loading items from OSRSBox Database...", end="\r")
items = items_api.load()
print("Items loaded!                         ", end="\r")

def logError(error):
    errorLog = open("error.log", "a")
    errorLog.write(f"[{datetime.now()}]: {error}\n")
    errorLog.close()

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
    randomItemID = randrange(0, len(items))
    print(f"Your current objective is: {items[randomItemID].name}!", end="\n\n")

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
            logError(str(exception))
            continue

        break
            
    
if __name__ == "__main__":
    main()
