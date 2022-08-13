#!/usr/bin/env python3
# *********************************************************************
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54@gmail.com
# *********************************************************************
# About:
# Script to look at the daily changes in CH4 and d13CH4 data between 
# the tank intervals. 
# *********************************************************************

import os
import sys
import numpy as np
import datetime as dt

def icl_tank_intervals(gcwerks_datapath, p_datapath):
  """ Find average CH4 in tank interval periods
  inputs:
      gcwerks_datapath (str): path to gcwerks space delimited datafile
      p_datapath (str): path to ICL pressure measurements
  
  """
#     Processing GCWerks 20-min output
  date, time, air_type =np.genfromtxt(gcwerks_datapath,
                                      unpack=True,
                                      usecols=(2,3,5),
                                      delimiter='',
                                      dtype=str,
                                      skip_header=2)
  d13ch4_c, d13ch4_c_stdev =np.genfromtxt(gcwerks_datapath,
                                          unpack=True,
                                          usecols=(11,14),
                                          delimiter='',
                                          skip_header=2) 
  _12ch4_c, _12ch4_c_stdev =np.genfromtxt(gcwerks_datapath,
                                          unpack=True,
                                          usecols=(21,24),
                                          delimiter='',
                                          skip_header=2)
  h2o =np.genfromtxt(gcwerks_datapath,
                     unpack=True,
                     usecols=(10),
                     delimiter='',
                     skip_header=2)
    
#     Correct d13ch4 values using Zazzeri formula (15/9/2020)
  d13ch4_dry =d13ch4_c/(-0.0109*h2o+1.0023)
  d13ch4_stdev_dry =d13ch4_c_stdev/(-0.0109*h2o+1.0023)
    
#     Carbon-13 standard values (Brandt et al. 2010)
  vpdb=0.0111802; vpdb_stdev=0.000016
    
#     Compute 13CH4 values
  _13ch4_c =vpdb*_12ch4_c*(1+d13ch4_dry*1e-3)
  _13ch4_c_stdev =vpdb_stdev*_12ch4_c_stdev*(1+d13ch4_stdev_dry*1e-3)
    
#     Find indices for different measurement tanks
  air_inds =[]
#     Standards from 15/1/2018 - 17/4/2019  
  D334212 =[]
  D334213 =[]
#     Standards from 17/4/2019 onwards
  D671527 =[]
  D671528 =[]

  for i in range(len(air_type)):
    if 'air' in air_type[i]:
      air_inds.append(i)
      
    elif 'D671527' in air_type[i]:
      D671527.append(i)
      
    elif 'D671528' in air_type[i]:
      D671528.append(i)
      
    elif 'D334212' in air_type[i]:
      D334212.append(i)
      
    elif 'D334213' in air_type[i]:
      D334213.append(i)
  
#   Samples of atmospheric CH4
  time_sample =[]
  ch4_c, ch4_stdev, d13ch4_c, d13ch4_stdev =[], [], [], []
  for i in air_inds:
    ch4_c.append(_12ch4_c[i] +_13ch4_c[i])
    ch4_stdev.append(np.sqrt(_12ch4_c_stdev[i]**2 +_13ch4_c_stdev[i]**2))
    d13ch4_c.append(d13ch4_dry[i])
    d13ch4_stdev.append(d13ch4_stdev_dry[i])
    t_hold =date[i]+' '+time[i]
    time_sample.append(dt.datetime.strptime(t_hold, "%y%m%d %H%M"))

#   Standards
  time_D671527, time_D671528 = [], []
  for i in D671527:
    t_hold =date[i]+' '+time[i]
    time_D671527.append(dt.datetime.strptime(t_hold, "%y%m%d %H%M"))   
  for i in D671528:
    t_hold =date[i]+' '+time[i]
    time_D671528.append(dt.datetime.strptime(t_hold, "%y%m%d %H%M"))
    
# 20-minute spaced arrays
  ch4_array =np.zeros(78912)+np.nan
  d13ch4_array =np.zeros(78912)+np.nan
  ch4_stdev_array =np.zeros(78912)+np.nan
  d13ch4_stdev_array =np.zeros(78912)+np.nan
  time_D671527_array =np.zeros(78912)+np.nan
  time_D671528_array =np.zeros(78912)+np.nan


Pressure_array   = np.zeros(78912)+np.nan
    
