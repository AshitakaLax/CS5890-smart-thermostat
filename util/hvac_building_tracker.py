
#from models import HVAC

class HvacBuildingTracker():
	""" Creates a tracker that will manage the data that the hvac building generates
	"""
	
	def __init__(self):
		"""Creates an instance of the hvac building tracker
		"""

		self.__HouseTempArr = []
		self.__OutsidTempArr = []
		self.__AvgPowerPerSecArr = []
	

	def AddSample(self, houseTemp: float, outsideTemp: float, avgPwrPerSecond: float):
		"""Adds a sample of the data for the house
		
		Arguments:
			houseTemp {float} -- The current house temperature in C
			outsideTemp {float} -- The current outside temperature in C
			avgPwrPerSecond {float} -- The average watts per second
		"""

		self.__HouseTempArr.append(houseTemp)
		self.__OutsidTempArr.append(outsideTemp)
		self.__AvgPowerPerSecArr.append(avgPwrPerSecond)