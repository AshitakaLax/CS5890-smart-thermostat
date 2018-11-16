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
	assert totalPowerUsed == startupEnergy + 

