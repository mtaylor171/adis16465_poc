#!/usr/bin/env python

# libraries
import spidev
import RPi.GPIO as GPIO
import time
from threading import Thread, Event
import numpy as np

spi = spidev.SpiDev()

# User Register Memory Map from Table 6
DIAG_STAT=      0x02  #Diagnostic and operational status
X_GYRO_LOW=     0x04  #X-axis gyroscope output, lower word
X_GYRO_OUT=     0x06  #X-axis gyroscope output, upper word
Y_GYRO_LOW=     0x08  #Y-axis gyroscope output, lower word
Y_GYRO_OUT=     0x0A  #Y-axis gyroscope output, upper word
Z_GYRO_LOW=     0x0C  #Z-axis gyroscope output, lower word
Z_GYRO_OUT=     0x0E  #Z-axis gyroscope output, upper word
X_ACCL_LOW=     0x10  #X-axis accelerometer output, lower word
X_ACCL_OUT=     0x12  #X-axis accelerometer output, upper word
Y_ACCL_LOW=     0x14  #Y-axis accelerometer output, lower word
Y_ACCL_OUT=     0x16  #Y-axis accelerometer output, upper word
Z_ACCL_LOW=     0x18  #Z-axis accelerometer output, lower word
Z_ACCL_OUT=     0x1A  #Z-axis accelerometer output, upper word
TEMP_OUT=       0x1C  #Temperature output (internal, not calibrated)
TIME_STAMP=     0x1E  #PPS mode time stamp
X_DELTANG_LOW=  0x24  #X-axis delta angle output, lower word
X_DELTANG_OUT=  0x26  #X-axis delta angle output, upper word
Y_DELTANG_LOW=  0x28  #Y-axis delta angle output, lower word
Y_DELTANG_OUT=  0x2A  #Y-axis delta angle output, upper word
Z_DELTANG_LOW=  0x2C  #Z-axis delta angle output, lower word
Z_DELTANG_OUT=  0x2E  #Z-axis delta angle output, upper word
X_DELTVEL_LOW=  0x30  #X-axis delta velocity output, lower word
X_DELTVEL_OUT=  0x32  #X-axis delta velocity output, upper word
Y_DELTVEL_LOW=  0x34  #Y-axis delta velocity output, lower word
Y_DELTVEL_OUT=  0x36  #Y-axis delta velocity output, upper word
Z_DELTVEL_LOW=  0x38  #Z-axis delta velocity output, lower word
Z_DELTVEL_OUT=  0x3A  #Z-axis delta velocity output, upper word
XG_BIAS_LOW=    0x40  #X-axis gyroscope bias offset correction, lower word
XG_BIAS_HIGH=   0x42  #X-axis gyroscope bias offset correction, upper word
YG_BIAS_LOW=    0x44  #Y-axis gyroscope bias offset correction, lower word
YG_BIAS_HIGH=   0x46  #Y-axis gyroscope bias offset correction, upper word
ZG_BIAS_LOW=    0x48  #Z-axis gyroscope bias offset correction, lower word
ZG_BIAS_HIGH=   0x4A  #Z-axis gyroscope bias offset correction, upper word
XA_BIAS_LOW=    0x4C  #X-axis accelerometer bias offset correction, lower word
XA_BIAS_HIGH=   0x4E  #X-axis accelerometer bias offset correction, upper word
YA_BIAS_LOW=    0x50  #Y-axis accelerometer bias offset correction, lower word
YA_BIAS_HIGH=   0x52  #Y-axis accelerometer bias offset correction, upper word
ZA_BIAS_LOW=    0x54  #Z-axis accelerometer bias offset correction, lower word
ZA_BIAS_HIGH=   0x56  #Z-axis accelerometer bias offset correction, upper word
FILT_CTRL=      0x5C  #Filter control
RANG_MDL=       0x5E  #Measurement range indentifier
MSC_CTRL=       0x60  #Miscellaneous control
UP_SCALE=       0x62  #Clock scale factor, PPS mode
DEC_RATE=       0x64  #Decimation rate control (output data rate)
NULL_CFG=       0x66  #Auto-null configuration control
GLOB_CMD=       0x68  #Global commands
FIRM_REV=       0x6C  #Firmware revision
FIRM_DM=        0x6E  #Firmware revision date, month and day
FIRM_Y=         0x70  #Firmware revision date, year
PROD_ID=        0x72  #Product identification 
SERIAL_NUM=     0x74  #Serial number (relative to assembly lot)
USER_SCR1=      0x76  #User scratch register 1 
USER_SCR2=      0x78  #User scratch register 2 
USER_SCR3=      0x7A  #User scratch register 3 
FLSHCNT_LOW=    0x7C  #Flash update count, lower word 
FLSHCNT_HIGH=   0x7E  #Flash update count, upper word 

def spi_write_reg(reg, command, r_w):
	spi_word0 = reg | (r_w << 7)        # adding write bit if necessary
	spi_word1 = command
	spi_words = [spi_word0, spi_word1]
	spi.writebytes(spi_words)

def spi_read_reg(n):
	spi_recv = [0x00, 0x00]
	spi_recv = spi.readbytes(n)
	return spi_recv
	# Possibly add bytes into an array here, then return

def BytesToHex(Bytes):
	return ''.join(["0x%02X " % x for x in Bytes]).strip() 

def adis16465_setup():
	spi.open(0, 0)
	spi.max_speed_hz = 1000000  # Max spi speed 1MHz
	spi.mode = 0b11     # spi mode 3 (CPOL = 1, CPHA = 1)
	spi.lsbfirst = False
	time.sleep(.5)  # give everything time to start up

	#spi_write_reg(MSC_CTRL, 0xC1, 1)   # enable data ready, set polarity
	#spi_read_reg(2)

# vibration sensor class


# main script
'''
	Send burst read command
	Read data read, receive all packets
	Handle checksum

	Store data on flash (or upload to database)
	Display on terminal?

	Clear data on local storage

'''


# starting script


if __name__ == "__main__":
	print("Progarm Started")
	adis16465_setup()
	while(1):
		try:
			data_str = input("Enter SPI signal: ")
			data_int = int(data_str, 16)
			data = hex(data_int)
			print("hex data:", type(data))
			spi.writebytes([(data & 0xFF), (data >> 4)])
			time.sleep(0.5)
			s_num = spi_read_reg(4)
			print("*SPI TEST* Serial Number: ", BytesToHex(s_num))
		except KeyboardInterrupt:
			spi.close()
			break


'''
	while(1):
		try:
			if input("Press 1 to read SN: ") == "1":
				#spi_write_reg(PROD_ID, 0x00, 0)
				spi.writebytes([0x72, 0x00])
				time.sleep(0.5)
				s_num = spi_read_reg(4)
				print("*SPI TEST* Serial Number: ", BytesToHex(s_num))
		except KeyboardInterrupt:
			spi.close()
			break
'''	
