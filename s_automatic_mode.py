"""
Created: ML + AT 6.3.2024
Updated:
"""

from s_utils import calc_sun_rise_n_set
import time
import datetime
from s_time import tick, init, get_timestamp
from s_motor import rotate_clockwise, rotate_counter_clockwise
from s_user_mode import check_close_time, update_close_time, should_update_closetimes

# 0 == rise, 1 == set
sunrise_sunset_timestamp = []
update_time = 0



def update_sun_timestamps(latitude_longitude: tuple, current_timestamp: float)->None:
    """Update sun timestamps."""
    global sunrise_sunset_timestamp
    sunrise_sunset_timestamp = calc_sun_rise_n_set(current_timestamp, latitude_longitude[0], latitude_longitude[1])
    #calculate next sunrise and sunset update time
    global update_time
    update_time = current_timestamp - (current_timestamp % 86400) + 86400 + (2 * 3600)


def __should_update_suntimes(current_timestamp: float)->bool:
    """Check if new sunrise and sunset times should be calculated. Calculation happens after midnight."""
    #Check if current unix time has passed set update_time, if so return True.
    if current_timestamp > update_time:
        return True
    return False


def __adjust_motor(current_timestamp: float, motor_pins: tuple)->None:
    """Adjust motor open or close based on 'sunrise_sunset_timestamp' values"""
    if not check_close_time(current_timestamp):
        if sunrise_sunset_timestamp[0] < current_timestamp < sunrise_sunset_timestamp[1]:
            rotate_clockwise(motor_pins)
            print("inside sunrise/set")
            return
    rotate_counter_clockwise(motor_pins)


def automatic_mode(current_timestamp: float, latitude_longitude: tuple, motor_pins: tuple, close_time_hours: int, close_time_minutes: int, closed_duration: int)->None:
    """Run in time mode. Takes in frames and current time."""
    __adjust_motor(current_timestamp, motor_pins)
    print(datetime.datetime.fromtimestamp(current_timestamp))
    # Determine whether to use morning timestamp or evening timestamp based on current time
    # Rotate motor open or close, motor has limit that it cannot go over boundaries and motor functions return early if it cannot rotate.
    # Last check is __should_update_suntimes() return early if no update need
    if __should_update_suntimes(current_timestamp):
        update_sun_timestamps(latitude_longitude, current_timestamp)
    if should_update_closetimes(current_timestamp):
        update_close_time(current_timestamp, close_time_hours, close_time_minutes, closed_duration)


if __name__ == "__main__":
    #Vaasa coordinates
    update_sun_timestamps((63.096, 21.61577), time.time())

    test_time = init()
    while True:
        tick(1)
        test_time = get_timestamp(True,1,test_time)
        print(datetime.datetime.fromtimestamp(test_time))
        if __should_update_suntimes(test_time):
            print("New suntimes calculated.")
            update_sun_timestamps((63.096, 21.61577), test_time)
