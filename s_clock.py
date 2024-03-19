"""
Created: linre-90/19.03.2024
Updated:
"""

import time
from datetime import datetime

# Predifened speed constants
T_SCALE_2X = 2
T_SCALE_5X = 5
T_SCALE_10X = 10
T_SCALE_50X = 50
T_SCALE_100X = 100
T_SCALE_1000X = 1000
T_SCALE_5000X = 5000


def clock_init()->float:
    """Initialize timestamp."""
    return time.time()


def clock_stamp():
    """Get snapshot from current time."""
    return datetime.now()


def clock_update_time(timestamp: float, dev_mode: bool, delta: float, time_scale: float):
    """Update software time stamp to either speed up development or use normal time."""
    if not dev_mode:
        return time.time()
    # add seconds to time stamp scale delta microseconds to seconds.
    return timestamp + (delta * .000001) * time_scale


def clock_run(dev_mode)->None:
    """This ensures that there is always atleast 10 ms delay in devmode."""
    if dev_mode:
        time.sleep(0.00001)


if __name__ == "__main__":
    timestamp = clock_init()
    dev_mode = True
    while(True):
        t_start = clock_stamp()
        for x in range(0,10):
            pass
        clock_run(dev_mode)
        t_end = clock_stamp()
        t_delta = t_end - t_start
        
        timestamp = clock_update_time(timestamp, dev_mode, t_delta.microseconds, T_SCALE_100X)
        print(datetime.fromtimestamp(timestamp))
