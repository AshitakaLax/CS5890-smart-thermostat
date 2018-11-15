from datetime import timedelta
from simplesimple import Building

conditioned_floor_area = 100
building = Building(
    heat_mass_capacity=165000 * conditioned_floor_area,
    heat_transmission=200,
    maximum_cooling_power=-10000,
    maximum_heating_power=10000,
    initial_building_temperature=16,
    time_step_size=timedelta(minutes=10),
    conditioned_floor_area=conditioned_floor_area
)

# simulate one time step
print(building.current_temperature) # returns 16
building.step(outside_temperature=20, heating_setpoint=18, cooling_setpoint=26)
print(building.current_temperature) # returns ~16.4