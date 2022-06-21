from MQTTconnection import *
from mainMQTT import Communications
from displayLib import MyDisplay
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
from machine import SoftSPI
from wavplayer import WavPlayer
import math
import os


sck=12
mosi=19
miso=23

spi=SoftSPI(baudrate=1000000, polarity=0, phase=0, sck=Pin(sck, Pin.OUT), mosi=Pin(mosi, Pin.OUT), miso=Pin(miso, Pin.OUT))
disp=MyDisplay(spi)
disp.printLogo()
disp.printText('Ticket: ', vspace=1, hspace=8)

COMM=Communications()

sim_ticket=0

last_publish_time = 0
message_interval = 2 # in seconds
refresh = True
comedor=1
cash_register_on=False
ID=''
IDcounter=0

SCK_PIN = 26 #32
WS_PIN = 22 #25
SD_PIN = 21 #33
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 5000
global local_ticket
local_ticket=0
last_ticket=0

wp = WavPlayer(id=I2S_ID,
              sck_pin=Pin(SCK_PIN),
              ws_pin=Pin(WS_PIN),
              sd_pin=Pin(SD_PIN),
              ibuf=BUFFER_LENGTH_IN_BYTES)
#---- AUDIO CONFIG

push_button = Pin(25, Pin.IN)  # 23 number pin is input
bw_button = Pin(23, Pin.IN) 

def char_type(char):
    if char=='1' or char=='2' or char=='3' or char=='4' or char=='5' or char=='6' or char=='7' or char=='8' or char=='9' or char=='0':
        return 'Number'
    elif char=='A': #Asterisco
        return 'Ast'
    elif char=='B': #Numeral
        return 'Sharp'
    
def button_verify():
    
    global local_ticket

    logic_state = push_button.value()
    bw_logic_state= bw_button.value()
  
    if logic_state == True or bw_logic_state== True:     # if pressed the push_button
    
        if bw_logic_state == True:
            local_ticket=local_ticket-1
            print("if")
            print(local_ticket)
        else:
            local_ticket = local_ticket+1
            print("else")
            print(local_ticket)
    

while True:    
    
    try:
        COMM.send(topic='Easymeals/Update', ticket=10, comedor=1)
    except OSError as e:
        print('OSError: Unable to sent anything')
    
    #COMM.check_message()
    #### Función para simular avance de turnos, se puede quitar
    '''
    try:
        if (time.time() - last_publish_time) > message_interval:
            if refresh:
                #COMM.send(topic='SI/Petition')
                COMM.send(topic='Easymeals/Update', ticket=sim_ticket, comedor=comedor)
                #COMM.send(topic='TEMPERATURE')
                refresh = False
                sim_ticket+=1
            else:
                refresh = True
            last_publish_time = time.time()
    except OSError as e:
        print('Unable to connect. Please restart device.')
    '''
    ####

# Send messages

    button_verify()
    if local_ticket!=last_ticket:
        try:
            COMM.send(topic='Easymeals/Update', ticket=local_ticket, comedor=comedor)
        except OSError as e:
            print('OSError: Unable to sent ticket update. Please restart device.')
        last_ticket=local_ticket
        
    
# Receive messages
    topic, message, pending_incoming_message=COMM.receive()
    if pending_incoming_message==True:
        if str(topic,'utf-8')=='Easymeals/Payment':
            if message["Registered"]:
                Name=message["Name"]
                Rol=message["Rol"]
                disp.printText('Name:', vspace=5, hspace=1)
                disp.printText(Name, vspace=6, hspace=1)
                disp.printText('Rol:', vspace=8, hspace=1)
                disp.printText(Rol, vspace=9, hspace=1)
                if Rol=='Student':
                    Payment=5900 
                else:
                    Payment=7900 # Cambiar si incorrecto
                disp.printText('Total amount to pay: ', vspace=11, hspace=1)
                disp.printText('$'+str(Payment), vspace=12, hspace=8)
                cash_register_on=True
            else:
                disp.printText('User not registered', vspace=5, hspace=3)
                cash_register_on=False
        elif str(topic,'utf-8')=='Easymeals/Update':
            if message["Comedor"]==comedor:
                ticket=message["ticket"]
                disp.printText('    ', vspace=3, hspace=11)
                disp.printText(str(ticket), vspace=3, hspace=11)
                cash_register_on=False
                
                
                wp.play("turno.wav", loop= False)
                done_deleting=False
                print('Indicador')
                while wp.isplaying() == True:
                    pass
                
                disp.printText('      ', vspace=5, hspace=1)
                disp.printText('                     ', vspace=6, hspace=1)
                disp.printText('Digite su numero de identificacion:', vspace=8, hspace=1)
                disp.printText('            ', vspace=9, hspace=1)
                disp.printText('                     ', vspace=11, hspace=1)
                disp.printText('     ', vspace=12, hspace=8)
                
                num_file = str(ticket) + ".wav"
                
                if ticket <= 9:
                    wp.play(num_file, loop= False)
                    while wp.isplaying() == True: 
                        pass
                elif ticket >= 10 and ticket <= 99:
                    tens = ticket // 10
                    unit = ticket % 10
                    wp.play(str(tens) + ".wav", loop= False)
                    while wp.isplaying() == True:
                        pass
                    wp.play(str(unit) + ".wav", loop= False)
                    while wp.isplaying() == True: 
                        pass
            
        COMM.pending_incoming_message=False    
            
        
    # Send messages
    
    
    
    # La función de Juan debe tener un print. Cambiar ese print por, considerando 'out' lo que se imprime:

'''
    if !cash_register_on: # Awaiting to get key from keyboard
        if char_type(out) =='Number':
            disp.printText(out,vspace=9, hspace=IDcounter)
            ID=ID+out
            IDcounter+=1

        elif char_type(out) =='Ast':
            disp.printText(' ' ,vspace=9, hspace=IDcounter-1)
            ID=ID[0:len(ID)-1] # verificar
            IDcounter-=1

        elif char_type(out) =='Sharp':
            try:
                COMM.send(topic='Easymeals/Payment', userID=ID)
                print('Sending ID to SI')
                cash_register_on=True
            except OSError as e:
                print('OSError: Unable to send ID')
'''
