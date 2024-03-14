"""
Created: ML + AT 12.3.2024
Updated:
"""
import time
import datetime
from s_motor import rotate_clockwise, rotate_counter_clockwise
from s_utils import stamp_to_midnight, hours_to_seconds, minutes_to_seconds

# 0 == close, 1 == open
close_times = [-1,-1]
update_time2 = 0

def should_update_closetimes(current_timestamp: float)->bool:
    """Check if new open and close times should be calculated. Calculation happens 14:00."""
    #Check if current unix time has passed set update_time2, if so return True.
    if current_timestamp > update_time2:
        return True
    return False

def check_close_time(current_timestamp: float):
    """Checks if current_timestamp is between calculated closing and opening times."""
    if close_times[0] < current_timestamp < close_times[1]:
        return True
    return False

def update_close_time(current_timestamp: float, close_time_hours: int, close_time_minutes: int, closed_duration: int):
    """Update user set closing and opening times."""
    global close_times
    close_times[0] = stamp_to_midnight(current_timestamp) + hours_to_seconds(close_time_hours) + minutes_to_seconds(close_time_minutes)
    close_times[1] = close_times[0] + hours_to_seconds(closed_duration)

    global update_time2
    update_time2 = stamp_to_midnight(current_timestamp) + hours_to_seconds(12) + 86400

def __adjust_motor(current_timestamp: float, motor_pins: tuple)->None:
    """Adjust motor open or close based on 'sunrise_sunset_timestamp' values"""
    if not check_close_time(current_timestamp):
            rotate_clockwise(motor_pins)
            print("daytime blinds open")
            return
    rotate_counter_clockwise(motor_pins)


def user_mode(current_timestamp: float, motor_pins: tuple, close_time_hours: int, close_time_minutes: int, closed_duration: int)->None:
    """Run in time mode. Takes in frames and current time."""
    __adjust_motor(current_timestamp, motor_pins)
    print(datetime.datetime.fromtimestamp(current_timestamp))

    if should_update_closetimes(current_timestamp):
        update_close_time(current_timestamp, close_time_hours, close_time_minutes, closed_duration)


if __name__ == "__main__":
    
    print("Tests")
    
    test_time = time.time()

    update_close_time(test_time, 20, 0, 8)
    print(datetime.datetime.fromtimestamp(close_times[0]))
    print(datetime.datetime.fromtimestamp(close_times[1]))
    print(datetime.datetime.fromtimestamp(update_time2))