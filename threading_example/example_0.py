import RPi.GPIO as GPIO
import time
import threading
import numpy as np


DR = 0
glob_var = 0

def spi_coms(DR, glob_var):
	#global DR
	#global glob_var
	while(True):
		if(DR ==1):
			print("Data received: ", glob_var)


def data_handle(DR, glob_var):
	global DR
	global glob_var
	for i in range(0,27):
		print("thread2: ", i)
		time.sleep(0.5)
		if(i % 3 == 0):
			glob_var = i
			DR = 1
			print("DR = ", DR)
		DR = 0





t1 = threading.Thread(target=spi_coms, args = (DR, glob_var, ))
t2 = threading.Thread(target=data_handle, args = (DR, glob_var, ))


t1.start()
t2.start()

t1.join()
t2.join()