#!/usr/bin/env python
from multiprocessing import Process
from time import sleep
from cfg import VehicleData
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
    plt.show()

  def _update(self):
    try:
      data = self.ifx.get_latest()
      # print '\nCanGui'
      # pprint(data)
      self.fig.clf()

      self.wheelspeed_ax = plt.subplot(121)
      # self.ax = self.fig.gca()
      self.wheelspeed_ax.axes.get_xaxis().set_visible(False)
      self.wheelspeed_ax.axes.get_yaxis().set_visible(False)
      # drivetrain picture
      plt.imshow(self.drivetrain_img, extent=cfg.gui_drivetrain_extent)
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
      
      self.steerangle_ax = plt.subplot(122)
      self.steerangle_ax.axes.get_xaxis().set_visible(False)
      self.steerangle_ax.axes.get_yaxis().set_visible(False)

      # steerwheel picture
      steerwheel_img_rot = ndimage.rotate(
                             self.steerwheel_img,
                             -data['steer_angle'],
                             reshape=False )
      plt.imshow(steerwheel_img_rot, extent=cfg.gui_steerwheel_extent, alpha=0.5)
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

