from datetime import timedelta

import pytest
from models import HvacBuilding
from models import HVAC
from util import HvacBuildingTracker

@pytest.fixture
def hvacBuilding():
	conditioned_floor_area = 100
	tracker = HvacBuildingTracker()
	return HvacBuilding(
		HVAC(), 
		heat_mass_capacity=16500 * conditioned_floor_area,
		#heat_mass_capacity=165000 * conditioned_floor_area,
		heat_transmission=500,
		initial_building_temperature=22,
		conditioned_floor_area=conditioned_floor_area,
		hvacBuildingTracker=tracker)

def test_HVAC_building_tracker(hvacBuilding: HvacBuilding):
	
	# check that the temperature is getting cooler every time
	for i in range(10):
		hvacBuilding.step(0)
	
	assert len(hvacBuilding.GetHvacBuildingTracker().GetHouseTempArray()) > 9
		