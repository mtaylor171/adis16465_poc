# libraries
import spidev
import time

spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 1000000  # Max spi speed 1MHz
spi.mode = 0b11     # spi mode 3 (CPOL = 1, CPHA = 1)

# vibration sensor class


# main script


# starting script


if __name__ == "__main__":
    while(1):
        if input("Press 1 to read SN: ") == 1:
            spi.writebytes(0x74)
            s_num = spi.readbytes(2)
            print("*SPI TEST* Serial Number: ", s_num)
    
