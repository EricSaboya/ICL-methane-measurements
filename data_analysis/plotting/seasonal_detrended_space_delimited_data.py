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

import sys
import pickle
import numpy as np 
import datetime as dt 

from scipy.stats import linregress

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib import dates as dates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.lines import Line2D

mpl.rcParams['axes.linewidth'] = 0.8
plt.rc('font', family='serif', size=12, weight='light')
plt.rcParams['text.usetex']=True



def processing_icl_measurements(gcwerks_datapath):
    """ Processing GCWerks output 
    inputs:
        gcwerks_datapath (str): path to space-delimited GCWerks 20-min ave file
        met_datapath (str): path to comma-delimited met data
    
    returns:
        co2 dict (dict): contains: 
            - CO2, d13CO2 values and stdev 
    """
#     Processing GCWerks 20-min output
    date, time, air_type=np.genfromtxt(gcwerks_datapath,
                                       unpack=True,
                                       usecols=(2,3,5),
                                       delimiter='',
                                       dtype=str,
                                       skip_header=2)
    d13co2_c, d13co2_c_stdev=np.genfromtxt(gcwerks_datapath,
                                           unpack=True,
                                           usecols=(16,19),
                                           delimiter='',
                                           skip_header=2)
    _12co2_c, _12co2_c_stdev=np.genfromtxt(gcwerks_datapath,
                                           unpack=True,
                                           usecols=(26,29),
                                           delimiter='',
                                           skip_header=2)
    h2o=np.genfromtxt(gcwerks_datapath,
                      unpack=True,
                      usecols=(10),
                      delimiter='',
                      skip_header=2)
    
#     Correct d13ch4 values using Zazzeri formula (15/9/2020)
# 	  Don't think CO2 data need correction for water 
    d13co2_dry=d13co2_c#/(-0.0109*h2o+1.0023)
    d13co2_stdev_dry=d13co2_c_stdev#/(-0.0109*h2o+1.0023)
    
#     Carbon-13 standard values (Brandt et al. 2010)
    vpdb=0.0111802; vpdb_stdev=0.000016
    
#     Compute 13CH4 values
    _13co2_c=vpdb*_12co2_c*(1+d13co2_dry*1e-3)
    _13co2_c_stdev=vpdb_stdev*_12co2_c_stdev*(1+d13co2_stdev_dry*1e-3)
    
#     Retain indices that are 'air' samples 
    inds_air=[]
    for i in range(len(air_type)):
        if 'air' in air_type[i]:
            inds_air.append(i)
            
#     Filter data to retain measurements that sampled outdoor air
    co2, t, d13co2, co2_stdev, d13co2_stdev = [],[],[],[],[]
    for i in inds_air:
        co2.append(_12co2_c[i]+_13co2_c[i])
        co2_stdev.append(np.sqrt(_12co2_c_stdev[i]**2 + _13co2_c_stdev[i]**2))
        d13co2.append(d13co2_dry[i])
        d13co2_stdev.append(d13co2_stdev_dry[i])
        t_load = date[i]+' '+time[i]
        t.append(dt.datetime.strptime(t_load, "%y%m%d %H%M"))
            
#     Save data to dict.
#     Data on MPI-BGC scale 
    co2_dict={}
    co2_dict['time']=np.array(t)
    co2_dict['co2']=np.array(co2)
    co2_dict['co2_stdev']=np.array(co2_stdev)
    co2_dict['d13co2']=np.array(d13co2)
    co2_dict['d13co2_stdev']=np.array(d13co2_stdev)

    return co2_dict
  
