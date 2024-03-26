from datetime import datetime
import time
from s_utils import minutes_to_seconds

logStamp = time.time()

def s_dev_Log(logLevel: bool, message: str):
    """Log 'logLevel' level messages to console and file."""
    if logLevel:
        logline = f"Log level: dev, time:{datetime.now()}, message: {message}\n"
        print(logline)
        with open("devlog.txt", "a") as f:
            f.write(logline)


def s_dev_Log_time(logLevel: bool, current_time: float):
    """Log 'logLevel' level messages to console and file."""
    global logStamp
    if logLevel and current_time > logStamp :
        logline = f"Log level: dev, time:{current_time}, Local_time: {datetime.fromtimestamp(logStamp)}\n"
        print(logline)
        with open("devlog.txt", "a") as f:
            f.write(logline)
        logStamp = current_time + minutes_to_seconds(5)