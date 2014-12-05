#!/usr/bin/env python
from math import pi, degrees
from pprint import pprint

################################################################################
### Settings
################################################################################

is_live = False

# MOOS Settings
moos_ip = '127.0.0.1'
moos_port = 9000
moos_name = 'CAN GUI'
moos_freq = 20.0
moos_vars = {               # name in MOOS
  'wheel_rpm_rear_left':    'Wheel_SpeedRL',
  'wheel_rpm_rear_right':   'Wheel_SpeedRR',
  'wheel_rpm_front_left':   'Wheel_SpeedFL',
  'wheel_rpm_front_right':  'Wheel_SpeedFR',
  'steer_position':        'SteerAngle',
}

# GUI settings
gui_freq = 10.0
gui_dt = 1.0/gui_freq
gui_left = .05
gui_width = .9
gui_bottom = .05
gui_height = .9
gui_right = gui_left + gui_width
gui_top = gui_bottom + gui_height
# vel text
gui_vel_text_vert_offset = .05
gui_vel_text_horiz_offset = .001
gui_vel_rl_pos = ( gui_left   + gui_vel_text_horiz_offset ,
                   gui_bottom + gui_vel_text_vert_offset  )
gui_vel_rr_pos = ( gui_right  - gui_vel_text_horiz_offset , 
                   gui_bottom + gui_vel_text_vert_offset  )
gui_vel_fl_pos = ( gui_left   + gui_vel_text_horiz_offset , 
                   gui_top    - gui_vel_text_vert_offset  )
gui_vel_fr_pos = ( gui_right  - gui_vel_text_horiz_offset , 
                   gui_top    - gui_vel_text_vert_offset  )
gui_vel_max = 35.0
# drivetrain image
gui_drivetrain_ratio = [3.0, 4.0]
gui_drivetrain_size = [.6] # width height (3:4 ratio)\
gui_drivetrain_size.append(gui_drivetrain_size[0] * gui_drivetrain_ratio[1]/gui_drivetrain_ratio[0])
gui_drivetrain_pos = [.5, .5] # horiz vert
gui_drivetrain_extent = [
  gui_drivetrain_pos[0] - gui_drivetrain_size[0]/2.0, # horiz min
  gui_drivetrain_pos[0] + gui_drivetrain_size[0]/2.0, # horiz max
  gui_drivetrain_pos[1] - gui_drivetrain_size[1]/2.0, # vert min
  gui_drivetrain_pos[1] + gui_drivetrain_size[1]/2.0, # vert max
  ]
print 'GUI Drivetrain Extent: ', pprint(gui_drivetrain_extent)
# steer angle
# gui_steerwheel_range = 270.0
gui_steerwheel_size = [.1, .1]
gui_steerwheel_horiz_offset = 2
gui_steerwheel_extent = [
  0.5 + gui_steerwheel_horiz_offset,
  0.5 + gui_steerwheel_horiz_offset + gui_steerwheel_size[0],
  0.5 - gui_steerwheel_size[1]/2.0,
  0.5 + gui_steerwheel_size[1]/2.0,
  ]
print 'GUI SteeringWheel Extent: ', pprint(gui_steerwheel_extent)
# Vehicle parameters
wheel_diameter = 0.651
wheel_radius = wheel_diameter/2.0
wheel_circumference = wheel_diameter*pi
steer_ratio = 15.9*2.0

################################################################################
### Utility Functions
################################################################################

def steer_position_to_angle(a):
  """convert steer angle @ steering wheel reported over CAN to radians"""
  return degrees(a/steer_ratio)

def wheel_rpm_to_speed(r):
  """convert rpm reported as the wheel speed to actual speed"""
  return r * wheel_circumference / 120.0

################################################################################
### Data Structures
################################################################################

VehicleData = {
  'wheel_speed_rear_left':    float(0),
  'wheel_speed_rear_right':   float(0),
  'wheel_speed_front_left':   float(0),
  'wheel_speed_front_right':  float(0),
  'steer_angle':              float(0),
}