def separate_data_monthly(times, co2_c):
	""" function to aggregate data into months by year 
	Function works for 2018-2021 inclusive

	"""
	jan18, feb18, mar18, apr18 = [], [], [], []
	may18, jun18, jul18, aug18 = [], [], [], []
	sep18, oct18, nov18, dec18 = [], [], [], []

	jan19, feb19, mar19, apr19 = [], [], [], []
	may19, jun19, jul19, aug19 = [], [], [], []
	sep19, oct19, nov19, dec19 = [], [], [], []

	jan20, feb20, mar20, apr20 = [], [], [], []
	may20, jun20, jul20, aug20 = [], [], [], []
	sep20, oct20, nov20, dec20 = [], [], [], []

	jan21, feb21, mar21, apr21 = [], [], [], []
	may21, jun21, jul21, aug21 = [], [], [], []
	sep21, oct21, nov21, dec21 = [], [], [], []


	for i in range(len(times)):

		if times[i].year==2018 and times[i].month==1:
			jan18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==2:
			feb18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==3:
			mar18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==4:
			apr18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==5:
			may18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==6:
			jun18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==7:
			jul18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==8:
			aug18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==9:
			sep18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==10:
			oct18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==11:
			nov18.append(co2_c[i])
		elif times[i].year==2018 and times[i].month==12:
			dec18.append(co2_c[i])


		elif times[i].year==2019 and times[i].month==1:
			jan19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==2:
			feb19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==3:
			mar19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==4:
			apr19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==5:
			may19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==6:
			jun19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==7:
			jul19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==8:
			aug19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==9:
			sep19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==10:
			oct19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==11:
			nov19.append(co2_c[i])
		elif times[i].year==2019 and times[i].month==12:
			dec19.append(co2_c[i])

		elif times[i].year==2020 and times[i].month==1:
			jan20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==2:
			feb20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==3:
			mar20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==4:
			apr20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==5:
			may20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==6:
			jun20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==7:
			jul20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==8:
			aug20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==9:
			sep20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==10:
			oct20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==11:
			nov20.append(co2_c[i])
		elif times[i].year==2020 and times[i].month==12:
			dec20.append(co2_c[i])


		elif times[i].year==2021 and times[i].month==1:
			jan21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==2:
			feb21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==3:
			mar21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==4:
			apr21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==5:
			may21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==6:
			jun21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==7:
			jul21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==8:
			aug21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==9:
			sep21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==10:
			oct21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==11:
			nov21.append(co2_c[i])
		elif times[i].year==2021 and times[i].month==12:
			dec21.append(co2_c[i])


	t_monthly = [
	dt.datetime(2018,1,1), dt.datetime(2018,2,1), dt.datetime(2018,3,1), dt.datetime(2018,4,1),
	dt.datetime(2018,5,1), dt.datetime(2018,6,1), dt.datetime(2018,7,1), dt.datetime(2018,8,1),
	dt.datetime(2018,9,1), dt.datetime(2018,10,1), dt.datetime(2018,11,1), dt.datetime(2018,12,1),
	dt.datetime(2019,1,1), dt.datetime(2019,2,1), dt.datetime(2019,3,1), dt.datetime(2019,4,1),
	dt.datetime(2019,5,1), dt.datetime(2019,6,1), dt.datetime(2019,7,1), dt.datetime(2019,8,1),
	dt.datetime(2019,9,1), dt.datetime(2019,10,1), dt.datetime(2019,11,1), dt.datetime(2019,12,1),
	dt.datetime(2020,1,1), dt.datetime(2020,2,1), dt.datetime(2020,3,1), dt.datetime(2020,4,1),
	dt.datetime(2020,5,1), dt.datetime(2020,6,1), dt.datetime(2020,7,1), dt.datetime(2020,8,1),
	dt.datetime(2020,9,1), dt.datetime(2020,10,1), dt.datetime(2020,11,1), dt.datetime(2020,12,1),
	dt.datetime(2021,1,1), dt.datetime(2021,2,1), dt.datetime(2021,3,1), dt.datetime(2021,4,1),
	dt.datetime(2021,5,1), dt.datetime(2021,6,1), dt.datetime(2021,7,1), dt.datetime(2021,8,1),
	dt.datetime(2021,9,1), dt.datetime(2021,10,1), dt.datetime(2021,11,1), dt.datetime(2021,12,1)
	]

	output = [
	np.array(jan18), np.array(feb18), np.array(mar18), np.array(apr18),
	np.array(may18), np.array(jun18), np.array(jul18), np.array(aug18),
	np.array(sep18), np.array(oct18), np.array(nov18), np.array(dec18),
	np.array(jan19), np.array(feb19), np.array(mar19), np.array(apr19),
	np.array(may19), np.array(jun19), np.array(jul19), np.array(aug19),
	np.array(sep19), np.array(oct19), np.array(nov19), np.array(dec19),
	np.array(jan20), np.array(feb20), np.array(mar20), np.array(apr20),
	np.array(may20), np.array(jun20), np.array(jul20), np.array(aug20),
	np.array(sep20), np.array(oct20), np.array(nov20), np.array(dec20),
	np.array(jan21), np.array(feb21), np.array(mar21), np.array(apr21),
	np.array(may21), np.array(jun21), np.array(jul21), np.array(aug21),
	np.array(sep21), np.array(oct21), np.array(nov21), np.array(dec21)
		]

	return t_monthly, output 

def extract_afternoon_data(times, co2_c, d13co2_c):
	"""
	keep data for afternoon times: 13:00-17:00
	"""
	times_pm = []
	co2_c_pm = []
	d13co2_c_pm = []

	for i in range(len(times)):
		if times[i].hour>=13 and times[i].hour<=17:
			times_pm.append(times[i])
			co2_c_pm.append(co2_c[i])
			d13co2_c_pm.append(d13co2_c[i])

	co2_pm_dict={}
	co2_pm_dict['time']=np.array(times_pm)
	co2_pm_dict['co2']=np.array(co2_c_pm)
	co2_pm_dict['d13co2']=np.array(d13co2_c_pm)

	return co2_pm_dict


