# Automatic Blinds
Automatic Blinds is a project for an embedded software course. The blinds adjust themselves based on user actions, time, and outdoor conditions.
Blinds are partially controlled with Android application found in the following repository: https://github.com/linre-90/SalekaihtimetApp  

## Description
The project is coded in Python (C style) and runs on Raspberry Pi 4. Users of the blinds can choose between three different operational modes:

- Automatic
- Time
- Manual

#### Automatic
In automatic mode, the program adjusts the blind state based on time and outdoor brightness, with brightness measured using a simple resistor. This is the expected default mode, requiring very little to no user interaction.

#### Time
In time mode, blinds are adjusted based on calculated sunrise/sunset times.

#### Manual
In manual mode, the user has the option to control blinds with two different buttons. Buttons smoothly adjust blinds to open and close. No automation is applied in this operation mode.

## Components
- Raspberry Pi 4
- 28BYJ-48 stepper motor
- 4 buttons (setup, mode toggling, opening, closing)
- Light-sensitive resistor
- 1 mF capacitor for light resistor analog input
