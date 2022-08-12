#!/usr/bin/env python3
# *********************************************************************
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54@gmail.com
# Date created: 1 Dec. 2020
# *********************************************************************
# About:
# Script for processing measurement data for Keeling Plot analysis
# *********************************************************************

import os 
import sys
import pickle
import numpy as np
import datetime as dt

def keeling_plot_data_processing(ch4_data):
  """
  Function for putting data into a regular array for Keeling Plots
  """
#   Load ICL dictionary with CH4 data
  with open(ch4_data, 'rb') as handle:
    ch4_dict = pickle.load(handle)
  
  time_icl=ch4_dict['time']
  ch4_icl=ch4_dict['ch4']
  ch4_stdev_icl=ch4_dict['ch4_stdev']
  d13ch4_icl=ch4_dict['d13ch4']
  d13ch4_stdev_icl=ch4_dict['d13ch4_stdev']  
  
#   Regular arrays for all ICL data
  time_array=[]
  ch4_array=np.zeros(78912)+np.nan
  ch4_stdev_array=np.zeros(78912)+np.nan
  d13ch4_array=np.zeros(78912)+np.nan
  d13ch4_stdev_array=np.zeros(78912)+np.nan
  
  for i in range(0, len(time_icl)-1):
    delta_day=(time_icl[i]- dt.datetime(2018,1,1,0,0)).days*72
    hour=3*time_icl[i].hour
    minute=time_icl[i].minute
    
    if minute<20:
      loc=delta_day+hour
      ch4_array[loc]=ch4_icl[i]
      ch4_stdev_array[loc]=ch4_stdev_icl[i]
      d13ch4_array[loc]=d13ch4_icl[i]
      d13ch4_stdev_array[loc]=d13ch4_stdev_icl[i]
      
    elif minute<40 and minute>=20:
      loc=delta_day+hour+1
      ch4_array[loc]=ch4_icl[i]
      ch4_stdev_array[loc]=ch4_stdev_icl[i]
      d13ch4_array[loc]=d13ch4_icl[i]
      d13ch4_stdev_array[loc]=d13ch4_stdev_icl[i]
      
    elif minute<60 and minute>=40:
      loc=delta_day+hour+2
      ch4_array[loc]=ch4_icl[i]
      ch4_stdev_array[loc]=ch4_stdev_icl[i]
      d13ch4_array[loc]=d13ch4_icl[i]
      d13ch4_stdev_array[loc]=d13ch4_stdev_icl[i]
                                 
    time_array.append(time_icl[i])
    
#     Filter data to retain values from 13:00-17:00
  ch4_day_array=np.zeros(78912)+np.nan
  ch4_day_stdev_array=np.zeros(78912)+np.nan
  d13ch4_day_array=np.zeros(78912)+np.nan
  d13ch4_day_stdev_array=np.zeros(78912)+np.nan
  
  for i in range(0, len(ch4_array), 72):
    for j in range(i+39, i+51):
      ch4_day_array[j]=ch4_array[j]
      ch4_day_stdev_array[j]=ch4_stdev_array[j]
      d13ch4_day_array[j]=d13ch4_array[j]
      d13ch4_day_stdev_array[j]=d13ch4_stdev_array[j]
  
  ordered_times = np.arange(dt.datetime(2018,1,1,0,0), dt.datetime(2021,1,1,0,0), dt.timedelta(minutes=20)).astype(dt.datetime)
  
  ch4_keelingplot_dict={}
  ch4_keelingplot_dict['time']=ordered_times
  ch4_keelingplot_dict['ch4']=ch4_array
  ch4_keelingplot_dict['ch4_stdev']=ch4_stdev_array
  ch4_keelingplot_dict['d13ch4']=d13ch4_array
  ch4_keelingplot_dict['d13ch4_stdev']=d13ch4_stdev_array
  ch4_keelingplot_dict['ch4_day']=ch4_day_array
  ch4_keelingplot_dict['ch4_day_stdev']=ch4_day_stdev_array
  ch4_keelingplot_dict['d13ch4_day']=d13ch4_day_array
  ch4_keelingplot_dict['d13ch4_day_stdev']=d13ch4_day_stdev_array
  
  return ch4_keelingplot_dict


def main():
  ch4_data_path="icl_ch4_met.pickle"
  ch4_keelingplot_dict=keeling_plot_data_processing(ch4_data_path)
  
  with open('icl_ch4_keelingplot_data.pickle', 'wb') as handle:
    pickle.dump(ch4_keelingplot_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
  main()
