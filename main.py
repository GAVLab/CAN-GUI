#!/usr/bin/env python
from gui import CanGui
from interface import MOOSInterface

if __name__ == '__main__':
  gui = CanGui(MOOSInterface())
  gui.run()