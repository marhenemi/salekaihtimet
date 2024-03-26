"""
Created: ML + AT 6.3.2024
Updated: AT 13.3.2024
"""

import time
import datetime
from s_utils import calc_sun_rise_n_set, stamp_to_midnight, hours_to_seconds, minutes_to_seconds
from s_motor import rotate_clockwise
from s_user_mode import check_close_time, user_mode
from s_memory import init_memory, read_mem_average, use_memory, is_memory_hydrated
from s_light_sensor import sensor_read_single_value, sensor_val_to_percentage
from s_motor import turn_motor_percentage
from s_logger import s_dev_Log

# List index 0 == rise, 1 == set
sunrise_sunset_timestamp = []
update_time = 0
adjust_time = 0
snapshot_time = 0
snapshot_adjust_interval = [-1,-1]


def automatic_init(adjust_interval, snapshot_interval, current_timestamp):
    """Initialize automatic module. 
    'Adjust_interval' is interval when motor adjusts, passed in as minutes. 
    'snapshot_interval' is passed in as seconds.
    """
    init_memory(adjust_interval, snapshot_interval, current_timestamp)
    global adjust_time 
    adjust_time = current_timestamp
    global snapshot_time
    snapshot_time = current_timestamp
    global snapshot_adjust_interval
    snapshot_adjust_interval[0] = snapshot_interval
    snapshot_adjust_interval[1] = minutes_to_seconds(adjust_interval)


def update_sun_timestamps(latitude_longitude: tuple, current_timestamp: float)->None:
    """Update sun timestamps."""
    global sunrise_sunset_timestamp
    # Calculates new sunrise and sunset times.
    sunrise_sunset_timestamp = calc_sun_rise_n_set(stamp_to_midnight(current_timestamp) + 60, latitude_longitude[0], latitude_longitude[1])
    # Calculates next update time.
    global update_time
    update_time = stamp_to_midnight(current_timestamp) + hours_to_seconds(2) + 86400


def __should_update_suntimes(current_timestamp: float)->bool:
    """Check if new sunrise and sunset times should be calculated. Calculation happens after midnight."""
    #Check if current unix time has passed set update_time, if so return True.
    if current_timestamp > update_time:
        return True
    return False


def __adjust_motor(current_timestamp: float, motor_pins: tuple)->None:
    """Adjust motor open or close based on 'sunrise_sunset_timestamp' values"""
    # Statement is entered when current_timestamp is between current sunrise and -set times.
    if sunrise_sunset_timestamp[0] < current_timestamp < sunrise_sunset_timestamp[1]:
        # if mem update time -> insert new brightness value to memory.
        global snapshot_time
        if current_timestamp > snapshot_time:
            use_memory(sensor_val_to_percentage(sensor_read_single_value(31)), current_timestamp)
            snapshot_time = current_timestamp + snapshot_adjust_interval[0]

        global adjust_time
        if current_timestamp > adjust_time and is_memory_hydrated():
            # if motor adjust time get average from memory and adjust motor.
            sensor_average = read_mem_average()
            s_dev_Log(True, f"time: {current_timestamp}, mem_average:{sensor_average}")
            turn_motor_percentage(motor_pins, sensor_average)
            adjust_time = current_timestamp + snapshot_adjust_interval[1]
        return
    rotate_clockwise(motor_pins)




def automatic_mode(current_timestamp: float, latitude_longitude: tuple, motor_pins: tuple, close_time_hours: int, close_time_minutes: int, closed_duration: int)->None:
    """Run in automatic mode. Takes in frames and current time."""
    # Check if __should_update_suntimes() return early if no update needed
    if __should_update_suntimes(current_timestamp):
        update_sun_timestamps(latitude_longitude, current_timestamp)

    # If current_timestamp between user set closed times, or if the sun does not rise or set, run user_mode.
    if check_close_time(current_timestamp) or (sunrise_sunset_timestamp[0] == 0 and sunrise_sunset_timestamp[1] == 0):
        user_mode(
                current_timestamp, 
                motor_pins, 
                close_time_hours, 
                close_time_minutes,
                closed_duration
            )
        print("inside if")
        return
    __adjust_motor(current_timestamp, motor_pins)