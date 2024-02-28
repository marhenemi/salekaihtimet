import RPi.GPIO as GPIO
import time
from copy import deepcopy

#Single rotation cycle of the motor
__motor_cycle = [
    (GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH),
    (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH),
    (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW),
    (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
    (GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW),
    (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW),
    (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW),
    (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
]

#Time between rotation cycles.
__motor_sleep = .005

# motor step counter, motor is assumed to be in 0 position at program start
# 28byj-48 gear ratio 64:1 results in 4096 steps/360.
__step_counter = 0

# allowed movement range 0-90deg 4096/4
__motor_min_max_steps=(0, 4096/4)


def __check_in_range(direction:int):
    """Checks whether motor is between the allowed movement range."""
    steps_after_cycle = __step_counter + direction * 8
    if steps_after_cycle >= __motor_min_max_steps[0] and \
       steps_after_cycle <= __motor_min_max_steps[1]:
        return True
    return False


def __step_motor_step(direction: int):
    """Handles step counting operations."""
    if __check_in_range(direction):
        global __step_counter
        __step_counter += direction * 8
        return True
    return False


def rotate_clockwise(motor_pins: tuple):
    """Rotates the motor clockwise with safety mechanics."""
    __turn_motor(1, motor_pins)


def rotate_counter_clockwise(motor_pins:tuple):
    """Rotates the motor counterclockwise with safety mechanics."""
    __turn_motor(-1, motor_pins)


def __turn_motor(direction: int, motor_pins:tuple):
    """Turns the motor one step and resets the pins."""
    #Check if motor can be stepped.
    if not __step_motor_step(direction):
        return
    
    #Depending on the direction reverse micro steps to create counterclockwise rotation
    mcycle = deepcopy(__motor_cycle)
    if direction < 0:
        mcycle.reverse()
    
    #run turn cycle
    for step in mcycle:
        for i in range(0,4):
            GPIO.output(motor_pins[i], step[i])
        time.sleep(__motor_sleep)
            
    #reset
    GPIO.output(motor_pins[0], GPIO.LOW)
    GPIO.output(motor_pins[1], GPIO.LOW)
    GPIO.output(motor_pins[2], GPIO.LOW)
    GPIO.output(motor_pins[3], GPIO.LOW)

