#!/usr/bin/env python
"""
Settings file. 
This is imported as a module.
"""
from math import pi


moos_ip = '127.0.0.1'
moos_port = 9000
moos_name = 'CAN GUI'
moos_freq = 10.0
moos_vars = {               # name in MOOS
  'wheel_rpm_rear_left':    'Wheel_SpeedRL',
  'wheel_rpm_rear_right':   'Wheel_SpeedRR',
  'wheel_rpm_front_left':   'Wheel_SpeedFL',
  'wheel_rpm_front_right':  'Wheel_SpeedFR',
  'steer_position',         'SteerAngle',
}

gui_freq = 2.0
gui_dt = 1.0/gui_freq

# Vehicle parameters
wheel_diameter = 0.651
wheel_radius = wheel_diameter/2.0
wheel_circumference = wheel_diameter*pi
steer_ratio = 15.9*2.0




def steer_position_to_angle(a):
  """convert steer angle @ steering wheel reported over CAN to radians"""
  return a / steer_ratio

def wheel_rpm_to_speed(r):
  """convert rpm reported as the wheel speed to actual speed"""
  return r * wheel_circumference / 120.0


class VehicleData(object):
  wheel_speed_rear_left = float(0)
  wheel_speed_rear_right = float(0)
  wheel_speed_front_left = float(0)
  wheel_speed_front_right = float(0)
  steer_angle = float(0)
