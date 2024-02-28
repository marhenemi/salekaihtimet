from datetime import datetime

def s_dev_Log(logLevel: bool, message: str):
    """Log 'logLevel' level messages to console and file."""
    if logLevel:
        logline = f"Log level: dev, time:{datetime.now()}, message: {message}\n"
        print(logline)
        with open("devlog.txt", "a") as f:
            f.write(logline)