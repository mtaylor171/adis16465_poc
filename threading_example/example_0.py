import RPi.GPIO as GPIO
import time
from threading import Thread, Event
import numpy as np


#DR = 0
#glob_var = 0

event = Event()

def data_handle(DR, glob_var):
	while(True):
		DR = 0
		for i in range(0,4):
			print(i)
			time.sleep(0.5)
			if(i % 3 == 0):
				glob_var = i
				DR = 1
				return DR, glob_var


DR = 0
glob_var = 0

t1 = Thread(target=data_handle, args = (DR, glob_var, ))
t1.start()

def spi_coms():
	while(True):
		try:
			if(DR ==1):
				print("Data received: ", glob_var)
			if event.is_set():
				break
		except KeyboardInterrupt:
			event.set()
			break

spi_coms()

t1.join()