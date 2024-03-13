"""
Created: ML + AT 12.3.2024
Updated: ML + AT 13.3.2024
"""

import datetime
from s_motor import rotate_clockwise, rotate_counter_clockwise

# List index 0 == close, 1 == open
close_times = [-1,-1]
update_time2 = 0


def should_update_closetimes(current_timestamp: float)->bool:
    """Check if new open and close times should be calculated. Calculation happens at 14:00."""
    # Check if current unix time has passed set update_time2, if so return True.
    if current_timestamp > update_time2:
        return True
    return False


def update_close_time(current_timestamp: float, close_time_hours: int, close_time_minutes: int, closed_duration: int):
    """Update user set closing and opening times."""
    global close_times
    # Calculates closing time
    close_times[0] = current_timestamp - (current_timestamp % 86400) + (close_time_hours * 3600) + (close_time_minutes * 60)
    # Calculates opening time
    close_times[1] = close_times[0] + (closed_duration * 3600)

    # Calculates next update time
    global update_time2
    update_time2 = current_timestamp - (current_timestamp % 86400) + 86400 + (12 * 3600)


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
            print("daytime, blinds open")
            return
    rotate_counter_clockwise(motor_pins)


def user_mode(current_timestamp: float, motor_pins: tuple, close_time_hours: int, close_time_minutes: int, closed_duration: int)->None:
    """Run in user mode. Takes in current time, user given close time in hours and minutes, and closed duration."""
    __adjust_motor(current_timestamp, motor_pins)
    print(datetime.datetime.fromtimestamp(current_timestamp))

    # Checks if new closing/opening times need to be calculated.
    if should_update_closetimes(current_timestamp):
        update_close_time(current_timestamp, close_time_hours, close_time_minutes, closed_duration)