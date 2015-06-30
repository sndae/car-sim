car-sim is a simple 2D car simulator written in java. It provides a interface which can be used to read sensor data and to control the car. This interface can either be implemented in java, or python using jython.

It simulates a z-axis gyro, speed and steering sensor, gps and a camera that looking at the ground. All the simulated sensors can be configured to have an error.
The car itself can be configured aswell. For steering and speed, a first oder lag (PT1) and a normal distributed error can be simulated.

This program was written to help learn about automated cars, to help visualize and learn about localization algorithms as it is taught at udacity.