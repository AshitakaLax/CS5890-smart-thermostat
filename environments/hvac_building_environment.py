
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from tensorforce.environments import Environment
from models.hvac_building import HvacBuilding

class HvacBuildingEnvironment(Environment):
	"""The Environment for Reinforcement Learning
	
	Arguments:
		Environment {Environment} -- The base class for this to simulate the hvac building model
	"""
	def __init__(self, modelHvacBuilding:HvacBuilding, env_duration = 3600):
		self.engine = modelHvacBuilding
		self.__env_duration = env_duration
	
	def __str__(self):
		return 'HVAC Building Environment'

	def close(self):
		self.engine = None

	def reset(self):
		# TODO: Reset to `ones`?
		return self.engine.reset()

	def execute(self, action):
		terminal = self.engine.building_hvac.TotalTimeInSeconds >= self.__env_duration
		reward = self.engine.Act(action)
		# currently we are testing it with a constant temperature of 28 C
		# and just using cooling
		state = self.engine.get_state(28.0)
		return state, terminal, reward

	@property
	def states(self):
		return dict(type='float', shape=(3,))
		
	@property
	def actions(self):
		return dict(type='bool', num_actions=1)