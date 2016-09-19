#! /usr/bin/env python
#-*- encoding: utf-8 -*-

#created by @ceapalaciosal
#under code Creative Commons

import os
import sys
sys.path.append('core')
from clear import *
from emition import *
from distribution import *
from split import *
from speciation import *

folder = os.path.join('..','data', 'out', '')
clear(folder)

YEAR = int (raw_input('INSERT YEAR RUN: '))

database = os.path.join('..', 'data', 'in', 'database.xlsx')
FactorEmissions = os.path.join('..', 'data', 'in','EmissionsFactors', 'EmissionFactors.xlsx')
Pollutants = emition(database, FactorEmissions, YEAR)

emitions = os.path.join('..', 'data', 'out', 'year', 'Year_Emisions.csv')
distribution(emitions, Pollutants)


distribution  = os.path.join('..', 'data','out', 'distribution', '')
speciation(distribution)
