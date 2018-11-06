# -*- coding: utf-8 -*-
# Clase para control de acciones de Radio con Raspberry
# mensajito.mx
# Idea Original : Diego Aguirre
# Código: Antonio Salinas

import os
import sys
import subprocess as sub
import xml.etree.ElementTree as ET
import time
import urllib2
import ConfigParser

class radio_class:

	bro_flag = False	# Flag -- BROADCAST
	int_flag = False	# Flag -- INTERNET
	aud_flag = False	# Flag -- AUDIO
	usb_flag = False 	# Flag -- USB

	mount_Point = ''	# Broadcast Link
	name 		= ''	# Broadcast Name
	location 	= ''	# Broadcast Location
	description = ''	# Broadcast Description
	genre 		= '' 	# Broadcast genre
	tags		= ''
	record 		= ''
	mp3_file	= ''
	path_usb	= ''
	listeners = 0
	socket = ''

	# Class Constructor
	def __init__(self, socket):

		# Get Mount Point
		self.gen_mountPoint()

		# Default Data
		self.name 		= 'mensajito'
		self.location		= 'mensajito'
		self.description	= 'mensajito'
		self.genre 		= 'mensajito'
		self.tags		= ''
		self.socket		= socket

	def gen_mountPoint(self):
		proc = sub.Popen('cat /sys/class/net/eth0/address', shell=True, stdout=sub.PIPE, )
                phy_add=proc.communicate()[0]
                add_phy = phy_add[::-1]
                add_phy = add_phy.split('\n')
                self.mount_Point = add_phy[1].replace(':','')
		return self.mount_Point

	def get_data(self):
		file = open("/home/pi/data.txt", "r")
		data = file.read()
		name = data.split('\n')[0]
		location = data.split('\n')[1]
		self.name = name
                self.location = location

	def internet_connect(self):
		ping = os.system('sudo timeout 0.25 ping -c1 8.8.8.8 > /dev/null')
		nb_ping = not(bool(ping))
		print nb_ping
                if nb_ping != self.int_flag:
                        if ping == 0:
                                self.internet_up()
                        else:
                                self.internet_down()
		return ping

	def internet_up(self):
		self.int_flag = True
		return self.int_flag

	def internet_down(self):
		self.int_flag = False
		# Método que termina transmisión
		self.stop_transm()
		return self.int_flag

	def audio_device(self):
		a_dev = os.popen('arecord -l')
		line_t = a_dev.read()
		line = line_t.split('\n')
		n_lines = len(line)
		if bool(n_lines - 2) != self.aud_flag:
			if n_lines == 2:
				print '\nNo se encuentra dispositivo de audio'
				self.audio_down()
			elif n_lines == 5:
				self.audio_up()
		return n_lines

	def audio_up(self):
		self.aud_flag = True
		return self.aud_flag

	def audio_down(self):
		self.aud_flag = False
		return self.aud_flag

	def chk_usb(self):
		a = os.listdir("/media/pi/")
		if len(a) == 0:
			print "sin dispositivos"
			self.usb_flag = False
		else:
        		path = "/media/pi/" + a[0]
        		self.path_usb = path + '/'
			self.usb_flag = True


	def mp3_date(self):
		date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		self.mp3_file = '/home/pi/audio/%s.mp3' %date
		return self.mp3_file

	def cfg_darkice(self):
		self.mp3_date()
		os.system('sudo rm /etc/darkice.cfg')
		Config = ConfigParser.ConfigParser()
		Config.optionxform = str
		cfgfile = open("/home/pi/mensajito/data/aux_cfg",'w')
		Config.add_section('general')
		Config.add_section('input')
		Config.add_section('icecast2-0')
		# [general]
		Config.set('general', 'duration', 0)
		Config.set('general', 'bufferSecs', 30)
		Config.set('general', 'reconnect', 'yes')
		# [input]
		Config.set('input', 'device', 'hw:1,0')
		Config.set('input', 'sampleRate', 48000)
		Config.set('input', 'bitsPerSample', 16)
		Config.set('input', 'channel', 2)
		# [icecast2-0]
		Config.set('icecast2-0', 'bitrateMode', 'vbr')
		Config.set('icecast2-0', 'bitrate', 256)
		Config.set('icecast2-0', 'format', 'mp3')
		Config.set('icecast2-0', 'quality', 0.6)
		Config.set('icecast2-0', 'server', 'mensajito.mx')
		Config.set('icecast2-0', 'port', 8000)
		Config.set('icecast2-0', 'password', 'mensajito$1192')
		Config.set('icecast2-0', 'mountPoint', self.mount_Point)
		Config.set('icecast2-0', 'sampleRate', 48000)
		Config.set('icecast2-0', 'channel', 2)
		Config.set('icecast2-0', 'name', self.name)
		Config.set('icecast2-0', 'description', self.description)
		Config.set('icecast2-0', 'genre', self.genre)
		Config.set('icecast2-0', 'public', 'yes')
		Config.set('icecast2-0', 'localDumpFile', self.mp3_file)
		# Write the changes
		Config.write(cfgfile)
		cfgfile.close()
		os.system("sudo cp /home/pi/mensajito/data/aux_cfg /etc/darkice.cfg")
		os.system("sudo rm /home/pi/mensajito/data/aux_cfg")

	def n_listeners(self):
		try:
			str_listen = ''
            		url = 'http://mensajito.mx:8000/' + self.mount_Point + '.xspf'
			f = urllib2.urlopen(url)
			data = f.read()
			data_split = data.split('\n')
			aux_listen = data_split[12].split(':')
			self.listeners = int(aux_listen[1])
		except:
			self.listeners = 0
		return self.listeners

	def start_transm(self):
		if self.int_flag == True and self.aud_flag == True:
			self.bro_flag = True
			self.get_data()
			self.cfg_darkice()
			os.system("darkice &")
			try:
				print self.name
				self.socket.sendto('n#' + self.name, ('localhost', 6000))
				print self.location
				self.socket.sendto('u#' + self.location, ('localhost', 6000))
			except Exception as e:
				print e
		else:
			self.socket.sendto('p#', ('localhost', 6000))

	def stop_transm(self):
		if self.aud_flag == True:
			self.bro_flag = False
			self.socket.sendto('p#', ('localhost', 6000))
			os.system('sudo killall darkice')

	def copy_data(self):
		self.chk_usb()
		if self.usb_flag == True:
			data_path = self.path_usb + "/radio_data.txt"
			print data_path
			print type(data_path)
			if os.path.isfile(data_path):
				os.system("cp " + self.path_usb + "/radio_data.txt /home/pi/mensajito/data/radio_data.txt")
				archi = open('/home/pi/mensajito/data/radio_data.txt','r')
				texto = archi.read()
				print texto
				txt = texto.split('\r\n')
				print txt
				try:
					self.name = txt[0].decode('utf-8')
					self.description = txt[1].decode('utf-8')
					self.location = txt[2].decode('utf-8')
					self.genre = txt[3].decode('utf-8')
					self.tags = txt[4].decode('utf-8')
				except:
					pass

	def copy_image(self):
		if self.usb_flag == True:
			if os.path.isfile(self.path_usb +  "/profile.png"):
				os.system("cp " + self.path_usb + "/profile.png /home/pi/mensajito/image/profile.png")

	def copy_audio(self):
		if self.usb_flag == True:
			os.system('sudo cp ' + self.mp3_file + ' /media/pendrive')
			# os.system('rm ' + self.record);

