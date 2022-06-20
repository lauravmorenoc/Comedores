from MQTTconnection import *
from mainMQTT import Communications
from displayLib import MyDisplay
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
from machine import SoftSPI
import math

sck=22
mosi=19
miso=23

spi=SoftSPI(baudrate=1000000, polarity=0, phase=0, sck=Pin(sck, Pin.OUT), mosi=Pin(mosi, Pin.OUT), miso=Pin(miso, Pin.OUT))
disp=MyDisplay(spi)
disp.printLogo()
disp.printText('Ticket: ', vspace=1, hspace=8)

COMM=Communications()

sim_ticket=0

last_publish_time = 0
message_interval = 1 # in seconds
refresh = True

while True:    
    
    try:
        if (time.time() - last_publish_time) > message_interval:
            if refresh:
                #COMM.send(topic='SI/Petition')
                COMM.send(topic='Easymeals/Update', ticket=sim_ticket)
                refresh = False
                sim_ticket+=1
            else:
                refresh = True
            last_publish_time = time.time()
    except OSError as e:
        print('Unable to connect. Please restart device.')
    
    
    # Receive messages
    topic, message, pending_incoming_message=COMM.receive()
    if pending_incoming_message==True:
        if str(topic,'utf-8')=='Easymeals/Payment':
            Name=message["Name"]
            Rol=message["Rol"]
            disp.printText('Name:', vspace=5, hspace=1)
            disp.printText(Name, vspace=6, hspace=1)
            disp.printText('Rol:', vspace=8, hspace=1)
            disp.printText(Rol, vspace=9, hspace=1)
            # Cuando se actualice el turno borrar nombre de persona y poner "bienvenido"
            if Rol=='Student':
                Payment=5900 
            else:
                Payment=7900 # Cambiar si incorrecto
            disp.printText('Total amount to pay: ', vspace=11, hspace=1)
            disp.printText('$'+str(Payment), vspace=12, hspace=8)
            COMM.pending_incoming_message=False
        elif str(topic,'utf-8')=='Easymeals/Update':
            ticket=message["ticket"]
            disp.printText('    ', vspace=3, hspace=11)
            disp.printText(str(ticket), vspace=3, hspace=11)
            
            # Delete last users'data from display
            disp.printText('      ', vspace=5, hspace=1)
            disp.printText('                     ', vspace=6, hspace=1)
            disp.printText('    ', vspace=8, hspace=1)
            disp.printText('    Welcome', vspace=9, hspace=1)
            disp.printText('                     ', vspace=11, hspace=1)
            disp.printText('     ', vspace=12, hspace=8)
            
            # Poner aquí función de que se reproduzca en audio
            
        
    # Sent messages