def plot_monthly_boxplots(time, co2_c, ylabel, savefile):
	fig, ax = plt.subplots(figsize=(10,6))

	for i in range(0,12):
		mask0 = ~np.isnan(co2_c[0+i])
		mask1 = ~np.isnan(co2_c[12+i])
		mask2 = ~np.isnan(co2_c[24+i])
		mask3 = ~np.isnan(co2_c[36+i])

		if len(co2_c[0+i][mask0]) > 3:
			a0_18=ax.boxplot(co2_c[0+i][mask0], showcaps=True, showbox=True, showfliers=False, medianprops=dict(color='#000000'), positions=[0.7+i], vert=True, whis=[0,100], patch_artist=True)
			for patch, color in zip(a0_18['boxes'], 'c'): patch.set_facecolor(color)

		if len(co2_c[12+i][mask1]) > 3:
			a0_19=ax.boxplot(co2_c[12+i][mask1], showcaps=True, showbox=True, showfliers=False, medianprops=dict(color='#000000'), positions=[0.9+i], vert=True, whis=[0,100], patch_artist=True)
			for patch, color in zip(a0_19['boxes'], 'r'): patch.set_facecolor(color)

		if len(co2_c[24+i][mask2]) > 3:
			a0_20=ax.boxplot(co2_c[24+i][mask2], showcaps=True, showbox=True, showfliers=False, medianprops=dict(color='#000000'), positions=[1.1+i], vert=True, whis=[0,100], patch_artist=True)
			for patch, color in zip(a0_20['boxes'], 'y'): patch.set_facecolor(color)

		if len(co2_c[36+i][mask3]) > 3:
			if i < 11:
				a0_21=ax.boxplot(co2_c[36+i][mask3], showcaps=True, showbox=True, showfliers=False, medianprops=dict(color='#000000'), positions=[1.3+i], vert=True, whis=[0,100], patch_artist=True)
				for patch, color in zip(a0_21['boxes'], 'b'): patch.set_facecolor(color)

	ax.set_xlim((0.35, 12.5))
	ax.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
	ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
	# ax.set_yticks([1900, 2000, 2100, 2200, 2300, 2400, 2500])
	# ax.set_ylim((1890, 2500))

	# colors = ['black', 'blue', 'magenta']
	# lines = [Line2D([0], [0], color=c, linewidth=3, linestyle='-') for c in colors]

	ax.legend([a0_18["boxes"][0], a0_19["boxes"][0], a0_20["boxes"][0], a0_21["boxes"][0],], ['ICL 2018', 'ICL 2019', 'ICL 2020',  'ICL 2021'], loc='upper right', ncol=2, fontsize=9, markerscale=0.5)

	ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
	ax.yaxis.set_ticks_position('both')
	ax.set_ylabel(ylabel,fontsize=14)
	ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
	ax.xaxis.set_ticks_position('both')

	ax.tick_params(which='major', direction='in')
	ax.tick_params(which='minor', direction='in')

	# plt.show(); plt.close()
	plt.savefig(savefile, bbox_inches='tight', dpi=300); plt.close()




def main():
	# Process CO2 data from gcwerks 20-min output 
	gcwerks_datapath="//Volumes/LaCie/data/measurements/ICL/full_record.txt"
	co2_dict = processing_icl_measurements(gcwerks_datapath)
	t_co2, co2_c, d13co2_c = co2_dict['time'], co2_dict['co2'], co2_dict['d13co2']

	# Extract afternoon data
	co2_pm_dict = extract_afternoon_data(t_co2, co2_c, d13co2_c)
	t_pm_co2, co2_pm_c, d13co2_pm_c = co2_pm_dict['time'], co2_pm_dict['co2'], co2_pm_dict['d13co2']

	# Detrend afternoon data using March 2018 as t0
	t_icl_linregress = np.linspace(0, len(co2_pm_c[535::])-1, len(co2_pm_c[535::]))
	
	co2_pm_icl = co2_pm_c[535::]
	d13co2_pm_icl = d13co2_pm_c[535::]

	mask_icl = ~np.isnan(co2_pm_icl)
	out_icl = linregress(t_icl_linregress[mask_icl], co2_pm_icl[mask_icl])
	detrended_co2_pm = co2_pm_icl - t_icl_linregress*out_icl[0] 

	out_d13c_icl = linregress(t_icl_linregress[mask_icl], d13co2_pm_icl[mask_icl])
	detrended_d13co2_pm = d13co2_pm_icl - t_icl_linregress*out_d13c_icl[0] 

	# get monthly data
	t_monthly, monthly_co2 = separate_data_monthly(t_pm_co2[535::], detrended_co2_pm)
	t_monthly, monthly_d13co2 = separate_data_monthly(t_pm_co2[535::], detrended_d13co2_pm)

	# Plot 
	plot_monthly_boxplots(t_monthly, monthly_co2, ylabel=r'CO$_2$ mixing ratio (ppm)', savefile="//Volumes/LaCie/ICL_CO2/Scripts/co2_2018_2021.png")

	plot_monthly_boxplots(t_monthly, monthly_d13co2, ylabel=r'$\delta^{13}$CO$_2$ (‰)', savefile="//Volumes/LaCie/ICL_CO2/Scripts/d13co2_2018_2021.png")



main()










