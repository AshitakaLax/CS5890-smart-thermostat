from datetime import timedelta
import building

class HVAC():
	"""Simulates an HVAC system with the startup times 
	and all of the of the cycles that a normal furnace has

	"""
	def init(self, gasValveEnergy=12, gasVentBlowerEnergy=184, 
	gasRateEnergy=29307, flameIgnitorEnergy=460, 
	houseBlowerEnergy=587, airConditioningEnergy= 3740,
	gasVentShutOffDelta=timedelta(-120),
	gasValveShutOffDelta=timedelta(-150),
	flameIgnitorDuration=timedelta(30),
	gasValveOpenDelay=timedelta(30),
	houseBlowerOnDelay=timedelta(70)):
		"""The HVAC object initializer
		
		Keyword Arguments:
			gasValveEnergy {int} -- The amount of energy used by the gas value solenoid valve (default: {12 Watts})
			gasVentBlowerEnergy {int} -- The vent for the used gas out of the top of the heat exchange (default: {184 Watts})
			gasRateEnergy {int} -- The equivalent KWH for 80,000 BTU/H of gas or BTUH with a conversion ratio of 1BTUH == 0.29WH (default: {29307 W})
			flameIgnitorEnergy {int} -- The ceramic flame ignitor to start the gas (default: {460 Watts})
			houseBlowerEnergy {int} -- The HVAC blower to circulate the air through the house, taking air in from the cool air return. default blower is a 1/3 HP motor (default: {587 Watts})
			airConditioningEnergy {int} -- The amount of energy the air conditioner compressor uses which provites 42,000 BTUs (default: {3740 Watts})
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
		self.TotalPowerUsed = 0.0
		self.TotalGasUsed = 0.0
		self.TotalDurationHeatingOn = 0.0
		self.TotalDurationCoolingOn = 0.0
		self.CoolingIsOn = False
		self.HeatingIsOn = False
		self.LastCoolingDuration = 0
		self.LastHeatingDuration = 0
		
	def TurnCoolingOn(self):
		if self.HeatingIsOn:
			return

		self.LastCoolingDuration = 0
		self.CoolingIsOn = True

	def TurnCoolingOff(self):
		self.CoolingIsOn = False
		self.TotalDurationCoolingOn = self.TotalDurationCoolingOn + self.LastCoolingDuration

	def TurnHeatingOn(self):
		if self.CoolingIsOn:
			return
			
		self.LastHeatingDuration = 0
		self.HeatingIsOn = True
		
	def TurnHeatingingOff(self):
		self.HeatingIsOn = False
		self.TotalDurationHeatingOn = self.TotalDurationHeatingOn + self.LastHeatingDuration

	def SimulateOneSecond(self):
		"""Runs the model for 1 second to determine the total energy used
		"""

		if self.CoolingIsOn == False and self.HeatingIsOn == False:
			return
		# check whether the 

		


