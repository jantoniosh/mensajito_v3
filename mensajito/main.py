# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# mensajito -- Main Program
# mensajito.mx
# Idea Original : Diego Aguirre
# Código: Antonio Salinas

import time
import threading
import os
import radio.radio_ctrl as radio
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 6100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def do_ping(radio):
	global end
        while 1:
		try:
			radio.internet_connect()
                	time.sleep(20)
                        if end == True:
				break
                except KeyboardInterrupt:
                    	end = True

def do_audio(radio):
	global end
	while 1:
           	try:
                	radio.audio_device()
                    	if end == True: break
                except KeyboardInterrupt:
                    	end = True

def do_escuchas(radio):
	global end
	num = 0
	while 1:
		if radio.bro_flag:
			num = radio.n_listeners()
			sock.sendto('e#' + str(num), ('localhost', 6000))
		else:
			num = None
			pass
		if end == True: break
		time.sleep(1)

def trns():
	print "button"
	if data == "true":
		print "transmitir"
		r_tm.start_transm()
	else:
		print "detener"
		r_tm.stop_transm()
	#r_tm.transm()

if __name__ == '__main__':

	global end
	global data
	try:
		end = False
		r_tm = radio.radio_class(sock)
		d_p = threading.Thread(target = do_ping, args = (r_tm,))
		d_a = threading.Thread(target = do_audio, args = (r_tm,))
		d_e = threading.Thread(target = do_escuchas, args = (r_tm,))

		d_p.start()
		d_a.start()
		d_e.start()

		while 1:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			print "received message:", data
			trns()

	except KeyboardInterrupt:
		end = True
		print 'Fin del Programa'
