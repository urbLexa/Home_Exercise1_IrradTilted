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

   
def irrad_tilt(time, lat, long, panel_elev, panel_az, irrad, alb, 
               alt=None, pressure=None, temp=None):
    '''
    Function to calculate the solar irradiance on arbitrary tited surface/
    PV panel and a arbitrary location at any given time.
    In order to obtain the solar position [1] is used and angle calculations
    are done according to [2]

    Parameters
    ----------
    time : Panda DateTimeIndex
        Must be date from Panda DateTimeIndex --> date and time to be assessed.
    lat : float
        Latitude of location in decimal; South of equator is negative.
    long : float
        Longitude of location in decimal; West of Greenwhich is negative.
    panel_elev : float
        Elevation angle of the PV panel surface (0-90, while 0 is horizontal) 
        in °.
    panel_az : float
        Azimuth angle of the PV panel surface (0-359, while 0 is north, 90 is
        east, 180 is south and 270 is west) in °.
    irrad : panda Dataframe
        Dataframe with panda DateTimeIndex, global horizontal irradiance
        ('G(h)'), direct normal irradiance ('Gb(n)') and diffuse horizontal
        irradiance ('Gd(h)') --> it is important that the collumns are named
        respectively.
    alb : float
        Albedo; Surface dependent reflection coefficient --> consult 
        https://de.wikipedia.org/wiki/Albedo for values.
    alt : float or None, optional
        Altitude of location above sea level m. The default is None.
    pressure : float or None, optional
        In Pa The default is None.
    temp : float or None, optional
        Average temperature in °C of location. The default is None.

    Returns
    -------
    irrad_t : float
        Irradiance on tilted surface for specific location and time.
        
    References
    -------
    [1] William F. Holmgren, Clifford W. Hansen, and Mark A. Mikofski.
    “pvlib python: a python package for modeling solar energy systems.” 
    Journal of Open Source Software, 3(29), 884, (2018). 
    https://doi.org/10.21105/joss.00884
    
    [2] Eiker Ursula. "Solare Technologien für Gebäude" Springer, (2012).
    https://doi.org/10.1007/978-3-8348-8237-0

    '''
    
    solar_pos = solarposition.get_solarposition(time, lat, long, alt, pressure,
                                               'nrel_numpy', temp)
    sol_az = solar_pos.at[time,'azimuth']
    sol_zen = solar_pos.at[time,'zenith']
    
    cos_tilt = np.cos(np.radians(sol_zen)*np.cos(np.radians(panel_elev))+
                      np.sin(np.radians(sol_zen))*
                      np.sin(np.radians(panel_elev))*
                      np.cos(np.radians(sol_az-panel_az)))
    
    irrad_dir_t = irrad.at[time,"Gb(n)"]*np.maximum(0,cos_tilt/np.sin(np.radians(90-sol_zen)))
    irrad_diff_t = irrad.at[time,"Gd(h)"]*(1+np.cos(np.radians(panel_elev)))*0.5
    irrad_ref_t = irrad.at[time,"G(h)"]*alb*(1-np.cos(np.radians(panel_elev)))*0.5
    irrad_t = irrad_dir_t + irrad_diff_t + irrad_ref_t
    
    return irrad_t
    
    