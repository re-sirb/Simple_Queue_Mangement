#!/usr/bin/python
# -*- coding: utf-8 -*-

#PYTHON 3!!!!!!!

import usb.core
import usb.util
from datetime import datetime, timedelta

class USB_Printer:
	def __init__(self): 
		#pass
		self.open()
		#self._raw(msg)
		#self.close()
	
	def open(self):
		""" Search device on USB tree and set it as escpos device.
		:param usb_args: USB arguments
		"""
		self.device = usb.core.find(idVendor=0x04b8, idProduct=0x0e15)
		if self.device is None:
			print("Device not found or cable not plugged in.")
			raise USBNotFoundError("Device not found or cable not plugged in.")
		else:
			pass
			#print("Device found!")
	
		self.idVendor = self.device.idVendor
		self.idProduct = self.device.idProduct
	
		# pyusb has three backends: libusb0, libusb1 and openusb but
		# only libusb1 backend implements the methods is_kernel_driver_active()
		# and detach_kernel_driver().
		# This helps enable this library to work on Windows.
		if self.device.backend.__module__.endswith("libusb1"):
			check_driver = None
	
			try:
				check_driver = self.device.is_kernel_driver_active(0)
			except NotImplementedError:
				pass
	
			if check_driver is None or check_driver:
				try:
					self.device.detach_kernel_driver(0)
				except NotImplementedError:
					pass
				except usb.core.USBError as e:
					if check_driver is not None:
						print("Could not detatch kernel driver: {0}".format(str(e)))
	
		try:
			self.device.set_configuration()
			self.device.reset()
			#print("Device config ready!")
		except usb.core.USBError as e:
			print("Could not set configuration: {0}".format(str(e)))
	
	def write(self, msg):
		self._raw(msg)
		
	def _raw(self, msg):
		""" Print any command sent in raw format
		:param msg: arbitrary code to be printed
		:type msg: bytes
		"""
		#self.device.write(self.out_ep, msg, self.timeout)
		self.device.write(0x1, msg)
	
	def _read(self):
		""" Reads a data buffer and returns it to the caller. """
		return self.device.read(0x1, 16)
	
	def close(self):
		""" Release USB interface """
		if self.device:
			usb.util.dispose_resources(self.device)
		self.device = None



class print_ticket:
	#devfile="/dev/usb/lp0"
	#device = usb.core.find(idVendor=0x04b8, idProduct=0x0e15)
	
	def __init__(self):
		#self.devfile=DEV
		pass
	
	def __int_txt(self):
		char_lst=[0x1B, 0x40, 10] 
		ret_val=bytearray(char_lst)
		return ret_val
		
	def __set_FONT_A(self):
		char_lst=[0x1B, 0x4D, 0, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_bold_on(self):
		char_lst=[0x1B, 0x45, 1, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_bold_off(self):
		char_lst=[0x1B, 0x45, 0, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_FONT_B(self):
		char_lst=[0x1B, 0x4D, 1, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_txt_space_smaler(self):
		char_lst=[0x1B, 0xc1, 2, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_txt_space_bigger(self):
		char_lst=[0x1B, 0xc1, 0, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_txt_size_BIG(self):
		char_lst=[0x1D, 0x21, 17, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_txt_size_normal(self):
		char_lst=[0x1D, 0x21, 0, 10] #15
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __set_german_code(self):
		char_lst=[0x1B, 0x52, 2, 10] #germany
		ret_val=bytearray(char_lst)
		return ret_val
	
	def __format_txt(self, str_msg):
		import textwrap
		from_str='\n'.join(textwrap.wrap(str_msg, 64, break_long_words=False))
		ret_val=self.__encode_string(from_str)
		return ret_val
	
	def __encode_string(self, c_str):
		char_lst=[]
		for n in c_str:
			if n=="ä":
				char_lst.append(123)
			elif n=="ö":
				char_lst.append(124)
			elif n=="ü":
				char_lst.append(125)
			elif n=="Ä":
				char_lst.append(91)
			elif n=="Ö":
				char_lst.append(92)
			elif n=="Ü":
				char_lst.append(93)
			elif n=="ß":
				char_lst.append(126)
			elif(len(n.encode(encoding='utf-8'))==1):
				
				if(int.from_bytes(n.encode(encoding='utf-8'), "little")<=127):
					char_lst.append(int.from_bytes(n.encode(encoding='utf-8'), "little"))
				else:
					char_lst.append(95)
			else:
				char_lst.append(95)
		
		ret_val=bytearray(char_lst)
		
		return ret_val
	
	def __push_cut(self, p_lenght=5):
		#vs = [0x1B, 0x64, 10]
		#sn = [0x1B, 0x69, 10]
		char_lst=[]
		char_lst.append(10)
		n=0
		while (n<p_lenght):
			char_lst.append(32)
			char_lst.append(10)
			n=n+1
			
		char_lst.append(0x1B)
		char_lst.append(0x69)
		char_lst.append(10)
		
		ret_val=bytearray(char_lst)
		
		return ret_val
	
	
	def print_patient_ticket(self, ticket_nr, t_title):
		
		import sys
		
		msg2=" \n________________________________________________________________\n "
		try:
			#device = open(self.devfile, "wb")
			device = USB_Printer()
			
			device.write(self.__int_txt())
			device.write(self.__set_german_code())
			
			device.write(self.__set_txt_size_normal())
			device.write(self.__set_FONT_A())
			device.write(self.__format_txt(t_title ))
			
			device.write(self.__set_FONT_B())
			device.write(self.__format_txt(msg2))
			
			device.write(self.__set_FONT_A())
			device.write(self.__set_txt_size_BIG())
			device.write(self.__format_txt("        Nr: " + str(ticket_nr)))
			device.write(self.__set_txt_size_normal())
			
			device.write(self.__set_FONT_B())
			device.write(self.__format_txt(msg2))
			device.write(self.__set_FONT_B())
			device.write(self.__format_txt("Klinikum Fürth" + "  /  " + datetime.now().strftime("%d.%m.%Y - %H:%M")+"\n"))
			
			device.write(self.__push_cut())
			device.close()
	
		except:
			print("Printer error!")
