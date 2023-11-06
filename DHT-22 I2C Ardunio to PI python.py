#!/usr/bin/python3

from smbus2 import SMBus
import time
import requests

# Define some device parameters
I2C_ADDR = 0x27     # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 20      # Maximum characters per line

# Define some device constants
LCD_CHR = 1     # Mode - Sending data
LCD_CMD = 0     # Mode - Sending command

LCD_LINE_1 = 0x80   # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0   # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94   # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4   # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On

ENABLE = 0b00000100     # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = SMBus(1)    # Rev 2 Pi uses 1

def writeNumber(value):
    bus.write_byte(slave_address, value)

def readNumber():
   number = bus.read_byte(slave_address) ### This works.
   block_data = bus.read_i2c_block_data(slave_address, 0, 32)
   return number, block_data


def ConvertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)     # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)     # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)     # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)     # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)     # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)     # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)
addr = 0x8
bus = SMBus(1)
i2c_cmd = 0x01
numb = 1
slave_address = 0x08

if __name__ == '__main__':
    lcd_init()
    print("Type In data to send")
    while numb ==1:
        writeNumber(3) #Blink the Arduino LED this many times. ### This works.
        time.sleep(1/100)
        print("from Read: ")
        data1 = readNumber()
        #print(data1)
        incomingdata = ''.join([chr(x) for x in data1[1]])
        print(incomingdata)
        datasplit=incomingdata.split(":")
        print(incomingdata[1])
        tempf=(float(datasplit[1])*2+30)
        print(datasplit)
        humid = str(datasplit[2])
        lcd_string("Temp:" + str(tempf),1)
        lcd_string("Humid:" + str(humid),2)
        time.sleep(10)
        urlstring="https://elect144.com/a2.php?sensorlocation=GC&sensortype=DHT22&temp=" + str(tempf) + "&humidity=" + str(humid)
        print(urlstring)
        response=requests.get(urlstring)
        print(response)
        time.sleep(20)
        #bytesToSend = ConvertStringToBytes(Data)
        #bus.write_i2c_block_data(addr, i2c_cmd, bytesToSend)
            #    Data = input(">>>>>>   ")
    #    if Data == "light off":
    #        i2c_cmd = 0x01
    #    elif Data == "light on":
    #        i2c_cmd = 0x02
    #        lcd_string("Light ON")
    #    writeNumber(3) #Blink the Arduino LED this many times. ### This works.
