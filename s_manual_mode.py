import RPi.GPIO as GPIO
import s_motor as MOTOR

def manual_mode(button_open: int, button_close:int, motor_channel:tuple):
    if GPIO.input(button_open) == 0:
        MOTOR.rotate_clockwise(motor_channel)
    if GPIO.input(button_close) == 0 and GPIO.input(button_open) == 1:
        MOTOR.rotate_counter_clockwise(motor_channel)