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


class CanGui(object):

  def __init__(self, ifx):
    self.ifx = ifx # comms interface
    plt.ion() # allow continuing after show() called
    self.drivetrain_img_path = os.path.join( \
                                 os.path.dirname(os.path.abspath(__file__)), \
                                 'img', 'drivetrain.png')
    self.drivetrain_img = mpimg.imread(self.drivetrain_img_path)
    self.fig, self.ax = plt.subplots()
    plt.show()

  def _update(self):
    print '\nCanGui'
    try:
      data = self.ifx.get_latest()
      pprint(data)
      self.fig.clf()
      self.ax = self.fig.gca()
      self.ax.axes.get_xaxis().set_visible(False)
      self.ax.axes.get_yaxis().set_visible(False)
      # drivetrain picture
      plt.imshow(self.drivetrain_img)
      # wheel speed text
      self.ax.text(cfg.gui_vel_rl_pos[0], cfg.gui_vel_rl_pos[1],
                   str(round(data['wheel_speed_rear_left'],1)) + '\n(m/s)',
                   horizontalalignment='left',
                   verticalalignment='bottom',
                   transform=self.ax.transAxes)
      self.ax.text(cfg.gui_vel_rr_pos[0], cfg.gui_vel_rr_pos[1],
                   str(round(data['wheel_speed_rear_right'],1)) + '\n(m/s)',
                   horizontalalignment='right',
                   verticalalignment='bottom',
                   transform=self.ax.transAxes)
      self.ax.text(cfg.gui_vel_fl_pos[0], cfg.gui_vel_fl_pos[1],
                   str(round(data['wheel_speed_front_left'],1)) + '\n(m/s)',
                   horizontalalignment='left',
                   verticalalignment='top',
                   transform=self.ax.transAxes)
      self.ax.text(cfg.gui_vel_fr_pos[0], cfg.gui_vel_fr_pos[1],
                   str(round(data['wheel_speed_front_right'],1)) + '\n(m/s)',
                   horizontalalignment='right',
                   verticalalignment='top',
                   transform=self.ax.transAxes)
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

