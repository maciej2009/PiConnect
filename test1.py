#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bez nazwy.py
#  
#  Copyright 2014  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



def main():
	print "start"
	import webiopi

	# load drivers
	from webiopi.devices.sensor.onewiretemp import DS18B20
	#from webiopi.devices.digital import MCP23017

	gpio = webiopi.GPIO # Helper for LOW/HIGH values
	Stycznik  = 18 # Heater plugged on the Expander Pin 0
	

	# initialize drivers
	tmp = DS18B20()

	#mcp = MCP23017(slave=0x20)
	
	gpio.setFunction(Stycznik,gpio.OUT)
	
	state = gpio.HIGH
	temp0 = 0
	while temp0 < 50.5:
		temp0 = tmp.getCelsius() 
		print temp0, state, gpio.HIGH
		
		
		gpio.output(Stycznik, state)
		if state == gpio.HIGH:
			state = gpio.LOW
		else:
			state = gpio.HIGH
		

	
	
	return 0

if __name__ == '__main__':
	main()

