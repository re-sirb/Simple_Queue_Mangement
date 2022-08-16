#!/usr/bin/python
# -*- coding: utf-8 -*-

#import json 
from print_ticket import print_ticket

class process_input:
	
	def __init__(self):
		
		self.current_ticket_nr=10
		
		self.json_str=""
		
		self.off_status=False
		self.off_msg="Die Ambulanz ist aktuell geschlossen"
		
		self.mod_title="Narkoseaufklärung"
		
		self.cabin=["Leer", "Leer", "Leer", "Leer", "Leer"]
		self.ticket_lst=[]
		
		self.display_name_lst=[]
		self.display_nr_lst=[]
	
	
	def process_response(self, data):
		ret_val=""
		#print(data)
		keyword=self.get_keyword_value("datasource", data)
		if(keyword=="0"):
			pass
		elif(keyword=="new_ticket"):
			self.add_ticket(self.get_keyword_value("t_name", data))
		elif(keyword=="del_ticket"):
			self.delete_ticket(self.get_keyword_value("t_name", data))
		elif(keyword=="change_cab_stat"):
			self.update_cabin(self.get_keyword_value("number", data), self.get_keyword_value("t_name", data))
		elif(keyword=="reset"):
			self.clear_ticket_lst()
		elif(keyword=="new_off_txt"):
			self.off_msg=self.get_keyword_value("txt", data)
		elif(keyword=="new_mod_name"):
			self.mod_title=self.get_keyword_value("mod_name", data)
		elif(keyword=="start_session"):
			self.off_status=False
		elif(keyword=="stop_session"):
			self.off_status=True
			self.clear_ticket_lst()
		else:
			pass
		
		ret_val=self.json_response()
		return ret_val
	
	
	def update_display_lst(self, nr, name):
		for n in self.ticket_lst:
			if(n[1]==name):
				self.display_name_lst.insert(0,n[0])
				if(nr=="1"):
					self.display_nr_lst.insert(0,"Kabine 1")
				if(nr=="2"):
					self.display_nr_lst.insert(0,"Kabine 2")
				if(nr=="3"):
					self.display_nr_lst.insert(0,"Kabine 3")
				if(nr=="4"):
					self.display_nr_lst.insert(0,"Behandlungszimmer 1")
				if(nr=="5"):
					self.display_nr_lst.insert(0,"Behandlungszimmer 2")
				break
		while(len(self.display_name_lst)>10):
			del self.display_name_lst[-1]
			
		while(len(self.display_nr_lst)>10):
			del self.display_nr_lst[-1]

	
	def update_cabin(self,nr,name):
		n=int(nr)-1
		if(name=="Leer"):
			self.cabin[n]="Leer"
		else:
			self.cabin[n]=name
			self.update_display_lst(nr, name)
	
	def add_ticket(self, t_name):
		skip_t=False
		for n in self.ticket_lst:
			if(n[1]==t_name):
				skip_t=True
				break
		if(skip_t==False):
			temp_lst=[]
			temp_lst.append(str(self.current_ticket_nr))
			temp_lst.append(t_name)
			self.ticket_lst.append(temp_lst)
			# PRINT NEW TICKET
			t_printer=print_ticket()
			t_printer.print_patient_ticket(self.current_ticket_nr, self.mod_title)
			#print(self.current_ticket_nr)
			self.current_ticket_nr=self.current_ticket_nr+1
	
	def delete_ticket(self, t_name):
		temp_lst=[]
		for n in self.ticket_lst:
			if (n[1]!=t_name):
				temp_lst.append(n)
		#print(temp_lst)
		self.ticket_lst=temp_lst
	
	def clear_ticket_lst(self):
		self.ticket_lst=[]
		self.cabin=["Leer", "Leer", "Leer", "Leer", "Leer"]
		self.current_ticket_nr=10
		self.display_name_lst=[]
		self.display_nr_lst=[]
	
	def json_response(self):
		#ticket-lst
		ret_val="{\"ticket_lst\":["
		if(len(self.ticket_lst)>0):
			for n in self.ticket_lst:
				if(len(n)>0):
					# if pat. not in cabin > show in list
					if(n[1] not in self.cabin):
						ret_val=ret_val + "\"" + n[1] + "\","
			if(ret_val[-1:]==","):
				ret_val=ret_val[:-1]
		ret_val=ret_val+"],"
		#title
		ret_val=ret_val+"\"title\":\""
		ret_val=ret_val+self.mod_title
		ret_val=ret_val+"\","
		#off-txt
		ret_val=ret_val+"\"off_txt\":\""
		ret_val=ret_val+self.off_msg
		ret_val=ret_val+"\","
		#cabin-lst
		ret_val=ret_val+"\"cabin_lst\":["
		for n in self.cabin:
			ret_val=ret_val + "\"" + n + "\","
		ret_val=ret_val[:-1]
		ret_val=ret_val+"],"
		#display_off
		ret_val=ret_val+"\"display_off\":"
		if(self.off_status==True):
			ret_val=ret_val+"true"
		else:
			ret_val=ret_val+"false"
		#end
		ret_val=ret_val+"}"
		#print(ret_val)
		return ret_val
		
	def json_display(self):
		#names
		ret_val="{\"ticket_nr\":["
		if(len(self.display_name_lst)>0):
			for n in self.display_name_lst:
				ret_val=ret_val + "\"" + n + "\","
			if(ret_val[-1:]==","):
				ret_val=ret_val[:-1]
		ret_val=ret_val+"],"
		#nrs
		ret_val=ret_val+"\"cabin\":["
		if(len(self.display_nr_lst)>0):
			for n in self.display_nr_lst:
				ret_val=ret_val + "\"" + n + "\","
			if(ret_val[-1:]==","):
				ret_val=ret_val[:-1]
		ret_val=ret_val+"],"
		#title
		ret_val=ret_val+"\"doc_title\":\""
		ret_val=ret_val+self.mod_title
		ret_val=ret_val+"\","
		#off_msg
		ret_val=ret_val+"\"screen_message\":\""
		ret_val=ret_val+self.off_msg
		ret_val=ret_val+"\","
		#display_off
		ret_val=ret_val+"\"clear_screen\":"
		if(self.off_status==True):
			ret_val=ret_val+"true"
		else:
			ret_val=ret_val+"false"
		#end
		ret_val=ret_val+"}"
		#print(ret_val)
		return ret_val
	
	def open_html_file(self,file_n):
		ret_val=""
		try:
			f=open(file_n,"r")
			ret_val=f.read()
			f.close()
		except:
			print("Could not open file!")
		return ret_val
	
	def open_binary_file(self,file_n):
		ret_val=""
		try:
			f=open(file_n,"rb")
			ret_val=f.read()
			f.close()
		except:
			print("Could not open file!")
		return ret_val
	
	def get_keyword_value(self, s_var, data):
		ret_val=""
		for n in data:
			if (n[0]==s_var):
				ret_val=n[1]
				break
		return ret_val


