#!/usr/bin/env python3
from time import sleep
from classe import Robot

r = Robot('A', 'B','C', '1', '3', '4', 7.65, 2.7)
cores = ['unknown','black','blue','green','yellow','red','white','brown']
# [cores[r.sensorE.value()], cores[r.sensorD.value()]]
stop = False
corAtual = None

while True:
	if not stop:
		r.andarTempo(200, 200, 100)
	print([cores[r.sensorE.value()], cores[r.sensorD.value()]], corAtual)

	r.saindoPista()

	# Achou Cor
	if r.sensorE.value() not in [0, 1, 6, 7, r.corAtual]:
		while not r.alinhaCor(r.sensorE.value(), r.sensorE, r.sensorD, 200, 0):
			continue
		r.andarTempo(200, 200, 500,True)
		r.girar(150)
		r.andarTempo(200, 200, 500,True)

	if r.sensorD.value() not in [0, 1, 6, 7, r.corAtual]:
		while not r.alinhaCor(r.sensorD.value(), r.sensorD, r.sensorE, 0, 200):
			continue
		r.andarTempo(200, 200, 500,True)
		r.girar(150)
		r.andarTempo(200, 200, 500,True)

	# Retorna Branco
	if r.sensorE.value() == 6 and r.corAtual != None:
		while not r.alinhaCor(6, r.sensorE, r.sensorD, 200, 0):
			continue

	if r.sensorD.value() == 6 and r.corAtual != None:
		while not r.alinhaCor(6, r.sensorD, r.sensorE, 0, 200):
			continue


# alinha cor
# verifa com o sensor do meio (HSL)
# RGB para HSL
# aprendendoCor  = True
# direcoes [-90, 0, 90]
# Cores [1, 2, 4]
# intelignecia = {}
# Verifica Dead end



# anda
# na cai
# acha cor gira

