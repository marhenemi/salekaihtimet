"""
Created: ML + AT + linre-90/1.03.2024
Updated: 
"""

import RPi.GPIO as GPIO
import s_motor as MOTOR

def manual_mode(button_open: int, button_close:int, motor_channel:tuple):
    """Listens to button presses from button_open and button_close,
    and rotates the motor accordingly."""
    if GPIO.input(button_open) == 0:
        MOTOR.rotate_clockwise(motor_channel)
    if GPIO.input(button_close) == 0 and GPIO.input(button_open) == 1:
        MOTOR.rotate_counter_clockwise(motor_channel)
