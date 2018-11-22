from datetime import timedelta

import pytest
from models import HvacBuilding
from models import HVAC

@pytest.fixture
def hvacBuilding():
	
    conditioned_floor_area = 100
    return HvacBuilding(
		HVAC(), 
		True,
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