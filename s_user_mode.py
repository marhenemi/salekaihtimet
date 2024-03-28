"""
Created: ML + AT 12.3.2024
Updated: ML + AT 13.3.2024
"""
import time
import datetime
from s_motor import rotate_clockwise, rotate_counter_clockwise
from s_utils import stamp_to_midnight, hours_to_seconds, minutes_to_seconds

# List index 0 == close, 1 == open
close_times = [-1,-1]


def update_close_time(current_timestamp: float, close_time_hours: int, close_time_minutes: int, closed_duration: int):
    """Update user set closing and opening times."""
    global close_times

    # Calculates closing time
    close_times[0] = stamp_to_midnight(current_timestamp) + hours_to_seconds(close_time_hours) + minutes_to_seconds(close_time_minutes)
     # Calculates opening time
    close_times[1] = close_times[0] + hours_to_seconds(closed_duration)


def check_close_time(current_timestamp: float):
    """Checks if current_timestamp is between calculated closing and opening times."""
    # If current_timestamp is between opening and closing time, return True
    if close_times[0] < current_timestamp < close_times[1]:
        return True
    return False


def __adjust_motor(current_timestamp: float, motor_pins: tuple)->None:
    """Adjust motor open or closed based on 'current_timestamp' values"""
    # Statement is entered when check_close_time return False.
    if not check_close_time(current_timestamp):
            rotate_clockwise(motor_pins)
            return
    rotate_counter_clockwise(motor_pins)


def user_mode(current_timestamp: float, motor_pins: tuple, close_time_hours: int, close_time_minutes: int, closed_duration: int)->None:
    """Run in user mode. Takes in current time, user given close time in hours and minutes, and closed duration."""
    __adjust_motor(current_timestamp, motor_pins)

    # Checks if new closing/opening times need to be calculated.
    # if should_update_closetimes(current_timestamp):
    #     update_close_time(current_timestamp, close_time_hours, close_time_minutes, closed_duration)
    update_close_time(current_timestamp, close_time_hours, close_time_minutes, closed_duration)


if __name__ == "__main__":
    
    print("Tests")
    
    test_time = time.time()

    update_close_time(test_time, 20, 0, 8)
    print(datetime.datetime.fromtimestamp(close_times[0]))
    print(datetime.datetime.fromtimestamp(close_times[1]))