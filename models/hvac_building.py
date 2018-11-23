from datetime import timedelta
from  .hvac import HVAC
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
		* time_step_size:               [s]
		* conditioned_floor_area:       [m**2]
	"""

	def __init__(self, hvac: HVAC, heat_mass_capacity, heat_transmission,
			initial_building_temperature, time_step_size,
			conditioned_floor_area):

		self.building_hvac = hvac
		self.__heat_mass_capacity = heat_mass_capacity
		self.__heat_transmission = heat_transmission
		self.__maximum_cooling_power = hvac.GetMaxCoolingPower()
		self.__maximum_heating_power = hvac.GetMaxHeatingPower()
		self.current_temperature = initial_building_temperature
		self.__time_step_size = time_step_size
		self.__conditioned_floor_area = conditioned_floor_area

	def step(self, outside_temperature, heating_setpoint, cooling_setpoint):
		"""Performs building simulation for the next time step.
		
		Parameters:
			* outside_temperature: [℃]
			* heating_setpoint: heating setpoint of the HVAC system [℃]
			* cooling_setpoint: cooling setpoint of the HVAC system [℃]
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
				heating_setpoint=heating_setpoint,
				cooling_setpoint=cooling_setpoint,
				heating_cooling_power=heating_cooling_power
			)
		
		# check whether the heater of Cooling is on
		btu_power = 0.0
		if self.building_hvac.HeatingIsOn:
			btu_power = self.building_hvac.GetLastIntervalHeatingPower()

		elif self.building_hvac.CoolingIsOn:
			btu_power = self.building_hvac.GetLastIntervalCoolingPower()
		
		next_temperature_heating_cooling = next_temperature(btu_power)
		self.current_temperature = next_temperature_heating_cooling

	def _next_temperature(self, outside_temperature, heating_setpoint, cooling_setpoint, heating_cooling_power):
		dt_by_cm = self.__time_step_size.total_seconds() / self.__heat_mass_capacity
		return (self.current_temperature * (1 - dt_by_cm * self.__heat_transmission) + dt_by_cm * (heating_cooling_power + self.__heat_transmission * outside_temperature))