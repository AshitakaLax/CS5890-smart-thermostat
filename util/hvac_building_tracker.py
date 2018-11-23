
#from models import HVAC

class HvacBuildingTracker():
	""" Creates a tracker that will manage the data that the hvac building generates
	"""

	def __init__(self):
		"""Creates an instance of the hvac building tracker
		"""
		self.__HouseTempArr = []
		self.__OutsideTempArr = []
		self.__AvgPowerPerSecArr = []
	
	def AddSample(self, houseTemp: float, outsideTemp: float, avgPwrPerSecond: float):
		"""Adds a sample of the data for the house
		
		Arguments:
			houseTemp {float} -- The current house temperature in C
			outsideTemp {float} -- The current outside temperature in C
			avgPwrPerSecond {float} -- The average watts per second
		"""

		self.__HouseTempArr.append(houseTemp)
		self.__OutsideTempArr.append(outsideTemp)
		self.__AvgPowerPerSecArr.append(avgPwrPerSecond)

	def GetHouseTempArray(self, isCelsius:bool = True):
		if isCelsius:
			return self.__HouseTempArr
		
		# convert an array to farienheit
		return self.__convertCArrayToF(self.__HouseTempArr)
		
	def GetOutsideTempArray(self, isCelsius:bool = True):
		if isCelsius:
			return self.__OutsideTempArr
		
		# convert an array to farienheit
		return self.__convertCArrayToF(self.__OutsideTempArr)

	def __convertCArrayToF(self, C_Array):
		f_array = []
		for c in C_Array:
			#convert 
			f = (c * (9/5))+32
			f_array.append(f)
		return f_array

