from models import HVAC
from models import HvacBuilding
from util import HvacBuildingTracker
# Create an instance of HVAC to simulate the Furnance
# use any parameters specific for your furnace
hvac = HVAC()

# Create the hvac building tracker to keep track of the simulation over time
tracker = HvacBuildingTracker()

# create the building model with the hvac and the tracker

conditioned_floor_area = 100
hvacBuilding = HvacBuilding(
	hvac, 
    heat_mass_capacity=16500 * conditioned_floor_area,
    heat_transmission=200,
    initial_building_temperature=18,
    conditioned_floor_area=conditioned_floor_area,
	hvacBuildingTracker = tracker
)

# a set of temperatures in Northern Utah, USA for one day
loganOutsideTemperatures = [18.0, 18.22, 18.67, 19.00, 19.22, 20.11, 20.11, 21.78, 22.44, 23.44, 24.56, 25.67, 24.67, 23.22, 22.67, 22.22, 21.22, 21.67, 20.11, 19.11, 19.56, 18.11, 18.00, 18.00]

print()
print("Starting Hvac Building Example")
print()

# simulate one day
numberOfCoolingTurnOn = 0
for outsideTemperature in loganOutsideTemperatures:
	# iterate through one hour with the same temperature
	for	i in range(3600):
		hvacBuilding.step(outsideTemperature)
		if hvac.CoolingIsOn and hvacBuilding.current_temperature < 17.3333:#21:
			print("Turning the AC Off")
			hvac.TurnCoolingOff()

		if hvac.CoolingIsOn == False and hvacBuilding.current_temperature > 18.8889 :#17:
			print("Turning the AC On")
			numberOfCoolingTurnOn = numberOfCoolingTurnOn + 1
			hvac.TurnCoolingOn()

hvacBuilding.PrintSummary()

# todo run a loop with various parameters for the set points to determine the optimal temperature in terms of the delta