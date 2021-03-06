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
loganOutsideTemperatures_October = [1.11, 2.22, 1.67, 1.67, 2.22, 1.11, 1.11, 2.78, 4.44, 4.44, 5.56, 6.67, 6.67, 7.22, 6.67, 2.22, 2.22, 1.67, 1.11, 1.11, 0.56, 1.11, 0.00, 0.00]
loganOutsideTemperatures =[
-7
,-8
,-8
,-8
,-8
,-9
,-10
,-9
,-8
,-7
,-4
,-2
,-3
,-2
,-2
,-1
,-2
,-3
,-3
,-4
,-4
,-4
,-4
,-4
]

print()
print("Starting Hvac Building Example")
print()

# items I need to get for the state
# current Temp  float
# outside temp  float
# average power/second  float




# simulate one day
numberOfHeatingOn = 0
for outsideTemperature in loganOutsideTemperatures:
	# iterate through one hour with the same temperature
	for	i in range(3600):
		hvacBuilding.step(outsideTemperature)
		if not hvac.HeatingIsShuttingDown and hvac.HeatingIsOn and hvacBuilding.current_temperature > 18.8889:#21:
			print("Turning the Heater Off")
			hvac.TurnHeatingOff()

		if hvac.HeatingIsOn == False and hvacBuilding.current_temperature < 17.7778:#17:
			print("Turning the Heater On")
			numberOfHeatingOn = numberOfHeatingOn + 1
			hvac.TurnHeatingOn()

hvacBuilding.PrintSummary()

# todo run a loop with various parameters for the set points to determine the optimal temperature in terms of the delta