from datetime import timedelta

import pytest
from models import HvacBuilding
from models import HVAC

@pytest.fixture
def hvacBuilding():
	
    conditioned_floor_area = 100
    return HvacBuilding(
		HVAC(), 
        heat_mass_capacity=16500 * conditioned_floor_area,
        #heat_mass_capacity=165000 * conditioned_floor_area,
        heat_transmission=500,
        initial_building_temperature=22,
        time_step_size=timedelta(seconds=1),
        conditioned_floor_area=conditioned_floor_area)

def test_HVAC_off(hvacBuilding: HvacBuilding):
	"""Tests the typical building gets colder and colder when the heater and cooler are both off
	
	Arguments:
		hvacBuilding {HvacBuilding} -- the hvac Building test fixture object
	"""
	# check that the temperature is getting cooler every time
	currentBuildingTemperature = 22
	for i in range(10):
		hvacBuilding.step(0, 30, 25)
		assert hvacBuilding.current_temperature < currentBuildingTemperature
		currentBuildingTemperature = hvacBuilding.current_temperature
		
def test_HVAC_on(hvacBuilding: HvacBuilding):
	"""Tests the typical building gets colder and colder when the heater and cooler are both off
	
	Arguments:
		hvacBuilding {HvacBuilding} -- the hvac Building test fixture object
	"""
	# check that the temperature is getting cooler every time
	currentBuildingTemperature = 22
	# turn on the furnace, it shouldn't change for the first while till we have completed the startup
	# so it will say at 22 for the first section
	hvacBuilding.building_hvac.TurnHeatingOn()

	for i in range(60):
		hvacBuilding.step(55, 0, 0)
		hvacBuilding.building_hvac.SimulateOneSecond()
		assert hvacBuilding.current_temperature > currentBuildingTemperature
		currentBuildingTemperature = hvacBuilding.current_temperature
	
	assert hvacBuilding.building_hvac.TotalPowerUsed > 0