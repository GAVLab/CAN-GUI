#!/usr/bin/env python
from multiprocessing import Process
from time import sleep
from cfg import VehicleData, steer_position_to_tire_angle
import cfg
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.cm import hsv
import matplotlib.image as mpimg
from pprint import pprint
import numpy as np
import os
from scipy import ndimage
from math import sin, cos


class CanGui(object):

  def __init__(self, ifx):
    self.ifx = ifx # comms interface
    plt.ion() # allow continuing after show() called
    drivetrain_img_path = os.path.join( \
                            os.path.dirname(os.path.abspath(__file__)), \
                            'img', 'drivetrain.png')
    steerwheel_img_path = os.path.join( \
                            os.path.dirname(os.path.abspath(__file__)), \
                            'img', 'steeringwheel_arrow.png')
    self.drivetrain_img = mpimg.imread(drivetrain_img_path)
    self.fig, _ = plt.subplots()
    self.fig.set_facecolor('w')
    self.steerwheel_img = ndimage.imread(steerwheel_img_path)
    plt.get_current_fig_manager().resize(1500,750)
    plt.show()

  def _update(self):
    try:
      data = self.ifx.get_latest()
      # print '\nCanGui'
      # pprint(data)
      self.fig.clf()

      # wheelspeed bar graph
      self.wheelbar_ax = plt.subplot(131)
      # self.wheelbar_ax.axes.get_xaxis().set_visible(False)
      # self.wheelbar_ax.axes.get_yaxis().set_visible(False)
      veldat = [
        data['wheel_speed_rear_left'],
        data['wheel_speed_front_left'],
        data['wheel_speed_front_right'],
        data['wheel_speed_rear_right']]
      hbar = plt.bar(np.arange(4),veldat)
      # self.wheelbar_ax.set_xticklabels(cfg.gui_vel_bar_names)
      xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in hbar]
      plt.xticks(xticks_pos, cfg.gui_vel_bar_names, ha='center')
      plt.ylabel('Wheel Speed (m/s)')

      self.wheelspeed_ax = plt.subplot(132)
      # self.ax = self.fig.gca()
      self.wheelspeed_ax.axes.get_xaxis().set_visible(False)
      self.wheelspeed_ax.axes.get_yaxis().set_visible(False)
      # drivetrain picture
      plt.imshow(self.drivetrain_img)
      # wheel speed text
      self.wheelspeed_ax.text(cfg.gui_vel_rl_pos[0], cfg.gui_vel_rl_pos[1],
                   str(round(data['wheel_speed_rear_left'],1)) + '\n(m/s)',
                   horizontalalignment='left',
                   verticalalignment='bottom',
                   transform=self.wheelspeed_ax.transAxes)
      self.wheelspeed_ax.text(cfg.gui_vel_rr_pos[0], cfg.gui_vel_rr_pos[1],
                   str(round(data['wheel_speed_rear_right'],1)) + '\n(m/s)',
                   horizontalalignment='right',
                   verticalalignment='bottom',
                   transform=self.wheelspeed_ax.transAxes)
      self.wheelspeed_ax.text(cfg.gui_vel_fl_pos[0], cfg.gui_vel_fl_pos[1],
                   str(round(data['wheel_speed_front_left'],1)) + '\n(m/s)',
                   horizontalalignment='left',
                   verticalalignment='top',
                   transform=self.wheelspeed_ax.transAxes)
      self.wheelspeed_ax.text(cfg.gui_vel_fr_pos[0], cfg.gui_vel_fr_pos[1],
                   str(round(data['wheel_speed_front_right'],1)) + '\n(m/s)',
                   horizontalalignment='right',
                   verticalalignment='top',
                   transform=self.wheelspeed_ax.transAxes)
      # tire_angle_deg = steer_position_to_tire_angle(-data['steer_angle'])
      # bbox = self.wheelspeed_ax.get_window_extent().transformed(
      #          self.fig.dpi_scale_trans.inverted())
      # width, height = bbox.width, bbox.height
      # width *= self.fig.dpi
      # height *= self.fig.dpi
      # to_coord =   [width/2.0  - cfg.gui_tire_angle_length*sin(tire_angle_deg)/2.0, \
      #               height/2.0 - cfg.gui_tire_angle_length*cos(tire_angle_deg)/2.0]
      # from_coord = [width/2.0  + cfg.gui_tire_angle_length*sin(tire_angle_deg)/2.0, \
      #               height/2.0 + cfg.gui_tire_angle_length*cos(tire_angle_deg)/2.0]
      # print 'from'
      # print from_coord
      # print 'to'
      # print to_coord
      # print '\n'
      # self.wheelspeed_ax.annotate("",
      #                             xy=to_coord, xycoords='data', xytext=from_coord,
      #                             size=20, ha='center',
      #                             arrowprops=dict(arrowstyle="simple",connectionstyle="arc3,rad=0"))
      

      # steerwheel picture
      self.steerangle_ax = plt.subplot(133)
      self.steerangle_ax.axes.get_xaxis().set_visible(False)
      self.steerangle_ax.axes.get_yaxis().set_visible(False)
      steerwheel_img_rot = ndimage.rotate(
                             self.steerwheel_img,
                             -data['steer_angle'],
                             reshape=False )
      plt.imshow(steerwheel_img_rot)
      # plt.imshow(self.steerwheel_img, cmap=plt.cm.gray, extent=cfg.gui_steerwheel_extent)

      plt.draw()
      plt.show()
    except Exception, e:
      print e
      self.ifx.exit()
      sys.exit()
  
  def run(self):
    while True:
      self._update()
      sleep(1.0/cfg.gui_freq)

