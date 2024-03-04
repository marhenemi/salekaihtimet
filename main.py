from s_logger import s_dev_Log
import RPi.GPIO as GPIO
import s_motor as MOTOR
from s_manual_mode import manual_mode
import signal
import sys

#Dev mode globals
DEV_MODE = True
DEV_LOGGING = True

# Operation mode pin list and initialization
MODE_MANUAL=11 #Red
MODE_TIME=13 #Blue
MODE_AUTOMATIC=15 #Green
OPERATION_MODES = [MODE_MANUAL, MODE_TIME, MODE_AUTOMATIC]
CURRENT_OPERATION_MODE = 0

# Button pin definitions
BUTTON_OPEN=3
BUTTON_CLOSE=5
BUTTON_MODE=7
MOTOR_CHANNEL=(32,36,38,40)


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
    GPIO.setup(BUTTON_MODE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(MODE_MANUAL, GPIO.OUT)
    GPIO.setup(MODE_TIME, GPIO.OUT)
    GPIO.setup(MODE_AUTOMATIC, GPIO.OUT)
    GPIO.setwarnings(DEV_MODE)
    s_dev_Log(DEV_LOGGING, "Running in development mode.")
    s_dev_Log(DEV_LOGGING, "Development logging enabled.")
    s_dev_Log(DEV_LOGGING, f"Pins: manual_mode={OPERATION_MODES[0]}, time_mode={OPERATION_MODES[1]}, automatic_mode={OPERATION_MODES[2]}")


def clean_up_pins():
    """Set everything back to 0 before shutting down."""
    GPIO.cleanup()


def mode_toggle(channel):
    """Cycles through the operation modes."""
    if channel == BUTTON_MODE:
        global CURRENT_OPERATION_MODE
        #If CURRENT_OPERATION_MODE can be incremented and stay under 3,
        #increment the variable. If not, give CURRENT_OPERATION_MODE value 0
        #to cycle to first mode.
        if CURRENT_OPERATION_MODE + 1 <= 2:
            CURRENT_OPERATION_MODE += 1
            s_dev_Log(DEV_LOGGING, f"Mode change to {CURRENT_OPERATION_MODE}")
            mode_light_toggle()
            return
        CURRENT_OPERATION_MODE = 0
        s_dev_Log(DEV_LOGGING, f"Mode change to {CURRENT_OPERATION_MODE}")
        mode_light_toggle()


def mode_light_toggle():
    "Lights up the corresponding colored LED while changing operation modes."
    if CURRENT_OPERATION_MODE == 0:
        #Manual mode red led
        GPIO.output(MODE_MANUAL, GPIO.HIGH)
        GPIO.output(MODE_TIME, GPIO.LOW)
        GPIO.output(MODE_AUTOMATIC, GPIO.LOW)
    if CURRENT_OPERATION_MODE == 1:
        #Time mode blue led
        GPIO.output(MODE_MANUAL, GPIO.LOW)
        GPIO.output(MODE_TIME, GPIO.HIGH)
        GPIO.output(MODE_AUTOMATIC, GPIO.LOW)
    if CURRENT_OPERATION_MODE == 2:
        #Automatic mode green led
        GPIO.output(MODE_MANUAL, GPIO.LOW)
        GPIO.output(MODE_TIME, GPIO.LOW)
        GPIO.output(MODE_AUTOMATIC, GPIO.HIGH)


def handle_keyboard_interrupt(sig, frame):
    """Assisting function for development."""
    clean_up_pins()
    sys.exit(0)


def main():
    if DEV_MODE:
        signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
    GPIO.add_event_detect(BUTTON_MODE, GPIO.FALLING, callback=mode_toggle, bouncetime=2000)
    mode_light_toggle()

    #Main program loop that selects the operation mode.
    while True:
        if CURRENT_OPERATION_MODE == 0:
            manual_mode(BUTTON_OPEN, BUTTON_CLOSE, MOTOR_CHANNEL)
        if CURRENT_OPERATION_MODE == 1:
            pass
        if CURRENT_OPERATION_MODE == 2:
            pass
        


if __name__ == "__main__":
    clean_up_pins()
    set_up_pins()
    main()
