#!/usr/bin/env python
# coding: utf-8

# # Time-varying Plots

# This app allows you to explore how the GDP-CO2 relationship varies across regions and over time.

# In[26]:


# Importing libraries
#%matplotlib inline

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()

from ipywidgets import interact, fixed
import ipywidgets as widgets


# In[27]:


# Creating flexible plotting function
def FlexPlot(region, year):
    """
    Makes GDP-CO2 scatterplot for a given region in a given year.

    ARGUMENTS
        * region: Which region to plot. It must be from the list: 'World', 'OECD', 'Asia', 'REF', 'MAF', 'LAM'.
        * year:   Which year to plot.
    """
    
    if region=='World':
        x = lGDP_world.loc[year]
        y = lCO2_world.loc[year]
    
    elif region=='OECD':
        x = lGDP_OECD.loc[year]
        y = lCO2_OECD.loc[year]
        
    elif region=='REF':
        x = lGDP_REF.loc[year]
        y = lCO2_REF.loc[year]
        
    elif region=='Asia':
        x = lGDP_Asia.loc[year]
        y = lCO2_Asia.loc[year]
        
    elif region=='MAF':
        x = lGDP_MAF.loc[year]
        y = lCO2_MAF.loc[year]
        
    elif region=='LAM':
        x = lGDP_LAM.loc[year]
        y = lCO2_LAM.loc[year]

    plt.scatter(x,y, color='black')
    plt.xlabel('log(GDP)')
    plt.ylabel('log(CO$_2$)')
    plt.show()


# In[28]:


# Loading data
GDP = pd.read_excel('Data/GDP.xlsx', sheet_name='Python', index_col=0)
GDP.sort_index(axis=1, inplace=True)

POP = pd.read_excel('Data/Population.xlsx', sheet_name='Python', index_col=0)
POP.sort_index(axis=1, inplace=True)

DEF = pd.read_excel('Data/Deflator.xlsx', sheet_name='Python', index_col=0)
DEF.sort_index(axis=1, inplace=True)

PPP = pd.read_excel('Data/PPP.xlsx', sheet_name='Python', index_col=0)
PPP.sort_index(axis=1, inplace=True)

CO2 = pd.read_excel('Data/CO2_GCP.xlsx', sheet_name='Python', index_col=0)
CO2.sort_index(axis=1, inplace=True)

# Aligning series
World_countries = list(CO2.columns.intersection(GDP.columns))

GDP = GDP[World_countries]
POP = POP[World_countries]
DEF = DEF[World_countries]
PPP = PPP[World_countries]
CO2 = CO2[World_countries]

POP_world = POP.sum(axis=1)

# Constructing per capita series
year = np.where(GDP.index == 2005)[0][0]

Real_GDP     = GDP / DEF
GDP_2005     = Real_GDP * np.reshape(np.array(DEF.iloc[year,:]), (1,-1), order='F')
GDP_USD_2005 = GDP_2005 / np.reshape(np.array(PPP.iloc[year,:]), (1,-1), order='F')
GDP_PC       = (GDP_USD_2005 / 1e9) / (POP / 1e6)

CO2_PC       = (CO2 * 3.664) / (POP / 1e6)

# Constructing time series
time = GDP.index.values
time = np.reshape(time, (-1,1), order='F')


# In[29]:


# Creating log-transformed series
lGDP_world = np.log(GDP_PC)
lCO2_world = np.log(CO2_PC)

OECD_countries = list(
    {'ALB', 'AUS', 'AUT', 'BEL', 'BIH', 'BGR', 'CAN', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC',
     'GUM', 'HUN', 'ISL', 'IRL', 'ITA', 'JPN', 'LVA', 'LTU', 'LUX', 'MLT', 'MNE', 'NLD', 'NZL', 'NOR', 'POL', 'PRT',
     'PRI', 'ROU', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'MKD', 'TUR', 'GBR',
     'USA'}.intersection(set(World_countries)))

lGDP_OECD = lGDP_world[OECD_countries]
lCO2_OECD = lCO2_world[OECD_countries]

REF_countries  = list(
    {'ARM', 'AZE', 'BLR', 'GEO', 'KAZ', 'KGZ', 'MDA', 'RUS', 'TJK', 'TKM', 'UKR',
     'UZB'}.intersection(set(World_countries)))

lGDP_REF = lGDP_world[REF_countries]
lCO2_REF = lCO2_world[REF_countries]

Asia_countries = list(
    {'AFG', 'BGD', 'BTN', 'BRN', 'KHM', 'CHN', 'PRK', 'KOR', 'FJI', 'PYF', 'IND', 'IDN', 'LAO', 'MYS', 'MDV', 'FSM',
     'MNG', 'MMR', 'NPL', 'NCL', 'PAK', 'PNG', 'PHL', 'WSM', 'SGP', 'SLB', 'LKA', 'THA', 'TLS', 'VUT',
     'VNM'}.intersection(set(World_countries)))

lGDP_Asia = lGDP_world[Asia_countries]
lCO2_Asia = lCO2_world[Asia_countries]

MAF_countries = list(
    {'DZA', 'AGO', 'BHR', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV', 'CAF', 'TCD', 'COM', 'COD', 'COG', 'CIV', 'DJI',
     'EGY', 'GNQ', 'ERI', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'IRN', 'IRQ', 'ISR', 'JOR', 'KEN', 'KWT', 'LBN',
     'LSO', 'LBR', 'LBY', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MAR', 'MOZ', 'NAM', 'NER', 'NGA', 'PSE', 'OMN', 'QAT',
     'RWA', 'SAU', 'SEN', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'SWZ', 'SYR', 'TGO', 'TUN', 'UGA', 'ARE', 'TZA', 'YEM',
     'ZMB', 'ZWE'}.intersection(set(World_countries)))

lGDP_MAF = lGDP_world[MAF_countries]
lCO2_MAF = lCO2_world[MAF_countries]

LAM_countries  = list(
    {'ARG', 'ABW', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CHL', 'COL', 'CRI', 'CUB', 'DOM', 'ECU', 'SLV', 'GRD', 'GTM',
     'GUY', 'HTI', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'PRY', 'PER', 'SUR', 'TTO', 'VIR', 'URY',
     'VEN'}.intersection(set(World_countries)))

lGDP_LAM = lGDP_world[LAM_countries]
lCO2_LAM = lCO2_world[LAM_countries]


# In[30]:


interact(FlexPlot, region=['World', 'OECD', 'REF', 'Asia', 'MAF', 'LAM'], year=widgets.IntSlider(min=1960, max=2018, step=1, value=1960));

