from s_logger import s_dev_Log
import RPi.GPIO as GPIO
import s_motor as MOTOR

#Dev mode globals
DEV_MODE = True
DEV_LOGGING = True

# Operation mode list and initialazation
MODE_MANUAL=11
MODE_TIME=13
MODE_AUTOMATIC=15
OPERATION_MODES = [MODE_MANUAL, MODE_TIME, MODE_AUTOMATIC]
CURRENT_OPERATION_MODE = 0

# Button pin definations
BUTTON_OPEN=3
BUTTON_CLOSE=5
MOTOR_CHANNEL=(32,36,38,40)


def cycle_operation_mode(currentMode: int, modes: list)->int:
    """Cycle through development modes inside array. Returns new operation mode index."""
    pass


def reset()->None:
    """Reset gpio, active mode and settings to default."""
    clean_up_pins()
    set_up_pins()
    CURRENT_OPERATION_MODE = 0


def set_up_pins():
    """Setup pin io modes etc..."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_OPEN, GPIO.IN)
    GPIO.setup(BUTTON_CLOSE, GPIO.IN)
    GPIO.setup(MOTOR_CHANNEL, GPIO.OUT)
    GPIO.setwarnings(DEV_MODE)
    s_dev_Log(DEV_LOGGING, "Running in development mode.")
    s_dev_Log(DEV_LOGGING, "Development logging enabled.")
    s_dev_Log(DEV_LOGGING, f"Pins: manual_mode={OPERATION_MODES[0]}, time_mode={OPERATION_MODES[1]}, automatic_mode={OPERATION_MODES[2]}")


def clean_up_pins():
    """Set everything back to 0 before shutting down."""
    GPIO.cleanup()


def main():

    while True:
        if GPIO.input(BUTTON_OPEN) == 0:
            MOTOR.rotate_clockwise(MOTOR_CHANNEL)
        if GPIO.input(BUTTON_CLOSE) == 0 and GPIO.input(BUTTON_OPEN) == 1:
            MOTOR.rotate_counter_clockwise(MOTOR_CHANNEL)



if __name__ == "__main__":
    clean_up_pins()
    set_up_pins()
    main()
