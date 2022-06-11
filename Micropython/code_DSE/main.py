import machine
from communications import Communications
from displayLib import MyDisplay

currentTicket = 0

commObject = Communications()
dspObject = Display()

if __name__ = __main__: #Aquí comienza el programa

	while True:
		newTicket = commObject.getTicket()
		if (currentTicket =! newTicket):
			dspObject.updateTicket(newTicket)
			soundObject.playNextTurn()
			currentTicket = newTicket
