# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:44:28 2020

@author: Axel
"""

import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
import pvlib
from pvlib import solarposition
import datetime

def solar_Angles(time, freq, long, lat, alt, temp):
    '''
    A function to obtain the current solarposition for current time in series

    Parameters
    ----------
    time : Panda DateTimeIndex
        Must be date from Panda DateTimeIndex
    freq : String
        Example for a frequency of 5 minutes or 5 hours, '5min' or '5h' 
        respectively
    long : Float
        Longitude of location in decimal; West of Greenwhich is negative
    lat : Float
        Latitude of location in decimal; South of equator is negative
    alt : float
        Altitude of location [m]
    temp : float
        Average temperature of location [°C]

    Returns Dataframe with Zenith and Azimuth angle for each timestep of the 
    desired location
    
    References
    -------
    [1] William F. Holmgren, Clifford W. Hansen, and Mark A. Mikofski.
    “pvlib python: a python package for modeling solar energy systems.” 
    Journal of Open Source Software, 3(29), 884, (2018). 
    https://doi.org/10.21105/joss.00884

    '''

    solar_position = solarposition.get_solarposition(time,lat,long,alt, temperature = temp)
    
    
    
def irrad_tilt():
    cos_tilt = np.cos