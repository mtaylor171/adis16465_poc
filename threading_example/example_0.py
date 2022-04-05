import RPi.GPIO as GPIO
import time
from threading import Thread, Event
import numpy as np


#DR = 0
#glob_var = 0

event = Event()

def data_handle(data):
	while(True):
		data[0] = 0
		for i in range(0,27):
			print(i)
			time.sleep(0.5)
			if((i % 3) == 0):
				data[1] = i
				data[0] = 1


data = [0, 0]

t1 = Thread(target=data_handle, args = (data, ))
t1.start()

def spi_coms():
	while(True):
		try:
			if(data[0] == 1):
				print("Data received: ", data[1])
				data[0] = 0
			if event.is_set():
				break
		except KeyboardInterrupt:
			event.set()
			break

spi_coms()

t1.join()