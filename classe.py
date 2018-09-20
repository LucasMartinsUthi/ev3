#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
import math
from time import sleep

class Robot():

	def __init__(self, motorD, motorE, garra, sensorD, sensorE, sensorM, R, r):
		# Motores
		self.motorD = LargeMotor('out' + motorD)
		self.motorE = LargeMotor('out' + motorE)
		self.motorG = MediumMotor('out' + garra)
		# Sensores de Cor
		self.sensorD = ColorSensor('in' + sensorD)
		self.sensorD.mode = 'COL-COLOR'
		self.sensorE = ColorSensor('in' + sensorE)
		self.sensorE.mode = 'COL-COLOR'
		self.sensorU = UltrasonicSensor('in' + sensorM)
		assert self.sensorU.connected
		# Odometria
		self.sensorU.mode = 'US-DIST-CM'
		self.razao = self.odometria(R, r)
		# Variaveis
		self.corAtual = None

	def detecta(self):
		if(self.sensorU.value() < 100):
			return True
		else:
			return False

	def odometria(self, R, r):
		C = 2*math.pi*R
		c = 2*math.pi*r

		return C/c

	def girar(self, g):
		girar = self.razao*g
		self.andarRotacao(girar,-girar,200)
		self.motorD.wait_while('running')

	def abreGarra(self, rotation, speed):
		self.motorG.run_to_rel_pos(position_sp=rotation, speed_sp=speed, stop_action="coast")
		self.motorG.wait_while('running')
		self.stop()
		return True

	def fechaGarra(self, speed):
		self.motorG.run_forever(speed_sp=speed)
		self.motorG.stop(stop_action='coast')
		return True

	def andarTempo(self, speed, speed2, time, wait = False):
		self.motorD.run_timed(time_sp = time, speed_sp = speed)
		self.motorE.run_timed(time_sp = time, speed_sp = speed2)
		if wait:
			sleep(time/1000)
		return True

	def andarRotacao(self, rotation, rotation2, speed, wait = False):
		self.motorD.run_to_rel_pos(position_sp=rotation, speed_sp=speed, stop_action="hold")
		self.motorE.run_to_rel_pos(position_sp=rotation2, speed_sp=speed, stop_action="hold")
		if wait:
			sleep(time/1000)

	def stop(self):
		self.motorD.stop()
		self.motorE.stop()
		return True

	def ruido(self, cores, sensor):
		ruido = 0
		for i in range(0, 80):
			if 0 <= i < 20 or 40 < i < 60:
				self.andarTempo(150, 150, 100)
				if sensor.value() in cores:
					ruido += 1
					continue
			self.andarTempo(-150, -150, 100)
			if sensor.value() in cores:
					ruido += 1

		print(ruido)
		if ruido > 56:
			return True

	def saindoPista(self):
		if self.sensorE.value() in [0,1,7]:
			if self.ruido([0,1,7], self.sensorE):
				self.andarTempo(-200, -200, 800, True)
				self.andarTempo(0, 200, 600, True)
				self.andarTempo(200, 200, 600, True)
				return True

		if self.sensorD.value() in [0,1,7]:
			if self.ruido([0,1,7], self.sensorD):
				self.andarTempo(-200, -200, 800, True)
				self.andarTempo(200, 0, 600, True)
				self.andarTempo(200, 200, 600, True)
				return True
		self.andarTempo(200, 200, 500)
		return False

	def alinhaCor(self, cor, sensorEntrada, sensorAjuste, velocidadeMotorEntrada, velocidadeMotorAjuste):
		self.corAtual = cor #Verificar essa cor com o sensor do meio

		if self.ruido([cor], sensorEntrada):
			while sensorAjuste.value() != cor:
				self.andarTempo(velocidadeMotorEntrada, velocidadeMotorAjuste, 100)
				if self.saindoPista():
					break

		if cor == 6:
			self.corAtual = None
			
		return True
#
# mB.stop()
# mC.stop()