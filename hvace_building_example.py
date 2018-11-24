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
    heat_mass_capacity=165000 * conditioned_floor_area,
    heat_transmission=200,
    initial_building_temperature=18,
    conditioned_floor_area=conditioned_floor_area,
	hvacBuildingTracker = tracker
)

# a set of temperatures in Northern Utah, USA for one day
loganOutsideTemperatures = [1.11, 2.22, 1.67, 1.67, 2.22, 1.11, 1.11, 2.78, 4.44, 4.44, 5.56, 6.67, 6.67, 7.22, 6.67, 2.22, 2.22, 1.67, 1.11, 1.11, 0.56, 1.11, 0.00, 0.00]


# simulate one day
for outsideTemperature in loganOutsideTemperatures:
	# iterate through one hour with the same temperature
	for	i in range(3600):
		hvacBuilding.step(outsideTemperature)
		if hvacBuilding.current_temperature > 21:
			hvac.TurnHeatingOff()
		if hvacBuilding.current_temperature < 17:
			hvac.TurnHeatingOn()
print()
print()
print()
print()
print("The Current Temperature: " + str(hvacBuilding.current_temperature) + "C")
print("The total power used: " + str(hvac.TotalPowerUsed) + "Watts")
print("The total power used: " + str(hvac.TotalPowerUsed / 1000) + "KWatts")
print("The total Time furnace is on: " + str(hvac.TotalTimeInSeconds))
print("The Average Watts Per Second: " + str(hvac.GetAverageWattsPerSecond()))
totalEnergy = hvac.TotalPowerUsed
totalGasEnergyUsed = hvac.GetTotalGasEnergyUsed()

print("The Total Electrical Only Energy Used: " + str(totalEnergy - totalGasEnergyUsed))
print("The Total Gas Energy Used: " + str(totalGasEnergyUsed))


