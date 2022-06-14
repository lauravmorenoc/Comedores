from displayLib import MyDisplay
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
from machine import SoftSPI
import math
import time

sck=22
mosi=19
miso=23

spi=SoftSPI(baudrate=1000000, polarity=0, phase=0, sck=Pin(sck, Pin.OUT), mosi=Pin(mosi, Pin.OUT), miso=Pin(miso, Pin.OUT))
disp=MyDisplay(spi)
disp.printLogo()
disp.printText('UN Campus', vspace=1, hspace=8)