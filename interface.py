#!/usr/bin/env python
import sys
from time import sleep
from pprint import pprint
from pymoos.MOOSCommClient import MOOSCommClient
from copy import deepcopy
import cfg
from cfg import VehicleData
from cfg import steer_position_to_angle, wheel_rpm_to_speed



class MOOSInterface(MOOSCommClient):

  def __init__(self):
    self.data = deepcopy(VehicleData)
    MOOSCommClient.__init__(self)
    self.SetOnConnectCallBack(self._on_connect)
    self.SetOnDisconnectCallBack(self._on_disconnect)
    self.SetOnMailCallBack(self._on_mail)
    self.Run(cfg.moos_ip, cfg.moos_port, cfg.moos_name, cfg.moos_freq)
    for x in range(30):
      if not self.IsConnected():
        sleep(0.1)
        continue
      print('CAN GUI Connected')
      return
    print('CAN GUI Could not connect to MOOSDB')
    sys.exit()

  def _on_connect(self):
    for key in cfg.moos_vars:
      self.Register(cfg.moos_vars[key])

  def _on_disconnect(self):
    print('CAN GUI Disconnected')
    sys.exit()

  def _on_mail(self):
    for msg in self.FetchRecentMail():
      if cfg.is_live:
        val = float(msg.GetString())
      else:
        val = msg.GetDouble()
      # figure out the key as defined in cfg.moos_vars
      key = [k for k,v in cfg.moos_vars.iteritems() if v == msg.GetKey()]
      if len(key):
        key = key[0]
      else:
        continue
      # print 'key: ' + key + '  val: ' + str(msg.GetDouble())
      if 'wheel_rpm' in key:
        speed = wheel_rpm_to_speed(val)
        data_key = 'wheel_speed_'+'_'.join(key.split('_')[2:])
        self.data[data_key] = speed
      elif key == 'steer_position':
        self.data['steer_angle'] = steer_position_to_angle(val)
    # print '\nMOOSInterface'
    # pprint(self.data)

  def get_latest(self):
    return deepcopy(self.data)

  def exit(self):
    self.Close()
    sys.exit()