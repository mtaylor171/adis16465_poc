/**
 * 	Change the #include to use the Serial Peripheral Diver header.
 */
#include <bcm2835.h>

/**
 * Define the number of bytes in a standard word for the
 * SPI device used.
 */
#define SPI_WORD_BYTES				1U		/* Number of bytes in SPI word for device */

// User Register Memory Map from Table 6
#define DIAG_STAT      0x02  //Diagnostic and operational status
#define X_GYRO_LOW     0x04  //X-axis gyroscope output, lower word
#define X_GYRO_OUT     0x06  //X-axis gyroscope output, upper word
#define Y_GYRO_LOW     0x08  //Y-axis gyroscope output, lower word
#define Y_GYRO_OUT     0x0A  //Y-axis gyroscope output, upper word
#define Z_GYRO_LOW     0x0C  //Z-axis gyroscope output, lower word
#define Z_GYRO_OUT     0x0E  //Z-axis gyroscope output, upper word
#define X_ACCL_LOW     0x10  //X-axis accelerometer output, lower word
#define X_ACCL_OUT     0x12  //X-axis accelerometer output, upper word
#define Y_ACCL_LOW     0x14  //Y-axis accelerometer output, lower word
#define Y_ACCL_OUT     0x16  //Y-axis accelerometer output, upper word
#define Z_ACCL_LOW     0x18  //Z-axis accelerometer output, lower word
#define Z_ACCL_OUT     0x1A  //Z-axis accelerometer output, upper word
#define TEMP_OUT       0x1C  //Temperature output (internal, not calibrated)
#define TIME_STAMP     0x1E  //PPS mode time stamp
#define X_DELTANG_LOW  0x24  //X-axis delta angle output, lower word
#define X_DELTANG_OUT  0x26  //X-axis delta angle output, upper word
#define Y_DELTANG_LOW  0x28  //Y-axis delta angle output, lower word
#define Y_DELTANG_OUT  0x2A  //Y-axis delta angle output, upper word
#define Z_DELTANG_LOW  0x2C  //Z-axis delta angle output, lower word
#define Z_DELTANG_OUT  0x2E  //Z-axis delta angle output, upper word
#define X_DELTVEL_LOW  0x30  //X-axis delta velocity output, lower word
#define X_DELTVEL_OUT  0x32  //X-axis delta velocity output, upper word
#define Y_DELTVEL_LOW  0x34  //Y-axis delta velocity output, lower word
#define Y_DELTVEL_OUT  0x36  //Y-axis delta velocity output, upper word
#define Z_DELTVEL_LOW  0x38  //Z-axis delta velocity output, lower word
#define Z_DELTVEL_OUT  0x3A  //Z-axis delta velocity output, upper word
#define XG_BIAS_LOW    0x40  //X-axis gyroscope bias offset correction, lower word
#define XG_BIAS_HIGH   0x42  //X-axis gyroscope bias offset correction, upper word
#define YG_BIAS_LOW    0x44  //Y-axis gyroscope bias offset correction, lower word
#define YG_BIAS_HIGH   0x46  //Y-axis gyroscope bias offset correction, upper word
#define ZG_BIAS_LOW    0x48  //Z-axis gyroscope bias offset correction, lower word
#define ZG_BIAS_HIGH   0x4A  //Z-axis gyroscope bias offset correction, upper word
#define XA_BIAS_LOW    0x4C  //X-axis accelerometer bias offset correction, lower word
#define XA_BIAS_HIGH   0x4E  //X-axis accelerometer bias offset correction, upper word
#define YA_BIAS_LOW    0x50  //Y-axis accelerometer bias offset correction, lower word
#define YA_BIAS_HIGH   0x52  //Y-axis accelerometer bias offset correction, upper word
#define ZA_BIAS_LOW    0x54  //Z-axis accelerometer bias offset correction, lower word
#define ZA_BIAS_HIGH   0x56  //Z-axis accelerometer bias offset correction, upper word
#define FILT_CTRL      0x5C  //Filter control
#define RANG_MDL       0x5E  //Measurement range indentifier
#define MSC_CTRL       0x60  //Miscellaneous control
#define UP_SCALE       0x62  //Clock scale factor, PPS mode
#define DEC_RATE       0x64  //Decimation rate control (output data rate)
#define NULL_CFG       0x66  //Auto-null configuration control
#define GLOB_CMD       0x68  //Global commands
#define FIRM_REV       0x6C  //Firmware revision
#define FIRM_DM        0x6E  //Firmware revision date, month and day
#define FIRM_Y         0x70  //Firmware revision date, year
#define PROD_ID        0x72  //Product identification
#define SERIAL_NUM     0x74  //Serial number (relative to assembly lot)
#define USER_SCR1      0x76  //User scratch register 1
#define USER_SCR2      0x78  //User scratch register 2
#define USER_SCR3      0x7A  //User scratch register 3
#define FLSHCNT_LOW    0x7C  //Flash update count, lower word
#define FLSHCNT_HIGH   0x7E  //Flash update count, upper word

/*
uint16_t adis16465_reg_arr[14][2] = {

};
*/


/**
 * Other useful macros
 */
#define	SHORT_DELAY	10		/* Delay used to let device do it's thing */
#define LONG_DELAY	50		/* Longer delay to give it more time */

