#!/usr/bin/env python

# libraries
from ctypes import *
import ctypes
import time
import numpy as np
import math

SO_FILE = os.path.dirname(os.path.realpath(__file__)) + "/adis16465_spi_lib.so"     # C wrapper for SPI Communication
C_FUNCTIONS = CDLL(SO_FILE)

if __name__ == "__main__":
	print("Program Started")

	while(1):
		try:
			if (input("Type 0 and press enter to start ") == "0"):
				if C_FUNCTIONS.initialize_sensor():
					print("Timed Out: Could not communcate with adis16465 within 5 seconds")
				else:
					print("Damn it works")
		except KeyboardInterrupt:
			break