#!/usr/bin/env python3
# *********************************************************************
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54@gmail.com
# Date created: 1 Dec. 2020
# *********************************************************************
# About:
# Script for processing: 
# - 20-min averaged GCWerks Imperial College London measurements
# - 5-min averaged meteorological data at Imperial College London
# 
# *********************************************************************

import os 
import sys
import pickle
import numpy as np 
import datetime as dt

sys.path.append('//')
import utils

def processing_icl_measurements(gcwerks_datapath, met_datapath):
    """ Processing GCWerks and ClimeMet output
    inputs:
        gcwerks_datapath (str): path to space-delimited GCWerks 20-min ave file
        met_datapath (str): path to comma-delimited met data
    
    returns:
        ch4_dict (dict): contains: 
            - CH4, d13CH4 values and stdev 
            - wind speed and direction
    """
#     Processing GCWerks 20-min output
    date, time, air_type=np.genfromtxt(gcwerks_datapath,
                                       unpack=True,
                                       usecols=(2,3,5),
                                       delimiter='',
                                       dtype=str,
                                       skip_header=2)
    d13ch4_c, d13ch4_c_stdev=np.genfromtxt(gcwerks_datapath,
                                           unpack=True,
                                           usecols=(11,14),
                                           delimiter='',
                                           skip_header=2)
    _12ch4_c, _12ch4_c_stdev=np.genfromtxt(gcwerks_datapath,
                                           unpack=True,
                                           usecols=(21,24),
                                           delimiter='',
                                           skip_header=2)
    h2o=np.genfromtxt(gcwerks_datapath,
                      unpack=True,
                      usecols=(10),
                      delimiter='',
                      skip_header=2)
    
#     Correct d13ch4 values using Zazzeri formula (15/9/2020)
    d13ch4_dry=d13ch4_c/(-0.0109*h2o+1.0023)
    d13ch4_stdev_dry=d13ch4_c_stdev/(-0.0109*h2o+1.0023)
    
#     Carbon-13 standard values (Brandt et al. 2010)
    vpdb=0.0111802; vpdb_stdev=0.000016
    
#     Compute 13CH4 values
    _13ch4_c=vpdb*_12ch4_c*(1+d13ch4_dry*1e-3)
    _13ch4_c_stdev=vpdb_stdev*_12ch4_c_stdev*(1+d13ch4_stdev_dry*1e-3)
    
#     Retain indices that are 'air' samples 
    inds_air=[]
    for i in range(len(air_type)):
        if 'air' in air_type[i]:
            inds_air.append(i)
            
#     Filter data to retain measurements that sampled outdoor air
    ch4, t, d13ch4, ch4_stdev, d13ch4_stdev = [],[],[],[],[]
    for i in inds_air:
        ch4.append(_12ch4_c[i]+_13ch4_c[i])
        ch4_stdev.append(np.sqrt(_12ch4_c_stdev[i]**2 + _13ch4_c_stdev[i]**2))
        d13ch4.append(d13ch4_dry[i])
        d13ch4_stdev.append(d13ch4_stdev_dry[i])
        t_load = date[i]+' '+time[i]
        t.append(dt.datetime.strptime(t_load, "%y%m%d %H%M"))
            
#     Save data to dict.
    ch4_dict={}
    ch4_dict['time']=np.array(t)
    ch4_dict['ch4']=np.array(ch4)*1.00028
    ch4_dict['ch4_stdev']=np.array(ch4_stdev)*1.00028
    ch4_dict['d13ch4']=np.array(d13ch4)*1.00028
    ch4_dict['d13ch4_stdev']=np.array(d13ch4_stdev)*1.00028
  

#     Processing met data
    t_met = np.genfromtxt(met_datapath, 
                          unpack=True, 
                          usecols=(0), 
                          delimiter=',', 
                          dtype=str, 
                          skip_header=1)
    t_met_stamp = []
    for i in range(len(t_met)):
        t_met_stamp.append(dt.datetime.strptime(t_met[i], "%Y-%m-%d %H:%M:%S"))
    
    wind_direction, wind_speed=np.genfromtxt(met_datapath,
                                             unpack=True,
                                             usecols=(10,8),
                                             delimiter=',',
                                             skip_header=1)

    wind_speed_20m, wind_direction_20m=[],[]
    for i in range(len(t)):
        ch4_date = t[i]
        met_ind=utils.nearest_ind(t_met_stamp,ch4_date)
        if len(met_ind)==0:
            wind_speed_20m.append(np.nan)
            wind_direction_20m.append(np.nan)
        else:
            wind_speed_20m.append(wind_speed[met_ind[0]])
            wind_direction_20m.append(wind_direction[met_ind[0]])
   
#     Add met data to ch4_dict
    ch4_dict['wind_speed']=np.array(wind_speed_20m)
    ch4_dict['wind_direction']=np.array(wind_direction_20m)
    
    return ch4_dict
    
            
def main():
#     Data paths
    picarro_data="//Volumes/HardDrive/PhD/disk1/data/Picarro/IMP_26magl/GCwerks/20min_record.txt"
    met_data="//Volumes/LaCie/CHAPTER1/Data/Observations/ICL_MET/RAW_COMPLETE.txt"
#     Create dictionary
    ch4_dict=processing_icl_measurements(picarro_data, met_data)
#     Save dictionary
    with open('icl_ch4_met.pickle','wb') as handle:
        pickle.dump(ch4_dict, handle,protocol=pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
    main()
