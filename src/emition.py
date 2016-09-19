# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import os
import sys
import json
import math

sys.path.append('core')
from excelmatriz import * 
from wcsv import *
from date import *


def emition(archive, EmissionsFactors, YEAR): 
	matriz = convertXLSCSV(archive)
	MFE = convertXLSCSV(EmissionsFactors)

	'''Factors Emisions charged in RAM'''
	FE = {}
	for i in range(1,MFE.shape[0]):
		Activity = MFE[i][0]
		if FE.get(Activity) is None:
			FE[Activity] = float(MFE[i][1])

	head = matriz[0,:]
	index = 0
	for value in head: 
		if value == 'ID':
			colID = index
		if value == 'LAT':
			colLAT = index
		if value == 'LON':
			colLON = index
		if value == 'ROW':
			colROW = index
		if value == 'COL':
			colCOL = index
		if value == 'DATE':
			colDATE = index
		if value == 'DPY':
			colDPY = index
		if value == 'FUEL_SOLD_REG_MONTH' or value == 'FUEL SOLD REG MONTH':
			colFSRM = index
		if value == 'GROWRATE':
			colGROWRATE = index
		if value == 'STORAGE_VOC_(LB/YR)':
			colSTORAGEVOC = index
		index += 1 
		
	data = {}
	for i in range(1, matriz.shape[0]):
		ID = int(float(matriz[i][colID]))
		if data.get(ID) is None:
			data[ID] = {} 
			data[ID]['base'] = {'LAT': [], 'LON': [], 'ROW': [], 'COL': [], 'DPY': [], 'DATE': [], 'GROWRATE': [], 'FSRM': [], 'STORAGEVOC': []}
			data[ID]['results'] = {'STORAGE': [], 'FILLING': [], 'SPILLING': [], 'DISTRIBUTION': []}

		if data[ID]['base']['LAT'] == []:
			data[ID]['base']['LAT'].append(float(matriz[i][colLAT]))
			data[ID]['base']['LON'].append(float(matriz[i][colLON]))
			data[ID]['base']['ROW'].append(int(float(matriz[i][colROW])))
			data[ID]['base']['COL'].append(int(float(matriz[i][colCOL])))
			data[ID]['base']['DPY'].append(int(float(matriz[i][colDPY])))
			if matriz[i][colDATE] == '':
				data[ID]['base']['DATE'].append(2014)
			else:
				data[ID]['base']['DATE'].append(int(xldate_to_datetime(float(matriz[i][colDATE]))))

			data[ID]['base']['FSRM'].append(float(matriz[i][colFSRM]))
			data[ID]['base']['STORAGEVOC'].append(float(matriz[i][colSTORAGEVOC]))
			data[ID]['base']['GROWRATE'].append(float(matriz[i][colGROWRATE]))

		n = YEAR - data[ID]['base']['DATE'][0]

		#print FE

		'''STORAGE VOC CALCULATION'''
		data[ID]['results']['STORAGE'] = ((data[ID]['base']['STORAGEVOC'][0] * math.exp(data[ID]['base']['GROWRATE'][0] * n))/2204.59) / data[ID]['base']['DPY'][0] 

		'''Calculation FILLING, SPILLING, DISTRIBUTION'''
		for pollutant in FE: 
			data[ID]['results'][pollutant] = (data[ID]['base']['FSRM'][0] * 12) * FE[pollutant] / data[ID]['base']['DPY'][0]


	FE['STORAGE'] = 0
	WriteYear(data)
	return FE
