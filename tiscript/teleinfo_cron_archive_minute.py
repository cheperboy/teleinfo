#!/usr/bin/env python
# -*- coding: utf-8 -*-

BASE = "/home/pi/currentlog/"
import datetime
import sys
import os
sys.path.append(os.path.join(BASE,'website/app'))

from models import *
from teleinfo_model import *
import teleinfo_minute_model as TeleinfoMinute

print TeleinfoMinute.process_archive_minute()
