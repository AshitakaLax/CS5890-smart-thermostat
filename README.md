## CAUTION (not being actively developed)

While this is a good start to simulating a thermostat. It does have some cleanup todo.
1. RL was able to detect a weakness in the model and exploit it. specifically with the shutdown phase of the furnace when there still is heat on the heat exchange, gas is off and the blower is running. Model needs to have less heat based on a Non-profitable amout of BTU per dollar. Currently it views this 90 second phase as Free Energy.

2. Another portion would be to have a better model for going from cold furnace heat exchange to hot heat exchange. 

3. I was able to run with open-gym other aspects.

4. If anyone wants to expand this project. I'm more than happy to help transision and cleanup code to assist. Ping me, or post a ticket, and I'll get back to you.

Enjoy


# CS5890-smart-thermostat
This is a reinforced learning implementation of a thermal model of a house

The efforts here were greatly supported by Tim Tröndle work in his Simple Simple git repo on github.

The model is derived from the hourly dynamic model in ISO 13790. It has only one capacity and
one resistance.

Compared to the ISO 13790 there is

* no internal heat gain,
* full shading of the building, no direct or indirect sun light,
* no windows or doors,
* no ventilation,
* immediate heat transfer between air and surface.

This model is to mirror the behavior of a typical furance, and keep track of energy used.

