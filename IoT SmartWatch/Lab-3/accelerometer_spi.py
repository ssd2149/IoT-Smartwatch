from machine import Pin, SPI, I2C
import ustruct
import time

"""
Lab Three: ADXL 345 accelerometer SPI example
"""

global cs, vcc, grnd, spi

# Register constants for the ADXL345 accelerometer
POWER_CTL = const(0x2D)
DATA_FORMAT = const(0x31)
DATAX0 = const(0x32)
DATAX1 = const(0x33)
DATAY0 = const(0x34)
DATAY1 = const(0x35)
DATAZ0 = const(0x36)
DATAZ1 = const(0x37)

# Write to the DATA_FORMAT register to set to 4g.
# Write to POWER_CTL register to begin measurements
def setup():
    writeA(DATA_FORMAT, 0x01)
    writeA(POWER_CTL, 0x08)

# Write command/value to specified register
def writeA(register, value):
    global cs, vcc, grnd, spi

    # Pack register and value into byte format
    write_val = ustruct.pack('B',value)
    write_reg_val = ustruct.pack('B',register)

    # Pull line low and write to accelerometer
    cs.value(0)
    spi.write(write_reg_val)
    spi.write(write_val)
    cs.value(1)

# Read value from a specified register
def readA():
    global cs, vcc, grnd, spi

    # Set the R/W bit high to specify "read" mode
    reg = DATAX0
    reg = 0x80 | reg

    # Set the MB bit high to specify that we want to
    # do multi byte reads.
    reg = reg | 0x40

    # Pack R/W bit + MB bit + register value into byte format
    write_reg_val = ustruct.pack('B',reg)

    # Setup buffers for receiving data from the accelerometer.
    x1 = bytearray(1)
    x2 = bytearray(1)
    y1 = bytearray(1)
    y2 = bytearray(1)
    z1 = bytearray(1)
    z2 = bytearray(1)

    # Read from all 6 accelerometer data registers, one address at a time
    cs.value(0)
    spi.write(write_reg_val)
    spi.readinto(x1)
    spi.readinto(x2)
    spi.readinto(y1)
    spi.readinto(y2)
    spi.readinto(z1)
    spi.readinto(z2)
    cs.value(1)
    
    # Reconstruct the X, Y, Z axis readings from the received data.
    x = (ustruct.unpack('b',x2)[0]<<8) | ustruct.unpack('b',x1)[0]
    y = (ustruct.unpack('b',y2)[0]<<8) | ustruct.unpack('b',y1)[0]
    z = (ustruct.unpack('b',z2)[0]<<8) | ustruct.unpack('b',z1)[0]
    return (x,y,z)

# Main program
if(__name__ == '__main__'):

    # Setup SPI: cs = Pin13, clk = Pin5, mosi = Pin2, miso = Pin16
    cs=Pin(13, Pin.OUT)
    vcc = Pin(12, Pin.OUT)
    grnd = Pin(14 , Pin.OUT)
    vcc.value(1)
    grnd.value(0)
    spi = SPI(-1, baudrate=500000, polarity=1, phase=1, sck=Pin(5), mosi=Pin(2), miso=Pin(16))
    cs.value(0)
    cs.value(1)

    # Initialize accelerometer
    setup()

    # Sample axis registers at 2 Hz
    while True:
        x, y, z = readA()
        print("x:",x,"y:",y,"z:",z)
        time.sleep_ms(500)
