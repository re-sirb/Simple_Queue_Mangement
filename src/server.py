#!/usr/bin/python
# -*- coding: utf-8 -*-
import _thread

import http.server
import socketserver
import urllib.parse

from input_processor import process_input
proc_in = process_input()

#Port for user-interface 
PORT_1 = 5555
#Port for display 
PORT_2 = 5556

#Handler = http.server.SimpleHTTPRequestHandler

class mod_Handler_disp(http.server.BaseHTTPRequestHandler):

	def _set_headers(self, status):
		self.send_response(status)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
	
	#for file-transfer
	def _set_file_header_jpeg(self):
		n=proc_in.open_binary_file("HTML/logo.jpg")
		self.send_response(200)
		self.send_header('Content-type', 'image/jpeg')
		self.end_headers()
		self.wfile.write(n)
	
	#for icon-transfer
	def _set_file_header_ico(self):
		n=proc_in.open_binary_file("HTML/favicon.ico")
		self.send_response(200)
		self.send_header('Content-type', 'image/ico')
		self.end_headers()
		self.wfile.write(n)

	#for sound-transfer
	def _set_file_header_mp3(self):
		n=proc_in.open_binary_file("HTML/ding.mp3")
		self.send_response(200)
		self.send_header('Content-type', 'audio/mp3')
		self.end_headers()
		self.wfile.write(n)

	
	def _parse_data_post(self, data):
		out_val=[]
		temp_val=data.split("&")
		for n in temp_val:
			temp_lst=n.split("=")
			temp_var=temp_lst[1].replace("+", " ")
			temp_lst[1]=temp_var
			out_val.append(temp_lst)
		return out_val

	def do_GET(self):

		#get request bearbeiten
		data = self.path # <--- Gets the data itself
		#print(data)
		
		if(data=="/"):
			self._set_headers(200)
			#return_txt=pr_i.open_html_file("HTML/laden.htm")
			return_txt=proc_in.open_html_file("HTML/display.htm")
			self.wfile.write(return_txt.encode(encoding='utf-8',errors="namereplace"))
		elif(data=="/ding.mp3"):
			self._set_file_header_mp3()
		elif(data=="/logo.jpg"):
			self._set_file_header_jpeg()
		elif(data=="/favicon.ico"):
			self._set_file_header_ico()
		else:
			self._set_headers(404)
			#return_txt=pr_i.open_html_file("HTML/X.htm")
			return_txt=proc_in.open_html_file("HTML/404.htm")
			self.wfile.write(return_txt.encode(encoding='utf-8',errors="namereplace"))
		
	
	def do_HEAD(self):
		self._set_headers(200)
	
	def do_POST(self):
		#posted data
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		#print(self.path)
		#URL-encodeing decodieren
		post_data_decoded=urllib.parse.unquote(post_data.decode('utf-8'))
		post_data_parsed=self._parse_data_post(post_data_decoded)
		#print(post_data_parsed)
		#Reply
		######return_txt=pr_i.process_response(post_data_parsed)
		return_txt=proc_in.json_display()
		self._set_headers(200)
		self.wfile.write(return_txt.encode(encoding='utf-8',errors="namereplace"))


class mod_Handler(http.server.BaseHTTPRequestHandler):

	def _set_headers(self, status):
		self.send_response(status)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
	
	#for file-transfer
	def _set_file_header_ico(self):
		n=proc_in. open_binary_file("HTML/favicon.ico")
		self.send_response(200)
		self.send_header('Content-type', 'image/ico')
		self.end_headers()
		self.wfile.write(n)
	
	def _parse_data_post(self, data):
		out_val=[]
		temp_val=data.split("&")
		for n in temp_val:
			temp_lst=n.split("=")
			temp_var=temp_lst[1].replace("+", " ")
			temp_lst[1]=temp_var
			out_val.append(temp_lst)
		return out_val

	def do_GET(self):

		#get request bearbeiten
		data = self.path # <--- Gets the data itself
		print(data)
		
		if(data=="/"):
			self._set_headers(200)
			#return_txt=pr_i.open_html_file("HTML/laden.htm")
			return_txt=proc_in.open_html_file("HTML/menu.htm")
			self.wfile.write(return_txt.encode(encoding='utf-8',errors="namereplace"))
		elif(data=="/favicon.ico"):
			self._set_file_header_ico()
		else:
			self._set_headers(404)
			#return_txt=pr_i.open_html_file("HTML/X.htm")
			return_txt=proc_in.open_html_file("HTML/404.htm")
			self.wfile.write(return_txt.encode(encoding='utf-8',errors="namereplace"))
		
	
	def do_HEAD(self):
		self._set_headers(200)
	
	def do_POST(self):
		#posted data
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		#print(self.path)
		#URL-encodeing decodieren
		post_data_decoded=urllib.parse.unquote(post_data.decode('utf-8'))
		post_data_parsed=self._parse_data_post(post_data_decoded)
		#print(post_data_parsed)
		#Reply
		######return_txt=pr_i.process_response(post_data_parsed)
		return_txt=proc_in.process_response(post_data_parsed)
		self._set_headers(200)
		self.wfile.write(return_txt.encode(encoding='utf-8',errors="namereplace"))

def start_GUI():
	with socketserver.TCPServer(("127.0.0.1", PORT_1), mod_Handler) as httpd_control:
		print("GUI serving at port", PORT_1)
		httpd_control.serve_forever()

def start_Display():
	with socketserver.TCPServer(("", PORT_2), mod_Handler_disp) as httpd_display:
		print("Display serving at port", PORT_2)
		httpd_display.serve_forever()


_thread.start_new_thread(start_GUI,())
start_Display()
#_thread.start_new_thread(start_Display,())


#with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print("serving at port", PORT)
#    httpd.serve_forever()
