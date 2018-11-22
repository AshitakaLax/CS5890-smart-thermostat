from datetime import timedelta
#import building

class HVAC():
	"""Simulates an HVAC system with the startup times 
	and all of the of the cycles that a normal furnace has

	"""
	def __init__(self, gasValveEnergy=12, gasVentBlowerEnergy=184, 
	gasRateEnergy=29307, flameIgnitorEnergy=460, 
	houseBlowerEnergy=587, airConditioningEnergy= 3740,
	gasVentShutOffDelta=timedelta(seconds = -120),
	gasValveShutOffDelta=timedelta(seconds = -150),
	flameIgnitorDuration=timedelta(seconds = 30),
	gasValveOpenDelay=timedelta(seconds = 30),
	houseBlowerOnDelay=timedelta(seconds = 70)):
		"""The HVAC object initializer
		
		Keyword Arguments:
			gasValveEnergy {int} -- The amount of energy used by the gas value solenoid valve (default: {12 Watts})
			gasVentBlowerEnergy {int} -- The vent for the used gas out of the top of the heat exchange (default: {184 Watts})
			gasRateEnergy {int} -- The equivalent KWH for 80,000 BTU/H of gas or BTUH with a conversion ratio of 1BTUH == 0.29WH (default: {29307 W})
			flameIgnitorEnergy {int} -- The ceramic flame ignitor to start the gas (default: {460 Watts})
			houseBlowerEnergy {int} -- The HVAC blower to circulate the air through the house, taking air in from the cool air return. default blower is a 1/3 HP motor (default: {587 Watts})
			airConditioningEnergy {int} -- The amount of energy the air conditioner compressor uses which provites 42,000 BTUs (default: {3740 Watts})
			gasVentShutOffDelta {timedelta} -- the time for the gas vent to shutoff (default: {3740 Watts})
		"""

		self.__gas_valve_energy = gasValveEnergy
		self.__gas_vent_blower_energy = gasVentBlowerEnergy
		self.__gas_rate_energy = gasRateEnergy
		self.__flame_ignitor_energy = flameIgnitorEnergy
		self.__house_blower_energy = houseBlowerEnergy
		self.__air_conditioning_energy = airConditioningEnergy
		self.__gas_vent_shut_off_delta = gasVentShutOffDelta
		self.__gas_valve_shut_off_delta = gasValveShutOffDelta
		self.__flame_ignitor_duration = flameIgnitorDuration
		self.__gas_valve_open_delay = gasValveOpenDelay
		self.__house_blower_on_delay = houseBlowerOnDelay
		self.__HeatingShutoffDuration = 0
		self.TotalPowerUsed = 0.0
		self.TotalPowerHeatingUsed = 0.0
		self.TotalPowerCoolingUsed = 0.0
		self.TotalDurationHeatingOn = 0.0
		self.TotalDurationCoolingOn = 0.0
		self.CoolingIsOn = False
		self.HeatingIsShuttingDown = False
		self.HeatingIsOn = False
		self.LastCoolingDuration = 0
		self.LastHeatingDuration = 0
		self.__lastCoolingEnergyInputed = 0
		self.__lastHeatingEnergyInputed = 0
		
	def TurnCoolingOn(self):
		if self.HeatingIsOn:
			return

		self.LastCoolingDuration = 0
		self.CoolingIsOn = True

	def TurnCoolingOff(self):
		self.CoolingIsOn = False

	def TurnHeatingOn(self):
		# check whether we can turn the heating on
		if self.HeatingIsShuttingDown:
			return

		# Can't turn on the Heater when the Cooling is already on
		if self.CoolingIsOn:
			return
		
		self.LastHeatingDuration = 0
		self.__HeatingShutoffDuration = 0
		self.HeatingIsOn = True
		
	def TurnHeatingOff(self):
		# check whether we are just starting to turn off the heater
		if self.HeatingIsOn and not self.HeatingIsShuttingDown:
			self.HeatingIsShuttingDown = True

		# the simulation will manage when the funace is completely shutoff
		#self.HeatingIsOn = False
		#self.TotalDurationHeatingOn = self.TotalDurationHeatingOn + self.LastHeatingDuration
		# Update the the state of the Heating since the heater can't shutdown for a while longer

	def GetMaxHeatingPower(self):
		"""Gets the Max Heating available for the furnace
		"""
		return self.__gas_rate_energy
	
	def GetLastIntervalHeatingPower(self):
		"""Gets the amount of heating power that was inputed to actually heating the house
		"""
		return self.__lastHeatingEnergyInputed
	
	def GetMaxCoolingPower(self):
		"""Get the max amount of cooling available from the A/C
		"""
		return self.__air_conditioning_energy
	
	def GetLastIntervalCoolingPower(self):
		"""Gets the amount of power that was inputed to actually cooling the house
		"""
		return self.__lastCoolingEnergyInputed

	def SimulateOneSecond(self):
		"""Runs the model for 1 second to determine the total energy used
		"""
		energyConsumedSum = 0.0
		self.__lastCoolingEnergyInputed = 0.0
		self.__lastHeatingEnergyInputed = 0.0
		if self.CoolingIsOn == False and self.HeatingIsOn == False:
			return
		# check whether the Heating is on
		if self.HeatingIsOn:
			# how long has heating been on
			energyConsumedSum = self.__SumHeating__()
			self.TotalPowerHeatingUsed = self.TotalPowerHeatingUsed + energyConsumedSum

			# Increment the Heater duration 
			self.LastHeatingDuration = self.LastHeatingDuration + 1
			if self.HeatingIsShuttingDown:
				# determine how long the till it is completely shutoff
				self.__HeatingShutoffDuration = self.__HeatingShutoffDuration + 1

		else:
			# how long has Cooling been on
			energyConsumedSum = self.__SumCooling__()
			self.TotalPowerCoolingUsed = self.TotalPowerCoolingUsed + energyConsumedSum
			self.TotalDurationCoolingOn = self.TotalDurationCoolingOn + 1
			self.LastCoolingDuration = self.LastCoolingDuration + 1

		self.TotalPowerUsed = self.TotalPowerUsed + energyConsumedSum
		return energyConsumedSum

	def __SumHeating__(self):
		"""Sums the heating portions of the HVAC
		"""
		heatingSum = 0.0
		# determine which phase the heating is in

		# check whether it is shutting down, this is a first check in case they decide to shutdown in the middle of the startup
		if self.HeatingIsShuttingDown:
			self.__lastHeatingEnergyInputed = self.__determine_shutdown_heat_energy()
			if self.__HeatingShutoffDuration < (-1 * self.__gas_vent_shut_off_delta.total_seconds()) :
				heatingSum = heatingSum + self.__gas_vent_blower_energy
			if self.__HeatingShutoffDuration < (-1 * self.__gas_valve_shut_off_delta.total_seconds()) :
				heatingSum = heatingSum + self.__house_blower_energy
			else:
				# we have finished the shut off cycle
				self.HeatingIsOn = False
				self.HeatingIsShuttingDown = False
				self.TotalDurationHeatingOn = self.TotalDurationHeatingOn + self.LastHeatingDuration

		# heater is starting up
		elif self.LastHeatingDuration < self.__house_blower_on_delay.total_seconds():
			# Pre gas turns on
			if self.LastHeatingDuration < self.__flame_ignitor_duration.total_seconds():
				heatingSum = heatingSum + self.__gas_vent_blower_energy + self.__flame_ignitor_energy
			else:
				# after the gas turns on, but the blower hasn't turned on yet
				self.__lastHeatingEnergyInputed = self.__gas_rate_energy
				heatingSum = heatingSum + self.__gas_valve_energy + self.__gas_rate_energy + self.__gas_vent_blower_energy
		else:
			# the system is in mid run with the gas vent running, gas energy, gas valve is on, and house blower
			self.__lastHeatingEnergyInputed = self.__gas_rate_energy # calculation for the amount of heat input to the house
			heatingSum = heatingSum + self.__gas_valve_energy + self.__house_blower_energy + self.__gas_rate_energy + self.__gas_vent_blower_energy
			
		return heatingSum


	def __SumCooling__(self):
		"""Sums the cooling portions of the HVAC for the last second
		"""
		# check if Cooling is on
		if not self.CoolingIsOn:
			return 0.0
		
		# The blower and compressor are running
		self.__lastCoolingEnergyInputed = self.__air_conditioning_energy
		acSum = self.__air_conditioning_energy + self.__house_blower_energy
		return acSum

	def __determine_shutdown_heat_energy(self):
		"""Used to calculate the amount of energy that is still left in the heat register that could be added to the house
		"""
		totalShutdownTime = -1 * self.__gas_valve_shut_off_delta.total_seconds()
		timeRemaining = totalShutdownTime - self.__HeatingShutoffDuration
		if timeRemaining <= 0:
			return 0.0
		
		# caculate the percentage of in the shutdown time
		gasHeatPercentage = timeRemaining / totalShutdownTime
		return gasHeatPercentage * self.__gas_rate_energy

		


