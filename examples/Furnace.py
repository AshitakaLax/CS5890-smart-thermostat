from datetime import timedelta
from simplesimple import Building
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

conditioned_floor_area = 100
# building = Building(
#     heat_mass_capacity=165000 * conditioned_floor_area,
#     heat_transmission=200,
#     maximum_cooling_power=-10000,
#     maximum_heating_power=10000,
#     initial_building_temperature=16,
#     time_step_size=timedelta(minutes=1),
#     conditioned_floor_area=conditioned_floor_area
# )
building = Building(
    heat_mass_capacity=16000 * conditioned_floor_area,
    heat_transmission=300,
    maximum_cooling_power=-10000,
    maximum_heating_power=100000,
    initial_building_temperature=-16,
    time_step_size=timedelta(minutes=1),
    conditioned_floor_area=conditioned_floor_area
)

loganOutsideTemperatures = [1.11, 2.22, 1.67, 1.67, 2.22, 1.11, 1.11, 2.78, 4.44, 4.44, 5.56, 6.67, 6.67, 7.22, 6.67, 2.22, 2.22, 1.67, 1.11, 1.11, 0.56, 1.11, 0.00, 0.00]

# simulate one time step
print(building.current_temperature) # returns 16
#building.step(outside_temperature=20, heating_setpoint=18, cooling_setpoint=26)
print(building.current_temperature) # returns ~16.4

print("Heater should be on")
print(building.heater_on)

# simulation for a single day in minutes
hourOfDay = -1
tempProfile = []
outsideTempProfile = []
furnaceOnProfile = []
acOnProfile = []
for i in range(1440):
	if i % 60 == 0:
		hourOfDay = hourOfDay + 1
	
	building.step(outside_temperature=loganOutsideTemperatures[hourOfDay], heating_setpoint=18, cooling_setpoint=26)
	#building.step(outside_temperature=-20.0, heating_setpoint=18, cooling_setpoint=26)
	tempProfile.append(building.current_temperature)
	acOnProfile.append(building.cooling_on)
	outsideTempProfile.append(loganOutsideTemperatures[hourOfDay])
	furnaceOnProfile.append(building.heater_on)
	print(building.current_temperature) # returns ~16.4


results = pd.DataFrame({
    'HeatingDemand': furnaceOnProfile,
    'CoolingDemand': acOnProfile,
    'IndoorAir': tempProfile,
    'OutsideTemp':  outsideTempProfile
})

# results[['HeatingDemand', 'CoolingDemand']].plot()
# plt.xlabel('min of day')
# plt.ylabel('on/off')
# plt.show()

results[['IndoorAir', 'OutsideTemp']].plot()
plt.xlabel('min of day')
plt.ylabel('C')
plt.show()