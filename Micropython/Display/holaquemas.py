from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
from machine import SoftSPI
import time


#spi = SPI(1, baudrate=10000000, sck=Pin(18), mosi=Pin(23))
#display = Display(spi, dc=Pin(4), cs=Pin(22), rst=Pin(15))

sckd = Pin(18, Pin.OUT)
mosid = Pin(23, Pin.OUT)
misod = Pin(19, Pin.OUT)
spid = SoftSPI(baudrate=10000000, polarity=0, phase=0, sck=sckd, mosi=mosid, miso=misod)
display = Display(spid, dc=Pin(4), cs=Pin(15), rst=Pin(22))
broadway = XglcdFont('fonts/Broadway17x15.c', 17, 15)
    
display.clear(color565(204, 53, 94)) # color de fondo en RGB de 24 bits
display.draw_text(55, 90, 'Hola', broadway, color565(255, 255, 255), color565(204, 53, 94))# x, y, texto, fuente, color de letra, color de fondo de letra
display.draw_text(110, 120, 'que', broadway, color565(255, 255, 255), color565(204, 53, 94))
display.draw_text(75, 150, 'mas', broadway, color565(255, 255, 255), color565(204, 53, 94))
    
#sleep(20)
time.sleep(20)
display.cleanup()
display.reset_mpy()