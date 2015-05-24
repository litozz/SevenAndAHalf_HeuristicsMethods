#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time
#print "ALGO!"
#time.sleep(3)
#print "Han pasado 3 segundos."

class Carta(object):
	def __init__(self,palo,num):
		self.palo=palo
		self.num=num
	def __str__(self):
		palito=""
		if(self.palo==0):
			palito="espadas"
		elif(self.palo==1):
			palito="bastos"
		elif(self.palo==2):
			palito="oros"
		elif(self.palo==3):
			palito="copas"

		if(self.num+1<10):
			return "{} de {}".format(self.num+1,palito)
		else:
			numerito=""
			if(self.num+1==10):
				numerito="Sota"
			elif(self.num+1==11):
				numerito="Caballo"
			elif(self.num+1==12):
				numerito="Rey"
			return "{} de {}".format(numerito,palito)	
	def __repr__(self):
		return self.__str__()
	def getPuntuacion(self):
		if(self.num<9):
			return self.num+1
		else: 
			return 0.5 

class Baraja(object):
	def __init__(self):
		self.baraja=[]
		for i in xrange(4):
			for j in xrange(12):
				self.baraja.append(Carta(i,j))
	def getBaraja(self):
		return self.baraja
	def extractRandomCard(self):
		i=random.randint(0,self.size()-1)
		return self.baraja[i]
	def __str__(self):
		return self.baraja.__str__()
	def searchCard(self,num,palo):
		for i in xrange(len(self.baraja)):
			if(baraja[i].palo==palo and baraja[i].num==num):
				return baraja[i]
	def removeCard(self,carta):
		self.baraja.remove(carta)
	def size(self):
		return len(self.baraja)
	def getCarta(self,i):
		return self.baraja[i]
	def quitEightsAndNines(self):
		i=0;
		size=len(self.baraja)
		while(i<size):
			if(self.baraja[i].getPuntuacion()==8 or self.baraja[i].getPuntuacion()==9):
				self.baraja.remove(self.baraja[i])
				size=len(self.baraja)
			else:
				i=i+1
	def barajar(self):
		random.shuffle(self.baraja)

class JugadorIA(object):
	def __init__(self,b,puntContrario):
		self.baraja=b
		self.puntContrario=puntContrario

	def getProbabilidadPuntuacion(self,valor):
		cartasEnBaraja=0.0
		for i in xrange(self.baraja.size()):
			if(self.baraja.getCarta(i).getPuntuacion()<=valor):
				cartasEnBaraja=cartasEnBaraja+1
		return cartasEnBaraja/self.baraja.size()

	def retirarCarta(self,carta):
		self.baraja.removeCard(carta);
	
	def jugar(self):
		puntuacion=0
		opc='s'
		continuar=True
		carta=self.baraja.extractRandomCard()
		while(carta.getPuntuacion()>7):
			carta=self.baraja.extractRandomCard()
		print ("Ha salido el {} para Maquina".format(carta))
		self.retirarCarta(carta)
		puntuacion=puntuacion+carta.getPuntuacion()

		while(continuar and puntuacion<7.5):
			print("puntuacion de Maquina es: {}".format(puntuacion))
			print("Maquina, quieres otra carta?: ")
			time.sleep(random.randint(2,5)) #Esto es para dar la impresion de que IA esta pensando
			#----------------FASE DE DECISION----------------#
			if (puntuacion>self.puntContrario or self.puntContrario>7.5):
				opc='n'
			else:
				if(puntuacion<self.puntContrario):
					opc='s'
				elif(self.getProbabilidadPuntuacion(7.5-puntuacion)>0.5): #Busco la probabilidad de ganar por 7 y medio en caso de empate
					opc='s'
				else: #Busco el empate
					opc='n'
			#----------------FASE DE DECISION----------------#
			if(opc=='s' or opc=='S'):
				print("Maquina pide otra carta.")
				print("")
				carta=self.baraja.extractRandomCard()
				self.retirarCarta(carta)
				print ("Ha salido el {} para Maquina".format(carta))
				print ("")
				puntuacion=puntuacion+carta.getPuntuacion()
				continuar=True
			else:
				print("Maquina se planta.")
				continuar=False

		if puntuacion==7.5:
			print("Maquina ha sacado 7 y 1/2")
		elif puntuacion>7.5:
			print("Maquina se pasa")
		else:
			print("Maquina saca {}.".format(puntuacion))

		return puntuacion




def main():
	baraja=Baraja()
	baraja.quitEightsAndNines()
	baraja.barajar()
	continuar=True
	puntuacion=0;
	opc='s'
	
	dineroJugador=100000
	dineroMaquina=100000
	bote=0
	apuesta=0
		
	while(dineroJugador>0 and dineroMaquina>0):
		print("Jugador: {}$".format(dineroJugador))
		print("IA: {}$".format(dineroMaquina))

		print("---------TURNO DE JUGADOR---------")
		print("")
		
		apuestaCorrecta=False
		while(not apuestaCorrecta):
			apuesta=input("Jugador, ¿Cuánto apuestas?: ")
			apuesta=int(apuesta)
			if(dineroJugador>=apuesta and dineroMaquina>=apuesta and apuesta>0):
				dineroJugador=dineroJugador-apuesta;
				dineroMaquina=dineroMaquina-apuesta;
				bote=bote+apuesta*2;
				apuestaCorrecta=True
			else:
				apuestaCorrecta=False
				print("Apuesta menor o igual que tu máximo o el de la maquina")

		carta=baraja.extractRandomCard()
		while(carta.getPuntuacion()>7):
			carta=baraja.extractRandomCard()
		print ("Ha salido el {}".format(carta))
		puntuacion=puntuacion+carta.getPuntuacion()
		while(continuar and puntuacion<7.5):
			print("Tu puntuacion es: {}".format(puntuacion))
			opc=raw_input("Quieres otra carta?: ")
			if(opc=='s' or opc=='S'):
				print("Jugador pide otra carta.")
				print("")
				carta=baraja.extractRandomCard()
				print ("Ha salido el {}".format(carta))
				print("")
				puntuacion=puntuacion+carta.getPuntuacion()
				continuar=True
			else:
				continuar=False

		if puntuacion==7.5:
			print("Jugador saca 7 y 1/2")
		elif puntuacion>7.5:
			print("Jugador se pasa.")
		else:
			print("Jugador saca {}.".format(puntuacion))

		print("---------TURNO DE JUGADOR IA---------")
		print("")
		jugadorIA=JugadorIA(baraja,puntuacion)
		puntuacionIA=jugadorIA.jugar()


		if(puntuacionIA>7.5):
			if(puntuacion<=7.5):
				print("GANA JUGADOR")
				dineroJugador=dineroJugador+bote
				bote=0
			else:
				print("AMBOS JUGADORES SE PASAN. EL BOTE ES DE: {}$".format(bote))

		else:
			if(puntuacion>7.5 or puntuacionIA>puntuacion):
				print("GANA IA")
				dineroMaquina=dineroMaquina+bote
				bote=0
			elif(puntuacion>puntuacionIA):
				print("GANA JUGADOR")
				dineroJugador=dineroJugador+bote
				bote=0
			else:
				print("EMPATE. BOTE PARA LA BANCA")
				dineroMaquina=dineroMaquina+bote
				bote=0
		#Reinicialización en cada mano.
		apuesta=0
		puntuacion=0
		continuar=True
		opc='s'

	if(dineroMaquina>dineroJugador):
		print ("La banca se ha llevado tu pasta. ¡PAQUETE!")
	else:
		print ("Has arruinado a la banca. ¡Enhorabuena!")

if __name__=="__main__":
	main()