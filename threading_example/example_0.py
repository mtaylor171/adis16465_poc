import RPi.GPIO as GPIO
import time
import threading


DR = 0
glob_var = 0

def spi_coms():
	while(true):
		while(DR != 1):
			pass
		print("Data received: ", glob_var)


def data_handle():
	for i in range(0,27):
		#print("thread2: ", i)
		time.sleep(0.5)
		if i % 3 == 0:
			glob_var = i
			DR = 1
		DR = 0





t1 = threading.Thread(target=spi_coms)
t2 = threading.Thread(target=data_handle)


t1.start()
t2.start()