from datetime import timedelta
#import building

class HVAC():
	"""Simulates an HVAC system with the startup times 
	and all of the of the cycles that a normal furnace has		
		Keyword Arguments:
			gasValveEnergy {int} -- The amount of energy used by the gas value solenoid valve (default: {12 Watts})
			gasVentBlowerEnergy {int} -- The vent for the used gas out of the top of the heat exchange (default: {184 Watts})
			gasRateEnergy {int} -- The equivalent KWH for 80,000 BTU/H of gas or BTUH with a conversion ratio of 1BTUH == 0.29WH (default: {29307 W})
			flameIgnitorEnergy {int} -- The ceramic flame ignitor to start the gas (default: {460 Watts})
			houseBlowerEnergy {int} -- The HVAC blower to circulate the air through the house, taking air in from the cool air return. default blower is a 1/3 HP motor (default: {587 Watts})
			airConditioningEnergy {int} -- The amount of energy the air conditioner compressor uses which provites 42,000 BTUs (default: {3740 Watts})
			gasVentShutOffDelta {timedelta} -- the negative time for the gas vent shuts off befor the heater is off(default: {-120 seconds})
			gasValveShutOffDelta {timedelta} -- the negative time for the gas Valve shuts off befor the heater is off (default: {-150 seconds})
			flameIgnitorDuration {timedelta} -- the time from the beginning of the heater being on that power is applied to the flame starter (default: {30 seconds})
			gasValveOpenDelay {timedelta} -- the time from the beginning of the heater being on before the gas is turned on (default: {30 seconds})
			houseBlowerOnDelay {timedelta} -- the time from the beginning of the heater being on before the blower turns on (default: {70 seconds})
		"""
	def __init__(self, 
	gasValveEnergy=12, 
	gasVentBlowerEnergy=184, 
	gasRateEnergy=29307, 
	flameIgnitorEnergy=460, 
	houseBlowerEnergy=587, 
	airConditioningEnergy= 3740,
	gasVentShutOffDelta=timedelta(seconds = -120),
	gasValveShutOffDelta=timedelta(seconds = -150),
	flameIgnitorDuration=timedelta(seconds = 30),
	gasValveOpenDelay=timedelta(seconds = 30),
	houseBlowerOnDelay=timedelta(seconds = 70)):
		# parameter variables
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

		# Initialize Public Variables
		self.TotalPowerUsed = 0.0 # The total number of watts used
		self.TotalTimeInSeconds = 0 # The total amount of time the furnace has run for
		self.TotalPowerHeatingUsed = 0.0 # The Total amount of Power Heating has been used (includes gas heating energy and overhead energy)
		self.TotalPowerCoolingUsed = 0.0 # The Total amount of Power Cooling has been used (includes cooling energy and overhead energy)
		self.TotalDurationHeatingOn = 0.0 # The total amount of time the heating has been used (including starting and shutdown usage)
		self.TotalDurationCoolingOn = 0.0 # The total amount of time the cooling has been used
		self.CoolingIsOn = False # whether the Cooling is on or off
		self.HeatingIsShuttingDown = False # whether the Heating is in the shutting down phase
		self.HeatingIsOn = False # Whether the Heater is on or off (This is true when the heating is shutting down)
		self.LastCoolingDuration = 0 # The last length of time of the last cooling duration
		self.LastHeatingDuration = 0 # the last length of time of the last heating duration (this includes the starting and shutdown usage)
		self.TotalGasEnergyUsed = 0.0 # The total amount of gas energy
		self.NumberOfTimesHeatingTurnedOn = 0
		self.NumberOfTimesCoolingTurnedOn = 0

		# initialize Private Variables
		self.__HeatingShutoffDuration = 0 # Used to keep track of how long we have been shutting down the heater
		self.__lastCoolingEnergyInputed = 0 # Used to keep track of the last amount of just cooling energy that was inputed into the house
		self.__lastHeatingEnergyInputed = 0 # Used to keep track of the last amount of just heating energy that was inputed into the house (this is 0 during heating start up)

		
	def TurnCoolingOn(self):
		"""Turns the A/C on.
		"""
		if self.HeatingIsOn:
			return
		
		self.NumberOfTimesCoolingTurnedOn = self.NumberOfTimesCoolingTurnedOn + 1
		self.LastCoolingDuration = 0
		self.CoolingIsOn = True

	def TurnCoolingOff(self):
		"""Turns the A/C off.
		"""
		self.CoolingIsOn = False

	def TurnHeatingOn(self):
		"""Turns the Heater on by starting the initial furnace sequence.
		"""
		# if heater is on, we can't turn it on again
		if self.HeatingIsOn:
			return

		# check whether we can turn the heating on
		if self.HeatingIsShuttingDown:
			return

		# Can't turn on the Heater when the Cooling is already on
		if self.CoolingIsOn:
			return
		
		self.NumberOfTimesHeatingTurnedOn = self.NumberOfTimesHeatingTurnedOn + 1
		self.LastHeatingDuration = 0
		self.__HeatingShutoffDuration = 0
		self.HeatingIsOn = True
		
	def TurnHeatingOff(self):
		"""Turns the Heater off by starting the shutdown sequence.
		"""

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
		return self.__air_conditioning_energy + self.__house_blower_energy
	
	def GetLastIntervalCoolingPower(self):
		"""Gets the amount of power that was inputed to actually cooling the house
		"""
		return self.__lastCoolingEnergyInputed
	
	def GetAverageWattsPerSecond(self):
		"""Gets the amount of power that was inputed to actually cooling the house
		"""
		if (self.TotalPowerUsed == 0.0 or self.TotalTimeInSeconds == 0):
			return 0.0
		return self.TotalPowerUsed / self.TotalTimeInSeconds

	def GetTotalGasEnergyUsed(self):
		"""Gets the total Amount of Gas energy used
		"""
		return self.TotalGasEnergyUsed

	def SimulateOneSecond(self):
		"""Runs the model for 1 second to determine the total energy used
		"""
		energyConsumedSum = 0.0
		self.TotalTimeInSeconds = self.TotalTimeInSeconds + 1
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
		"""Sums the heating portions of the HVAC for one second, and keeps track of the stage of the heating (starting, running, and cooling)
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
				self.TotalGasEnergyUsed = self.TotalGasEnergyUsed + self.__gas_rate_energy
				heatingSum = heatingSum + self.__gas_valve_energy + self.__gas_rate_energy + self.__gas_vent_blower_energy
		else:
			# the system is in mid run with the gas vent running, gas energy, gas valve is on, and house blower
			self.__lastHeatingEnergyInputed = self.__gas_rate_energy # calculation for the amount of heat input to the house
			self.TotalGasEnergyUsed = self.TotalGasEnergyUsed + self.__gas_rate_energy
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


		
	def GetElectricKilowattHours(self):
		"""Gets the number of KWH the HVAC has Used in terms of Electricity
		"""
		totalGasEnergyUsed = self.GetTotalGasEnergyUsed()
		totalEnergy = self.TotalPowerUsed
		totalElectricEnergyUsed = totalEnergy - totalGasEnergyUsed
		totalTimeHVACRunning = self.TotalDurationHeatingOn + self.TotalDurationCoolingOn
		totalTimeHVACRunning = self.TotalTimeInSeconds
		# convert the total Watts and convert that to KWH

		hoursUsed = totalTimeHVACRunning / 3600
		# convert the totalElectricEnergyUsed to an average watts per hour
		averageWatts = totalElectricEnergyUsed / totalTimeHVACRunning
		kwhUsed = averageWatts * hoursUsed
		return kwhUsed / 1000


	def GetGasKilowattHours(self):
		"""Gets the number of KWH the HVAC has Used in terms of gas equivalent
		"""
		totalGasEnergyUsed = self.GetTotalGasEnergyUsed()



	def GetGasDTH(self):
		"""Gets the number of DTH the HVAC has Used 
		"""
		totalGasEnergyUsed = self.GetTotalGasEnergyUsed()
		if(totalGasEnergyUsed == 0.0):
			return 0.0

		dthUsed = self.ConvertWattsToDTH(totalGasEnergyUsed, self.TotalDurationHeatingOn)
		return dthUsed


	def ConvertWattsToDTH(self, watts, seconds:int):
		"""Converts the watts and the timespan into Decatherms equivalent
		
		Arguments:
			watts {energy} -- The sumation of watts over the timespan (this is weird, and could be improved)
			seconds {int} -- The length of time the watts were summed 
		"""
		# Convert Watts to Watt hours
		# determine the number of hours
		hours = seconds / 3600.0
		# calculate the average watts for the timeframe given
		averageWatts = watts / seconds
		wattHours = averageWatts * hours
		kilowattHours = wattHours / 1000
		
		# convert  Watt hours into DTH
		return kilowattHours / 293.001111

