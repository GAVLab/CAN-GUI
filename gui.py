#!/usr/bin/env python
from cfg import VehicleData


class CanGui(object):

  def __init__(self, ifx):
    self.ifx = ifx
    self.data = VehicleData()
    

  def _update(self):
    self.data = self.ifx.get_latest()