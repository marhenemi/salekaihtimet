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

# Personal evaluation on finnish line
The project was successful, and it provided us with valuable learning experiences in coding practices, Git usage, and teamwork. Reflecting on the codebase, I (linre-90) have several suggestions for improvement:
- Utilizing more classes to encapsulate individual data types, allowing for the passing of a single class object to functions instead of multiple parameters.
- Encapsulating global variables within classes, where initialization functions return the state or handle to the module, which is a pointer to a class instance.
- Implementing better naming conventions for variables and functions to enhance readability, including tying function names to their respective modules.
- Rewriting unit tests to ensure comprehensive coverage and accuracy.
- Addressing memory usage optimizations to enhance efficiency.
