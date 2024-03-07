"""
Created: 5.3.2024 ML + AT
Updated: 6.3.2024 ML + AT
"""

import time
import math
import datetime

# Time scaling 1 min == 1 sec
skip_minute = 60
# Time scaling 60 min == 1 sec
skip_hour = 3600
speed = skip_hour

def __frame_time(fps: int)->int:
    """Function calculates how long each frame (in while -loop) lasts in milliseconds and returns it."""
    result = 1000 / fps
    return result

def get_timestamp(DEV_MODE: bool, fps: int, old_timestamp:float)->float:
    """Calculate new unix timestamp or if DEV_MODE == true, accelarate time so 1min == 1sec. Use __frame_time."""
    if DEV_MODE == True:
        dev_time = math.ceil(old_timestamp + ((__frame_time(fps) * speed) / 1000))
        return dev_time
    return time.time()

def init()->float:
    """Get and return initial time stamp in unix time."""
    current_unix_timestamp = time.time()
    return current_unix_timestamp

def tick(fps:int)->None:
    """Delay/sleep execution by X milliseconds. Milliseconds are calculated with __frame_time(fps: int)->int function."""
    #print("test 1")
    time.sleep(__frame_time(fps)/1000)
    #print("test 2")

if __name__ == "__main__":
    print("Running time module tests.\n")
    # test functions
    place_holder_time = init()
    while True:
        tick(1)
        place_holder_time = get_timestamp(True,1,place_holder_time)
        print(datetime.datetime.fromtimestamp(place_holder_time))
