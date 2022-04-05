import RPi.GPIO as GPIO
import time
import threading

def spi_coms():
	for i in range(0,4):
		print("thread1: ", i)
		time.sleep(0.5)


def data_handle():
	for i in range(0,4):
		print("thread2: ", i)
		time.sleep(0.5)


t1 = threading.Thread(target=spi_coms)
t2 = threading.Thread(target=data_handle)


t1.start()
t2.start()