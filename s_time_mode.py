"""
Created:
Updated:
"""

from s_utils import calc_sun_rise_n_set

# 0 == rise, 1 == set
sunrise_sunset_timestamp = []


def __update_sun_timestamps(latitude_longitude: tuple, current_timestamp: float)->None:
    """Update sun time stamps."""
    global sunrise_sunset_timestamp
    # Update 'sunrise_sunset_timestamp' with new values. 
    # 0 == rising time
    # 1 == setting time
    pass


def __should_update_suntimes(current_timestamp: float)->bool:
    """Check if new sunrise and sunset times should be calculated. Calculation happens after midnight."""
    # Check if current time is midnight + offset
    pass


def __adjust_motor(direction: int)->None:
    """Adjust motor open or close based on 'sunrise_sunset_timestamp' values"""
    pass


def time_mode(current_timestamp: float, latitude_longitude: tuple)->None:
    """Run in time mode. Takes in frames and current time."""

    # Determinate whether to use morning timestamp or evening timestamp based on current time

    # Rotate motor open or close, motor has limit that it cannot go over boundaries and motor functions return early if it cannot rotate.

    # Last check is __should_update_suntimes() return early if no update need.
    pass

