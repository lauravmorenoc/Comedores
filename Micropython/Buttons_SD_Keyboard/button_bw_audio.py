import os
import time
from machine import Pin, SoftSPI
from wavplayer import WavPlayer


#---AUDIO CONFIG
SCK_PIN = 26 #32
WS_PIN = 22 #25
SD_PIN = 21 #33
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 5000


wp = WavPlayer(id=I2S_ID,
              sck_pin=Pin(SCK_PIN),
              ws_pin=Pin(WS_PIN),
              sd_pin=Pin(SD_PIN),
              ibuf=BUFFER_LENGTH_IN_BYTES)
#---- AUDIO CONFIG

led = Pin(27, Pin.OUT)    # 22 number in is Output
push_button = Pin(25, Pin.IN)  # 23 number pin is input
bw_button = Pin(23, Pin.IN) 
i=0
while True:
  
  logic_state = push_button.value()
  bw_logic_state= bw_button.value()
  
  if logic_state == True or bw_logic_state== True:     # if pressed the push_button
    
    if bw_logic_state == True:
        i=i-1
        print("if")
        print(i)
    else:
        i = i+1
        led.value(1)
        print("else")
        print(i)
    wp.play("turno.wav", loop= False)
    while wp.isplaying() == True: # hace que se reproduzca todo el audio 1 para luego seguir con el 2
    # other actions can be done inside this loop during playback
        pass
    num_file = str(i) + ".wav"
    if i <= 9:
        wp.play(num_file, loop= False)
        while wp.isplaying() == True: # hace que se reproduzca todo el audio 1 para luego seguir con el 2
        # other actions can be done inside this loop during playback
            pass
    elif i >= 10 and i <= 99:
        tens = i // 10
        unit = i % 10
        wp.play(str(tens) + ".wav", loop= False)
        while wp.isplaying() == True: # hace que se reproduzca todo el audio 1 para luego seguir con el 2
        # other actions can be done inside this loop during playback
            pass
        wp.play(str(unit) + ".wav", loop= False)
        while wp.isplaying() == True: # hace que se reproduzca todo el audio 1 para luego seguir con el 2
        # other actions can be done inside this loop during playback
            pass
    else:
        i=0
        
  else:                       # if push_button not pressed
    led.value(0)             # led will turn OFF

#wp.play("wav_music-16k-16bits-mono.wav", loop= False)
#while wp.isplaying() == True: # hace que se reproduzca todo el audio 1 para luego seguir con el 2
    # other actions can be done inside this loop during playback
#    pass
#wp.play("1.wav", loop= False)


