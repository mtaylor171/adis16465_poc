import RPi.GPIO as GPIO
import time
from threading import Thread, Event
import numpy as np


#DR = 0
#glob_var = 0

event = Event()

def spi_coms(DR, glob_var):
	#global DR
	#global glob_var
	while(True):
		if(DR ==1):
			print("Data received: ", glob_var)
		if event.is_set():
			break

DR = 0
glob_var = 0

t1 = Thread(target=spi_coms, args = (DR, glob_var, ))
t1.start()

def data_handle():
	global DR
	global glob_var
	while(True):
		try:
			DR = 0
			for i in range(0,27):
				print(i)
				time.sleep(0.5)
				if(i % 3 == 0):
					glob_var = i
					DR = 1
		except KeyboardInterrupt:
			event.set()
			break

data_handle()

t1.join()