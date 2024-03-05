"""
Created: 
Updated:
"""


def __frame_time(fps: int)->int:
    """Function calculates how long each frame(while loop) lasts in milliseconds and returns it."""
    pass


def get_timestamp(DEV_MODE: bool, fps: int, old_timestamp:float):
    """Calculate new unix timestamp or if DEV_MODE == true, accelarate time so 1min == 1sec. Use __frame_time."""
    pass


def init()->float:
    """Get and return initial time stamp in unix time."""
    pass


def tick(fps:int)->None:
    """Delay/sleep execution by x milliseconds. Milliseconds are calculated with __frame_time(fps: int)->int function."""
    pass

if __name__ == "__main__":
    print("Running time module tests.\n")
    # test functions
