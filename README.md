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

