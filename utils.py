#!/usr/bin/env python3
# *********************************************************************
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54@gmail.com
# Date created: 12 Oct. 2018
# *********************************************************************
# About:
# Script that contains functions used across multiple scripts
# 
# *********************************************************************

import os 
import sys
import numpy as np

def nearest_ind(items, pivot):
  """ Finds nearest data value correpsonding to 20-min data
  """
  time_diff = np.abs([date - pivot for date in items])
  ind_min = time_diff.argmin(0)
  if time_diff[ind_min].total_seconds() < 1200:
    return [time_diff.argmin(0)]
  else:
    return []
