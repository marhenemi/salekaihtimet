"""
Created: linre-90/11.3.2024
"""

import pickle

def read_settings(filename: str):
    """Read settings from file to dictionary."""
    with open(filename, "rb") as f:
       return pickle.load(f)


def __write_user_settings(data: dict):
    """Write user settings to specific file."""
    with open("user_settings.kaihdin", "wb") as f:
        pickle.dump(data, f)


def parse_data(data: str)->bool:
    """
    Extract data from data string to dict object. Writes settings to disk if parsing is succesfull.
    Sample data: close_start=22:00;close_duration=8;latitude=63.096;longitude=21.61577;
    """
    # data shape and fields
    keys = {
        "close_start": "",
        "close_duration": "",
        "latitude": "",
        "longitude": ""
    }

    # Loop overkeys 
    for key, value in keys.items():
        # Find starting index of key from string
        index = data.find(key)
        if index < 0:
            # Malformed cant parse
            return False
        
        # Move forward to value start index
        index += len(key) + 1
        value = ""
        
        # Extract value until ';' is found. 
        for charidx in range(index, len(data)):
            if data[charidx] == ';':
                break
            value += data[charidx]
        
        # Save extracted value
        keys[key] = value

    __write_user_settings(keys)
    return True

if __name__ == "__main__":
    try:
        # Try Read user settings file and parse it
        user_settings = read_settings("user_settings.kaihdin")
        close_time = user_settings["close_start"]
        hours_mins = close_time.split(":")
        hours_mins[0], hours_mins[1] = int(hours_mins[0]), int(hours_mins[1])
        
        CLOSE_HOURS = hours_mins[0]
        CLOSE_MINS = hours_mins[1]
        CLOSE_DURATION = int(user_settings["close_duration"])
        LATITUDE = float(user_settings["latitude"])
        LONGITUDE = float(user_settings["longitude"])

        print(f"Close time: hours={CLOSE_HOURS}, min={CLOSE_MINS}")
        print(f"Close duration: {CLOSE_DURATION}")
        print(f"Location: latitude={LATITUDE}, longitude={LONGITUDE}")
    except:
        print("Something went wrong use default settings.")
        default_settings = read_settings("default_settings.kaihdin")
        print(default_settings)