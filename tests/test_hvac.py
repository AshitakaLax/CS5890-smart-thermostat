from datetime import timedelta

import pytest
from models import HVAC

@pytest.fixture
def typicalHvac():
    return HVAC()

def test_HVAC_off(typicalHvac):
	"""Tests the typical HVAC when the heater and cooler are both off
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.SimulateOneSecond()
	totalPowerUsed = typicalHvac.TotalPowerUsed
	assert totalPowerUsed == 0.0

def test_HVAC_on(typicalHvac):
	"""Tests the typical HVAC when the heater is on
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.TurnHeatingOn()
	typicalHvac.SimulateOneSecond()
	totalPowerUsed = typicalHvac.TotalPowerUsed
	assert typicalHvac.HeatingIsOn == True
	assert totalPowerUsed == (184 + 460)
	assert typicalHvac.LastHeatingDuration == 1
	
def test_HVAC_Pass_ignite(typicalHvac):
	"""Tests the typical HVAC when the heater is on for more 30 seconds
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	startupEnergy = (184 + 460) * 30
	typicalHvac.TurnHeatingOn()
	for i in range(31):
		typicalHvac.SimulateOneSecond()
	totalPowerUsed = typicalHvac.TotalPowerUsed
	assert typicalHvac.HeatingIsOn == True
	assert typicalHvac.LastHeatingDuration == 31

	# gas energy + startup energy + vent blower engery + gas valve energy
	assert totalPowerUsed == startupEnergy + 12 + 29307 + 184


def test_HVAC_cooling_on(typicalHvac: HVAC):
	"""Tests the typical power when the cooling is on
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.TurnCoolingOn()
	typicalHvac.SimulateOneSecond()
	assert typicalHvac.CoolingIsOn == True
	assert typicalHvac.TotalPowerUsed == (3740 + 587)
	assert typicalHvac.LastCoolingDuration == 1

def test_HVAC_cooling_on_off(typicalHvac: HVAC):
	"""Tests the typical power when the cooling is on and then switched to off
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.TurnCoolingOn()
	typicalHvac.SimulateOneSecond()
	typicalHvac.TurnCoolingOff()
	typicalHvac.SimulateOneSecond()
	typicalHvac.SimulateOneSecond()
	typicalHvac.SimulateOneSecond()

	assert typicalHvac.CoolingIsOn == False
	assert typicalHvac.TotalPowerUsed == (3740 + 587)
	assert typicalHvac.LastCoolingDuration == 1
	
def test_HVAC_Average_watts(typicalHvac: HVAC):
	"""Tests the The average watts per second calculation
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.TurnCoolingOn()
	typicalHvac.SimulateOneSecond()
	typicalHvac.TurnCoolingOff()

	assert typicalHvac.TotalPowerUsed == (3740 + 587)
	assert typicalHvac.LastCoolingDuration == 1
	assert typicalHvac.GetAverageWattsPerSecond() == (3740 + 587)
	typicalHvac.TurnCoolingOff()
	typicalHvac.SimulateOneSecond()
	typicalHvac.SimulateOneSecond()
	typicalHvac.SimulateOneSecond()

	assert typicalHvac.GetAverageWattsPerSecond() == ((3740 + 587) / 4)


def test_HVAC_Average_watts_per_day(typicalHvac: HVAC):
	"""Tests the The average watts per second calculation
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.TurnCoolingOn()
	for i in range(3600*24):
		typicalHvac.SimulateOneSecond()

	assert typicalHvac.GetAverageWattsPerSecond() == (3740 + 587)
	assert typicalHvac.GetAverageWattsPerSecond() * 24 == 103848
	assert typicalHvac.TotalPowerUsed / 3600 == 103848

def test_HVAC_Average_watts_for_small_time_frame(typicalHvac: HVAC):
	"""Tests the The average watts per second calculation
	
	Arguments:
		typicalHvac {HVAC} -- the hvac test fixture object
	"""
	typicalHvac.TurnCoolingOn()
	typicalHvac.SimulateOneSecond()
	typicalHvac.SimulateOneSecond()
	typicalHvac.SimulateOneSecond()

	assert typicalHvac.TotalPowerUsed == (3740 + 587) * 3
	