#define CHANNEL0			BCM2835_SPI_CS0
#define	CHANNEL1			BCM2835_SPI_CS1

char spiOut[2]; 			/* SPI output buffer */
char spiIn[2];	 			/* SPI input buffer  */

uint16_t mV;					/* millivolts */
uint16_t result;				/* result */
uint8_t digitalOutPins = 0x00;	/* Bit mask of pins currently set as digital out */
uint8_t digitalInPins = 0x00;	/* Bit mask of pins currently set as digital in */
uint8_t analogOutPins = 0x00;	/* Bit mask of pins currently set as analog out */
uint8_t analogInPins = 0x00;	/* Bit mask of pins currently set as analog in */

typedef unsigned short int	AD16465_WORD;

/**
 * Clear the spi buffer.
 * Parameters:
 * 	spiBuffer[] = spi buffer
 */
void clearBuffer(char spiBuffer[]);

/**
 * Parse the 16 bit word of the AD5592 into two 8 bit chunks that
 * works with the bcm2835 library.
 * Parameters:
 * 	eightBits[] = spi buffer
 * 	sixteenBits = AD5592 spi word
 */
void makeWord(char eightBits[], AD16465_WORD sixteenBits);

/**
 * Select the SPI channel.
 * Parameters:
 * 	ch = channel number
 */
void setADIS16465Ch(int ch);

/**
 * Set pins to digital outputs.
 * Parameter: Pins as bit mask
 */

void spiComs(AD16465_WORD command);

/**
 * Set a pin to high or low output.
 * Parameters:
 * 	Pins to output as bit mask
 * 	State to be output as bit mask
 */


uint32_t elapsed_time();

/**
 * Initialize the SPI for using the AD5592. Does not set channel. Do that
 * after calling this function by calling setAD5592Ch().
 * Parameters:
 * 	none
 */
void ADIS16465_Init();

int initialize_sensor();

#endif /* SOURCES_AD5592RPI_H_ */

/* Main Program */

#include <stdio.h>
#include <sys/time.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

struct timeval st, et;

uint32_t elapsed_time(){
	uint32_t elapsed = ((et.tv_sec - st.tv_sec) * 1000000) + (et.tv_usec - st.tv_usec);
	return elapsed;
}

/**
 * Clear the spi buffer.
 * Parameters:
 * 	spiBuffer[] = spi buffer
 */

void clearBuffer(char spiBuffer[])
{
	int i;
	for(i=0;i<strlen(spiBuffer);i++)
	{
		spiBuffer[i] = 0x00;
	}
}

int initialize_sensor(){
	int spi_timeout_counter = 0;
	ADIS16465_Init();
	setADIS16465Ch(0);
	bcm2835_delay(10);
	spiComs(0xE880);	// SW reset
	bcm2835_delay(100);
	spiComs(0xE900);	// Begin sampling
	bcm2835_delay(100);
	spiComs(PROD_ID << 8);
	spiComs(0x0000);
	bcm2835_delay(10);
	while((spiIn[0] != 0x40) && (spiIn[1] != 0x51)){
		spiComs(PROD_ID << 8);
		spiComs(0x0000);
		bcm2835_delay(100);
		spi_timeout_counter ++;
		if(spi_timeout_counter >= 50){
			return 1;		//Timeout after 5 seconds of trying
	}
	return 0;
}

/**
 * Parse the 16 bit word of the ADIS16465 into two 8 bit chunks that
 * works with the bcm2835 library.
 * Parameters:
 * 	eightBits[] = spi buffer
 * 	sixteenBits = ADIS16465 spi word
 */

void makeWord(char eightBits[], AD16465_WORD sixteenBits)
{
	clearBuffer(eightBits);
	eightBits[0] = (sixteenBits & 0xFF00) >> 8;
	eightBits[1] = sixteenBits & 0xFF;
}

/**
 * Select the SPI channel.
 * Parameters:
 * 	ch = channel number
 */
void setADIS16465Ch(int ch)
{
	switch(ch){
		case 0:
			bcm2835_spi_chipSelect(CHANNEL0);
			bcm2835_spi_setChipSelectPolarity(CHANNEL0, LOW);
			break;
		case 1:
			bcm2835_spi_chipSelect(CHANNEL1);
			bcm2835_spi_setChipSelectPolarity(CHANNEL1, LOW);
			break;
	}
}

/**
 * SPI communications
 * Parameter:
 * 	Command to send.
 */
void spiComs(AD16465_WORD command)
{
	makeWord(spiOut, command);
	clearBuffer(spiIn);
	bcm2835_spi_transfernb(spiOut, spiIn, sizeof(spiOut));
}

/**
 * Initialize the SPI for using the ADIS16465. Does not set channel. Do that
 * after calling this function by calling setADIS16465Ch.
 * Parameters:
 * 	none
 */
void ADIS16465_Init()
{
	//int msg;
	/* Initialize the bcm2835 library */
	bcm2835_init();

    /* Initialize the SPI module */
    bcm2835_spi_begin();

    /* Set SPI bit order */
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);      // The default

    /* Set SPI polarity and phase */
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE3);                   // Mode 1

    /* Set SPI clock */
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_1024); 	  // 700MHz / 1024 = 684kHz (Check Pi Zero CPU Speed: https://low-orbit.net/raspberry-pi-how-to-check-cpu-speed)
}
