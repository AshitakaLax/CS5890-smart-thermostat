from datetime import timedelta
from  .hvac import HVAC
from util import HvacBuildingTracker
#import building
class HvacBuilding():
	"""A simple Hvac Building Energy Model.

	Consisting of one thermal capacity and one resistance, this model is derived from the
	hourly dynamic model of the ISO 13790. It models heating and cooling energy demand only. With the HVAC system

	Parameters:
		* hvac {HVAC}:           		The HVAC controller informing the building how much power to put into the system.
		* heat_mass_capacity:           capacity of the building's heat mass [J/K]
		* heat_transmission:            heat transmission to the outside [W/K]
		* maximum_cooling_power:        [W] (<= 0)
		* maximum_heating_power:        [W] (>= 0)
		* initial_building_temperature: building temperature at start time [℃]
		* conditioned_floor_area:       [m**2]
		* hvacTracker {HvacTracker} : The tracker to keep track of metrics with the HVAC (default: {None})
	"""

	def __init__(self, 
	hvac: HVAC, 
	heat_mass_capacity, 
	heat_transmission,
	initial_building_temperature,
	conditioned_floor_area,
	hvacBuildingTracker:HvacBuildingTracker = None):

		self.building_hvac = hvac
		self.__heat_mass_capacity = heat_mass_capacity
		self.__heat_transmission = heat_transmission
		self.__maximum_cooling_power = hvac.GetMaxCoolingPower()
		self.__maximum_heating_power = hvac.GetMaxHeatingPower()
		self.current_temperature = initial_building_temperature
		self.__time_step_size = timedelta(seconds=1)
		self.__conditioned_floor_area = conditioned_floor_area
		self.__hvac_building_tracker = hvacBuildingTracker

	def step(self, outside_temperature):
		"""Performs building simulation for the next time step.
		
		Parameters:
			* outside_temperature: [℃]
		"""

		def next_temperature(heating_cooling_power):
			"""Gets the next temperature of the building
			
			Arguments:
				heating_cooling_power {watts} -- Amount of power used to heat or cool
			
			Returns:
				float -- Temperature in C
			"""

			return self._next_temperature(
				outside_temperature=outside_temperature,
				heating_cooling_power=heating_cooling_power
			)

		# Simulate the one second with the hvac to get the values that will be used
		self.building_hvac.SimulateOneSecond()

		# check whether the heater of Cooling is on
		btu_power = 0.0
		if self.building_hvac.HeatingIsOn:
			btu_power = self.building_hvac.GetLastIntervalHeatingPower()

		elif self.building_hvac.CoolingIsOn:
			btu_power = self.building_hvac.GetLastIntervalCoolingPower()
		
		next_temperature_heating_cooling = next_temperature(btu_power)
		self.current_temperature = next_temperature_heating_cooling
		
		# if the hvac_building_tracker exists, then we will add a sample to it.
		if self.__hvac_building_tracker != None:
			self.__hvac_building_tracker.AddSample(next_temperature_heating_cooling, outside_temperature, self.building_hvac.GetAverageWattsPerSecond())

	def GetHvacBuildingTracker(self):
		return self.__hvac_building_tracker
		
	def _next_temperature(self, outside_temperature, heating_cooling_power):
		dt_by_cm = self.__time_step_size.total_seconds() / self.__heat_mass_capacity
		return (self.current_temperature * (1 - dt_by_cm * self.__heat_transmission) + dt_by_cm * (heating_cooling_power + self.__heat_transmission * outside_temperature))


	def PrintSummary(self, dollarsPerKiloWattHour = 0.1149, dollarsPerDTH = 6.53535):
		"""Prints the summary of the Hvac building in the current state
		"""
		print()
		print("     RESULTS    ")
		print()
		print("The Number of times the furnace turns on: " + str(self.building_hvac.NumberOfTimesHeatingTurnedOn))
		print("The Current Temperature: " + str(self.current_temperature) + "C")
		print("The total power used: " + str(self.building_hvac.TotalPowerUsed) + "Watts")
		print("The total power used: " + str(self.building_hvac.TotalPowerUsed / 1000) + "KWatts")
		print("The total Time furnace is on: " + str(self.building_hvac.TotalTimeInSeconds))
		wattsPerSecond = self.building_hvac.GetAverageWattsPerSecond()
		print("The Average Watts Per Second: " + str(wattsPerSecond))

		# convert to Kilowatts per second
		KilowattHour = wattsPerSecond /1000
		# convert to kilowatts per hour
		KilowattHour = KilowattHour * 3600
		print("The Average KWH: " + str(KilowattHour))
		totalEnergy = self.building_hvac.TotalPowerUsed
		totalGasEnergyUsed = self.building_hvac.GetTotalGasEnergyUsed()

		print("The Total Electrical Only Energy Used: " + str(totalEnergy - totalGasEnergyUsed))
		print("The Total Gas Energy Used: " + str(totalGasEnergyUsed))
		print("Electrical Cost: $" + str(self.CalculateElectricEneregyCost()))
		print("Gas Cost: $" + str(self.CalculateGasEneregyCost()))

	def ConvertWattsToDTH(self, watts, seconds:int):
		"""Converts the watts and the timespan into Decatherms equivalent
		
		Arguments:
			watts {energy} -- The sumation of watts over the timespan
			seconds {int} -- The length of time the watts were summed
		"""
		# Convert Watts to Watt hours
		# determine the number of hours
		hours = seconds / 3600.0

		wattHours = watts / hours
		
		# convert  Watt hours into DTH
		return wattHours / 293001.111

	def CalculateGasEneregyCost(self, dollarsPerDTH = 6.53535):
		"""Calculates the total cost of energy for the gas energy used
		
		Keyword Arguments:
			dollarsPerDTH {float} -- calculates the cost per DTH (default: {6.53535})
		"""
		totalGasEnergyUsed = self.building_hvac.GetTotalGasEnergyUsed()
		dthUsed = self.ConvertWattsToDTH(totalGasEnergyUsed, self.building_hvac.TotalDurationHeatingOn)
		return dthUsed * dollarsPerDTH

	def CalculateElectricEneregyCost(self, dollarsPerKiloWattHour = 0.1149, ):
		"""Calculates the total cost of energy for the electric energy used
		
		Keyword Arguments:
			dollarsPerKiloWattHour {float} -- calculates the cost per KWH(default: {0.1149})
		"""
		totalGasEnergyUsed = self.building_hvac.GetTotalGasEnergyUsed()
		totalEnergy = self.building_hvac.TotalPowerUsed
		totalElectricEnergyUsed = totalEnergy - totalGasEnergyUsed
		totalTimeHVACRunning = self.building_hvac.TotalDurationHeatingOn + self.building_hvac.TotalDurationCoolingOn

		# convert the total Watts and convert that to KWH
		hoursUsed = totalTimeHVACRunning / 3600
		kwhUsed = totalElectricEnergyUsed / hoursUsed

		# convert the 
		return kwhUsed * dollarsPerKiloWattHour



