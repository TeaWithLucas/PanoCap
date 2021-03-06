import json
import zlib
import re
import os
import csv
import urllib.request
import socket
import certifi
import shutil
import shlex
import subprocess
import tarfile
import zipfile
import tempfile 
import io
import datetime
import threading
import queue
import time
import random
from tkinter import *
import tkinter.ttk as ttk
import configparser
import logging

settingsfl = 'settings.ini'
version = 4.1

class gui():
	#constructor called on creation
	def __init__(self, title = 'the game'):
		print(time.strftime('%y-%m-%d %H:%M:%S'), 'initialisng gui')

		global threads, conn
		
		with open(logfile, 'w'):
			pass
		
		self.running = True
		self.title = title

		#TK gui window
		self.main = Tk()
		main = self.main
		main.resizable(width = True, height = True)
		main.title(self.title)

		#main frame
		frame = Frame(main, background = 'white')
		frame.pack()
		frame.rowconfigure(0, weight=1)
		frame.columnconfigure(0, weight=1)
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(1, weight=1)
		frame.rowconfigure(2, weight=1)
		frame.columnconfigure(2, weight=1)
		frame.rowconfigure(3, weight=1)
		frame.columnconfigure(3, weight=1)

		#creating each widget
		
		frame_left = Frame(frame, background = 'white')
		#frame_left.pack( side = LEFT, fill=BOTH, expand=True)
		frame_left.grid(row = 1, column = 1)
		frame_left.rowconfigure(1, weight=1)
		frame_left.columnconfigure(1, weight=1)
		

		output_label_widget = Label(frame_left, text="General Output", font=("Helvetica", 14))
		output_label_widget.grid(row = 1, column = 1)
		output_widget = Text(frame_left, bg = 'black', fg = '#D3D3D3', padx = 10, pady = 10, height=20, wrap = WORD)
		output_widget.grid(row = 2, column = 1)
		ffmpeg_label_widget = Label(frame_left, text="ffmpeg Output", font=("Helvetica", 14))
		ffmpeg_label_widget.grid(row = 3, column = 1)
		ffmpeg_widget = Text(frame_left, bg = 'black', fg = '#D3D3D3', padx = 10, pady = 10, height=20, wrap = WORD)
		ffmpeg_widget.grid(row = 4, column = 1)

		frame_middle = Frame(frame, background = 'white')
		#frame_middle.pack( side = LEFT, fill=BOTH, expand=True)
		frame_middle.grid(row = 1, column = 2)
		frame_middle.rowconfigure(1, weight=1)
		frame_middle.columnconfigure(1, weight=1)

		title_widget = Label(frame_middle, text="PanoCap", font=("Helvetica", 20))
		title_widget.grid(row = 1, column = 1)

		tree_label_widget = Label(frame_middle, text="Sessions Found", font=("Helvetica", 16))
		tree_label_widget.grid(row = 2, column = 1)

		self.tree = ttk.Treeview(frame_middle, height=20)
		self.tree.grid(row = 3, column = 1)

		status_widget = Label(frame_middle, text="Please Wait...", font=("Helvetica", 14))
		status_widget.grid(row = 4, column = 1)

		frame_cookies = Frame(frame_middle, background = 'white')
		frame_cookies.grid(row = 5, column = 1)

		self.cookie_aspath_var = StringVar()
		self.cookie_yourid_var = StringVar()

		cookie_aspath_label_widget = Label(frame_cookies, text="ASPXAUTH", font=("Helvetica", 12))
		cookie_aspath_label_widget.grid(row = 1, column = 1)
		cookie_yourid_label_widget = Label(frame_cookies, text="Your ID", font=("Helvetica", 12))
		cookie_yourid_label_widget.grid(row = 1, column = 4)		
		cookie_aspath_widget = Entry(frame_cookies, textvariable=self.cookie_aspath_var, bg = 'black', fg = 'white', insertbackground ='white')
		cookie_aspath_widget.grid(row = 2, column = 1)
		cookie_yourid_widget = Entry(frame_cookies, textvariable=self.cookie_yourid_var, bg = 'black', fg = 'white', insertbackground ='white')
		cookie_yourid_widget.grid(row = 2, column = 4)

		console_widget = Entry(frame_middle, bg = 'black', fg = 'white', insertbackground ='white')
		console_widget.grid(row = 6, column = 1)

		frame_buttons = Frame(frame_middle, background = 'white')
		frame_buttons.grid(row = 7, column = 1)
		
		button_start = Button(frame_buttons, text="Get Latest Data", command=self.call_start)
		button_start.grid(row = 1, column = 1)
		button_aquire = Button(frame_buttons, text="Aquire Raw Sessions", command=self.call_aquire_sessions)
		button_aquire.grid(row = 1, column = 2)
		button_compress = Button(frame_buttons, text="Compress Sessions", command=self.call_compress_sessions)
		button_compress.grid(row = 1, column = 3)
		button_save = Button(frame_buttons, text="Save Cookies", command=self.call_save)
		button_save.grid(row = 1, column = 4)
		button_exit = Button(frame_buttons, text="Exit", command=self.call_exit)
		button_exit.grid(row = 1, column = 6)

		frame_right = Frame(frame, background = 'white')
		#frame_right.pack( side = LEFT, fill=BOTH, expand=True)
		frame_right.grid(row = 1, column = 3)
		frame_right.rowconfigure(1, weight=1)
		frame_right.columnconfigure(1, weight=1)

		#Widget dictionary for access
		self.widgets = {
			'console' : console_widget,
			'output' : output_widget,
			'status' : status_widget,
			'ffmpeg' : ffmpeg_widget,
			'tree1' : self.tree,
			'btn_start' : button_start,
			'btn_aquire' : button_aquire,
			'btn_compress' : button_compress,
			'btn_save' : button_save,
			'btn_exit' : button_exit,
			'cookie_aspath' : cookie_aspath_widget,
			'cookie_yourid' : cookie_yourid_widget
		}

		treads = []
		for n in range(len(threads)):
			threadname = 'Thread-'+str(n)
			label = threadname+'-label'
			ffmpeg = threadname+'-ffmpeg'
			i = 3*n
			treads.append(Label(frame_right, text=threadname, font=("Helvetica", 16)))
			treads[i].grid(row = (i+1), column = 1)
			self.widgets[label] = treads[i]
			ii = 3*n+1
			treads.append(Label(frame_right, text='thread', font=("Helvetica", 12)))
			treads[ii].grid(row = (ii+1), column = 1)
			self.widgets[ffmpeg] = treads[ii]
			iii = 3*n+2
			treads.append(Text(frame_right, bg = 'black', fg = '#D3D3D3', padx = 5, pady = 5, wrap = WORD, height=12))
			treads[iii].grid(row = (iii+1), column = 1)
			treads[iii].config(state = DISABLED)
			self.widgets[threadname] = treads[iii]
			
			
		#Disable all widgets so they become read only
		self.widgets['console'].config(state = DISABLED)
		self.widgets['output'].config(state = DISABLED)
		self.widgets['btn_start'].config(state = DISABLED)
		self.widgets['btn_aquire'].config(state = DISABLED)
		self.widgets['btn_compress'].config(state = DISABLED)
		self.widgets['btn_save'].config(state = DISABLED)
		self.widgets['btn_exit'].config(state = DISABLED)
		self.widgets['cookie_aspath'].config(state = DISABLED)
		self.widgets['cookie_yourid'].config(state = DISABLED)


		#Bind the button press to a function
		console_widget.bind('<Return>', self.rtn_pressed)
		self.tree.bind('<Double-Button-1>', self.onDoubleClick)
		#self.set_columns('tree1', ('SessionID', 'SessionAbstract','StartTime', 'Duration', 'NumStreams'), ('Name', 'ID', 'Abstract','Time', 'Duration', 'Streams'))
		column_data = [{'ID':'SessionID', 'Name':'ID', 'width':10},{'ID':'SessionName', 'Name':'Session Name', 'width':380},{'ID':'SessionAbstract', 'Name':'Abstract', 'width':250},{'ID':'StartTime', 'Name':'Date', 'width':90},{'ID':'Duration', 'Name':'Duration', 'width':60},{'ID':'NumStreams', 'Name':'streams', 'width':55}]
		self.set_columns('tree1', column_data)
		#Set focus on the console
		#console_widget.focus_set()

		self.check_cookies()
		conn = connection()

		#self.current_stage = "init"
		self.arg = False
		#end of init

	def check_cookies(self):
		self.cookie_aspath_var.set(settings['Cookies']['ASPXAUTH'])
		self.cookie_yourid_var.set(settings['Cookies']['yourid'])
		self.current_stage = "setcookies"
		if settings['Cookies']['ASPXAUTH'] == "":
			self.set_lbl("Cookies Empty...Please enter correct ones")

		else:
			self.set_lbl("Cookies Found... Please Wait...")
		self.widgets['cookie_aspath'].config(state = NORMAL)
		self.widgets['cookie_yourid'].config(state = NORMAL)
		self.widgets['btn_save'].config(state = NORMAL)




	#Event driven fuctions
	def rtn_pressed(self, event):
		to_print_d("Input - Enter Key")
		self.stage_man.navigate(self.get_input())

	def call_start(self):
		global conn, cachefolder
		print("Input - Start Button")
		self.widgets['btn_start'].config(state = DISABLED)
		self.set_lbl("Please Wait...")
		self.repeater()
		records = conn.GetSessions()
		logging.info(records)
		#to_print_d(records)
		if len(records) > 0:
			conn.GetSessionsInfo(records)
			
			self.current_stage = "start"
			self.setup_next_stage()
		else:
			self.current_stage = "setcookies"
			self.widgets['btn_save'].config(state = NORMAL)
			self.add_txt("Error, possible invalid or expired cookies...")

	def setup_next_stage(self):
		global threads, pauseFlag, workQueue, sessionInfo, exitFlag, conn
		pauseFlag = 1
		idlethreads = 0
		for t in threads:
			#if t.idle:
			idlethreads += t.idle
		#print(workQueue.empty(), idlethreads, len(threads))
		if workQueue.empty() and idlethreads >= len(threads) and not exitFlag:
			pauseFlag = 0
			if self.current_stage == "start":
				self.records = SessionsInfo
				self.call_save_json()
				#self.widgets['btn_save'].config(state = NORMAL)
				self.widgets['btn_aquire'].config(state = NORMAL)
				self.widgets['btn_exit'].config(state = NORMAL)
			if self.current_stage == "aquire":
				self.widgets['btn_start'].config(state = NORMAL)
				self.widgets['btn_exit'].config(state = NORMAL)
			if self.current_stage == "compress" or self.current_stage == "init":
				self.widgets['btn_start'].config(state = NORMAL)
				self.widgets['btn_exit'].config(state = NORMAL)
			if self.current_stage == "setcookies":
				settings['Cookies']['ASPXAUTH'] = self.cookie_aspath_var.get()
				settings['Cookies']['yourid'] = self.cookie_yourid_var.get()
				write_settings(settings, settingsfl)
				cookies = 'UserSettings=LastLoginMembershipProvider=CLAWSBlackboard; .ASPXAUTH='+settings['Cookies']['ASPXAUTH']+'; clawsblackboard\\'+settings['Cookies']['yourid']+'={"defaultVolume":100,"defaultBitrateMBR":2}; CLAWSBlackboard\\'+settings['Cookies']['yourid']+'={"navBarSection":1}'
				conn.set_cookies(cookies)
				if conn.TestConnection():
					self.add_txt("Correct cookies")
					self.widgets['cookie_aspath'].config(state = DISABLED)
					self.widgets['cookie_yourid'].config(state = DISABLED)
					self.widgets['btn_save'].config(state = DISABLED)
					self.widgets['btn_start'].config(state = NORMAL)
					self.current_stage = "init"
				else:
					self.add_txt("Invalid or expired cookies...Please try again...")
				self.widgets['btn_exit'].config(state = NORMAL)
			self.set_lbl("Click to continue")
		else:
			if exitFlag:
				print(idlethreads)
				if idlethreads >= len(threads):
					print("exiting...")
					self.set_lbl("Bye!")
					self.main.destroy()
					exit()
			else:
				self.main.after(1000, self.setup_next_stage)

	def call_aquire_sessions(self):
		self.widgets['btn_aquire'].config(state = DISABLED)
		self.set_lbl("Please Wait...")
		self.current_stage = "aquire"
		aquire_sessions(self.records)
		self.setup_next_stage()

	def call_compress_sessions(self):
		self.widgets['btn_compress'].config(state = DISABLED)
		self.set_lbl("Please Wait...")
		self.current_stage = "compress"
		compress_sessions(self.records)
		self.setup_next_stage()

	def call_exit(self):
		self.widgets['btn_exit'].config(state = DISABLED)
		self.widgets['btn_aquire'].config(state = DISABLED)
		self.widgets['btn_compress'].config(state = DISABLED)
		self.widgets['btn_start'].config(state = DISABLED)
		self.set_lbl("Shutting down... Waiting for threads to end... Please Wait...")
		self.current_stage = "exit"
		global threads, pauseFlag, workQueue, exitFlag
		exitFlag = 1
		self.setup_next_stage()

	def call_save(self):
		if self.current_stage == "setcookies":
			self.setup_next_stage()
		

	def call_save_json(self):
		jsontofile(groupsfile, conn.groups)
		save_cache(self.records, version)
		csvtofile(csvfile, self.records)

	def repeater(self):
		global win_outputs, processes
		outputs = win_outputs.copy()
		win_outputs.clear()
		for widget, strings in outputs.items():
			
			if str(type(self.widgets[widget])) == "<class 'tkinter.Text'>":
				string = "\n".join(strings)
				self.add_txt(inputstr=string, widget=widget)
			elif str(type(self.widgets[widget])) == "<class 'tkinter.Label'>":
				string = strings[(len(strings)-1)]
				self.set_lbl(inputstr=string, widget=widget)
			elif str(type(self.widgets[widget])) == "<class 'tkinter.Button'>":
				pass
		oldprocesses = processes[:]
		processes = []
		for process in oldprocesses:
			if process.poll():
				processes.append(process)
				self.add_txt(str(process.communicate()), widget='ffmpeg')
		self.main.after(1000, self.repeater)

	#Appends text at the end of a widget
	def add_txt(self, inputstr, widget="output", tag="", end="\n"):
		print(inputstr)
		self.widgets[widget].config(state = NORMAL)
		if tag != "":
			self.widgets[widget].insert(END, inputstr + end, tag)
		else:
			self.widgets[widget].insert(END, inputstr + end)
		self.widgets[widget].see(END)
		self.main.update()
		self.widgets[widget].config(state = DISABLED)

	def set_lbl(self, inputstr, widget="status"):
		self.widgets[widget].config(text=inputstr)
		self.main.update()


	def set_columns(self, widget, columns):
		column_ids = []
		count=0
		for column in columns:
			if count > 0:
				column_ids.append(column['ID'])
			count+=1

		self.widgets[widget]['columns'] = column_ids

		count = 0
		for column in columns:
			self.widgets[widget].heading('#'+str(count), text=column['Name'])
			self.widgets[widget].column('#'+str(count), stretch=YES, width=column['width'])
			count+=1

	def add_node(self, widget, parent='', iid=None, row=(), text=None, index=0):
		#print(self.widgets[widget])
		#print(iid)
		if self.widgets[widget].exists(iid):
			self.widgets[widget].item(iid, text=text, values=row)
		else:
			self.widgets[widget].insert(parent, index, iid=iid, text=text, values=row)
		
			
	def onDoubleClick(self, event):
		''' Executed, when a row is double-clicked. Opens 
		read-only EntryPopup above the item's column, so it is possible
		to select text '''

		print("double-clicked")
		# close previous popups
		#self.destroyPopups()

		# what row and column was clicked on
		rowid = self.tree.identify_row(event.y)
		column = self.tree.identify_column(event.x)

		# clicked row parent id
		parent = self.tree.parent(rowid)

		# do nothing if item is top-level		
		if parent != '':
			# get column position info
			x,y,width,height = self.tree.bbox(rowid, column)

			# y-axis offset
			pady = height // 2

			# place Entry popup properly		 
			#url = self.tree.item(rowid, 'text')
			curItem = self.tree.item(self.tree.focus())
			itemvalues = [curItem['text']] + curItem['values']
			#print(itemvalues, rowid, column[1:],x,y,width,height)
			self.entryPopup = EntryPopup(self.tree, itemvalues[int(column[1:])])
			self.entryPopup.place( x=x, y=y+pady, anchor=W, width=width)
		
class EntryPopup(Entry):

	def __init__(self, parent, text, **kw):
		self.parent=parent
		''' If relwidth is set, then width is ignored '''
		super().__init__(self.parent, **kw)

		self.insert(0, text) 
		self['state'] = 'readonly'
		self['readonlybackground'] = 'white'
		self['selectbackground'] = '#1BA1E2'
		self['exportselection'] = False

		self.focus_force()
		self.bind("<Control-a>", self.selectAll)
		self.bind("<Escape>", lambda *ignore: self.destroy())

	def selectAll(self, *ignore):
		''' Set selection on the whole text '''
		self.selection_range(0, 'end')

		# returns 'break' to interrupt default key-bindings
		return 'break'
		

class threaders(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.lablel = name +'-label'
		self.ffmpeg = name+'-ffmpeg'
		self.idle = 1
	def run(self):
		to_print_d("Starting " + self.name,  self.name)
		self.process_data(self.name)
		self.idle = 1
		to_print_d(self.name + " has stopped",  self.name)
	def process_data(self, threadName):
		global window, queueLock, workQueue, conn, SessionsInfo, SessionsMeta, exitFlag, pauseFlag
		while not exitFlag:
			
			queueLock.acquire()
			if not workQueue.empty():
				datas = workQueue.get()
				queueLock.release()
				if 'GetSession' in datas:
					self.idle = 0
					to_print(self.name + " - Working", widget=self.lablel)
					sessionid = datas['GetSession']['sessionid']
					groupid = datas['GetSession']['groupid']
					sessionindex = datas['GetSession']['sessionindex']
					cachedData = {}
					if 'cachedData' in datas['GetSession']:
						cachedData = datas['GetSession']['cachedData']
					
					to_print_d("Processing: " + sessionid, widget=self.name)
					print("Processing: " + sessionid)
					sessionInfo = conn.GetSession(sessionid, groupid, sessionindex, self.name)
					if sessionInfo != None:
						if len(sessionInfo['streams']) > 0:
							
							if len(cachedData) > 0:
								to_print_d("Using online version using cached for: " + sessionid, widget=self.name)
								for key, value in cachedData.items():
									if key not in sessionInfo:
										sessionInfo[key] = value
								if 'streams' in cachedData:
									for cachedSteam in cachedData['streams']:
										found = False
										for stream in sessionInfo['streams']:
											if cachedSteam['PublicID'] == stream['PublicID']:
												found = True
										if not found:
											sessionInfo['streams'].append(cachedSteam)
								if 'Timestamps' in cachedData:
									for cachedTS in cachedData['Timestamps']:
										found = False
										for stream in sessionInfo['Timestamps']:
											if cachedTS['ID'] == stream['ID']:
												found = True
										if not found:
											sessionInfo['Timestamps'].append(cachedTS)
							else:
								to_print_d("Using online version only for: " + sessionid, widget=self.name)
							if sessionid in SessionsMeta:
								for key, value in SessionsMeta[sessionid].items():
									if key in sessionInfo:
										sessionInfo[key] = value
							SessionsInfo[sessionInfo['SessionGroupID']][sessionid] = sessionInfo
							add_session_row(sessionInfo, groupid)
						else:
							to_print_d("No streams for: " + sessionid, widget=self.name)
					elif len(cachedData) > 0:
						to_print_d("No online version using cached for: " + sessionid, widget=self.name)
						sessionInfo = cachedData
						if sessionid in SessionsMeta:
							for key, value in SessionsMeta[sessionid].items():
								if key in sessionInfo:
									sessionInfo[key] = value
						SessionsInfo[sessionInfo['SessionGroupID']][sessionid] = sessionInfo
						add_session_row(sessionInfo, groupid)
					else:
						to_print_d("Data error for: " + sessionid, widget=self.name)
				if 'aquire_session' in datas:
					self.idle = 0
					to_print(self.name + " - Working", widget=self.lablel)
					data = datas['aquire_session']
					to_print_d("Processing: " + data['SessionName'], widget=self.name)
					aquire_session(data, self.name)
				if 'compress_session' in datas:
					self.idle = 0
					to_print(self.name + " - Working", widget=self.lablel)
					data = datas['compress_session']
					to_print_d("Processing: " + data['SessionName'], widget=self.name)
					compress_session(data, self.name)
				to_print(self.name + " - Idle", widget=self.lablel)
			else:
				queueLock.release()
				to_print(self.name + " - Idle", widget=self.lablel)
				self.idle = 1
				if pauseFlag:
					time.sleep(5)
				else:
					time.sleep(1)

class connection():
	

	def __init__(self):
		if os.path.exists(groupsfile):
			print('Checking for previous group data')
			with open(groupsfile, "r") as text_file:
				data=text_file.read()
				if data.strip() != "":
					self.groups = json.loads(data)
		else:
			self.groups = {'000':{'Name':'Miscellaneous','OrigName':'Miscellaneous','AncestorID':'000'}}
		self.attempts=0

	def set_cookies(self, cookies):
		self.cookies = cookies
		
	def get_data(self, url, headers={"Content-Type": "application/json; charset=utf-8"}, data=None):
	
		if data != None:
			databin = data.encode('utf-8')
		else:
			databin = "".encode('utf-8')	
		
		headers["cookie"] = self.cookies		

		req = urllib.request.Request(url=url, headers=headers, data=databin)
		#print(req.headers)
		
		worked = False
		attempts = 0;
		errtxt = ''
		while(worked == False and attempts < 1):
			try:
				resp = urllib.request.urlopen(req, cafile=cafileMain)
				worked = True
			except urllib.error.HTTPError as e:
				errtxt = f'HTTPError: {e}'
				print(errtxt)
				window.add_txt(errtxt)
			attempts+=1
		outcome = 'Success' if worked else 'Failure'
		print(f"HTTP Request Result: {outcome}, Attempts: {attempts}")
		if(not worked or attempts > 1):
			logging.debug(f"HTTP Request Result: {outcome}, Attempts: {attempts}")
			logging.debug(req.headers)
			logging.debug(errtxt)
		if worked:
			return resp.read()
		else:
			return None
		
	def TestConnection(self):
	
		global targets;
		
		self.attempts+=1

		window.add_txt('Testing Cookies: Attempt ' + str(self.attempts))

		bodydict = {"queryParameters":{"query":None, "page":0, "startDate":None,"endDate":None}}
		url = targets['urltarget'] + "/Services/Data.svc/GetSessions"
		
		headers={"Content-Type": "application/json; charset=utf-8"}

		dataraw = self.get_data(url=url, headers=headers, data =json.dumps(bodydict))
		
		worked = False
		
		if dataraw != None:
			data = self.decode_json(dataraw)
			results = data['d']['Results']
			#print(data)
			
			if results and len(results) > 0:
				worked = True

		return worked
	
	
	
	def GetSessions(self):
		window.add_txt('Getting Sessions')

		bodydict = {"queryParameters":{
			"query":None,
			"sortColumn":1,
			"sortAscending":False,
			"maxResults":500,
			"page":0,
			"startDate":None,
			"endDate":None,
			"bookmarked":False,
			"getFolderData":False,
			"isSharedWithMe":False,
			"includePlaylists":True
			}}
			
		global targets;
		
		url = targets['urltarget'] + "/Services/Data.svc/GetSessions"
		
		headers={"Content-Type": "application/json; charset=utf-8"}

		dataraw = self.get_data(url=url, headers=headers, data=json.dumps(bodydict))

		data = self.decode_json(dataraw)
		results = data['d']['Results']
		records = {}
		
		
		#print(results)

		for record in results:
			if 'DeliveryID' in record and record['DeliveryID'] != None:
				DeliveryID = record['DeliveryID']
				if 'FolderName' in record and record['FolderName'] != None:
					defaultName = record['FolderName']
				else:
					defaultName = 'Miscellaneous'
				#print(DeliveryID)
				
				window.add_txt('Processing: ' + DeliveryID + ' in ' + defaultName)
				groupID = '000'
				if 'FolderID' in record:
					groupID = record['FolderID']
				elif defaultName != 'Miscellaneous':
					errtxt = f'Error: No group ID, defaultName: {defaultName}, attempting reverse lookup'
					window.add_txt(errtxt)
					
					for key, item in self.groups.items():
						#print(item['Name'])
						if item['OrigName'] == defaultName:
							groupID = item['AncestorID']
					if groupID == '000':
						errtxt = f'Reverse lookup failed'
						window.add_txt(errtxt)
				else: 
					errtxt = f'Error: No group ID, defaultName: {defaultName}'
					window.add_txt(errtxt)
					groupID = '000'
					
				if groupID not in self.groups:
					groupAncestorID = self.GetAncestorGroup(groupID)
					self.groups[groupID] = self.GetGroupData(groupAncestorID)
					if self.groups[groupID]['Name'] == None:
						formattedName = regexgroup(defaultName) 
						errtxt = f'Error: No empty group name, defaulting to: {formattedName}'
						window.add_txt(errtxt)
						self.groups[groupID]['Name'] = formattedName
					if groupAncestorID not in self.groups:
						self.groups[groupAncestorID] = self.groups[groupID]
				else:
					print(groupID)
					groupAncestorID = self.groups[groupID]['AncestorID']
				groupID = groupAncestorID
					
				
				if groupID not in records:
					records[groupID] = []
				#StartTime = jsontots(record['StartTime'])
				records[groupID].append({'DeliveryID': DeliveryID})
			else:
				print('Broken record: ')
				print(record)
		#print(self.groups)
		return {key: records[key] for key in sorted(records.keys(), key=lambda item: self.groups[item]['Name'])}
		
	def GetAncestorGroup(self, FolderID):
		bodydict = 			{"queryParameters":{
			"query":None,
			"sortColumn":1,
			"sortAscending":False,
			"maxResults":25,
			"page":0,
			"startDate":None,
			"endDate":None,
			"folderID":FolderID,
			"bookmarked":False,
			"getFolderData":True,
			"isSharedWithMe":False,
			"includePlaylists":True}
			}		
			
		global targets;
		
		url = targets['urltarget'] + "/Services/Data.svc/GetSessions"
		
		headers={"Content-Type": "application/json; charset=utf-8"}
		
		dataraw = self.get_data(url=url, headers=headers, data=json.dumps(bodydict))
		
		if dataraw != None:
		
			data = self.decode_json(dataraw)
			
			
			if 'd' in data and 'ParentFolderId' in data['d'] and data['d']['ParentFolderId'] != None and data['d']['ParentFolderId'] != "":
				window.add_txt('ParentFolderId: ' + data['d']['ParentFolderId'])
				return self.GetAncestorGroup(data['d']['ParentFolderId']) 
			else:
				return FolderID
		else:
			return FolderID
			
	def GetGroupData(self, FolderID):
		bodydict = {"folderID":FolderID}
		
		global targets;
		
		url = targets['urltarget'] + "/Services/Data.svc/GetFolderInfo"
		
		headers={"Content-Type": "application/json; charset=utf-8"}
		
		dataraw = self.get_data(url=url, headers=headers, data=json.dumps(bodydict))
		
		if dataraw != None:
			data = self.decode_json(dataraw)
			
			#print(data)
			if 'd' in data and 'Name' in data['d'] and data['d']['Name'] != None and data['d']['Name'] != "":
				window.add_txt('Ancestor Name: ' + data['d']['Name'])
				return {
					'Name':regexgroup(data['d']['Name']), 
					'OrigName':data['d']['Name'], 
					'AncestorID':FolderID
				}
			else:
				return None
		else:
			return None

	def GetSession(self, sessionid, groupid, sessionindex, thread="output"):
		body = "deliveryId=" + sessionid + "&invocationId=&isLiveNotes=false&refreshAuthCookie=false&isActiveBroadcast=false&isEditing=false&isKollectiveAgentInstalled=false&isEmbed=false&responseType=json"
		
		global targets;
		
		url = targets['urltarget'] + '/Pages/Viewer/DeliveryInfo.aspx'
		
		headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
		
		dataraw = self.get_data(url=url, headers=headers, data=body)
		
		if dataraw != None:
	
			data = self.decode_json(dataraw)
		
			if 'Delivery' in data:
				
				#SessionGroup = norm_fn(data['Delivery']['SessionGroupLongName'])
				SessionGroupID = groupid
				SessionGroup = self.groups[groupid]['Name']
				
				session = {}
				for key, item in data['Delivery'].items():
					session[key] = item
				SessionName = norm_fn(data['Delivery']['SessionName'])
				StartTime = win2unixts(data['Delivery']['SessionStartTime'])
				Owner = data['Delivery']['OwnerDisplayName']
				SessionAbstract = data['Delivery']['SessionAbstract']
				
				name = fixsessionname(SessionName, SessionGroup, sessionindex)

				if SessionAbstract == "Presented by":
					SessionAbstract = name
				to_print_d("working on: " + name, widget=thread)
				
				session['SessionID'] = sessionid
				session['SessionName'] = name
				session['Name'] = name
				session['SessionGroupID'] = SessionGroupID
				session['SessionGroup'] = SessionGroup
				session['SessionAbstract'] = SessionAbstract
				session['StartTime'] = StartTime
				session['Owner'] = Owner
				session['streams'] = []
				session['Streams'] = []
				
				if data['Delivery']['IsPurgedEncode']:
					print('Purged stream, getting purged encode')
					embeddedurlmatches = re.match(r'.*src="(.*?)".*', data['EmbedUrl'],  flags=re.IGNORECASE|re.UNICODE)
					if(embeddedurlmatches):
						embeddedurl = embeddedurlmatches.group(1)
						print(embeddedurl)
						html = conn.get_data(embeddedurl, headers={"Content-Type": "text/plain"}).decode("UTF-8", errors='backslashreplace')
						#print(html)
						videourlmatch = re.search(r'"VideoUrl":"(.*?)"', html,  flags=re.IGNORECASE|re.UNICODE)
						#print(videourlmatch)
						if videourlmatch:
							videourl = videourlmatch.group(1).replace("\\", "")
							#print(videourlmatch.group(1))
							
							StreamHttpUrl = videourl
							StreamUrl = videourl
							StreamTypeName = 'Encoded'
							Tag = 'NoTag'
							PublicIDSafe = norm_fn(videourl)
							#httpurlshort = StreamHttpUrl[:StreamHttpUrl.index("?")]
							#ext = httpurlshort[-3:]
							ext = 'mp4'
							#DownloadUrl = StreamUrl[:StreamUrl.index(".hls")] + '.vsp.' + ext
							#urlshort = StreamUrl[:StreamUrl.index("?")]
							DownloadUrl = processurl(StreamUrl)
							if DownloadUrl != None:
								streamData = {}
								Folder = SessionGroup + '/' + name
								Path = Folder + '/' + Tag + '-' +  StreamTypeName + '-' + PublicIDSafe + '.' + ext
								streamData['PublicID'] = PublicIDSafe
								streamData['Folder'] = Folder
								streamData['Path'] = Path
								streamData['DownloadUrl'] = DownloadUrl
								streamData['Tag'] = Tag
								streamData['StreamTypeName'] = StreamTypeName
								streamData['PurgedEncodeStream'] = True
								session['streams'].append(streamData)
				#else:
				for sessStream in data['Delivery']['Streams']:
					#print(sessStream)
					print('Processing stream: ' + sessStream['PublicID'])
					#StreamHttpUrl = sessStream['StreamHttpUrl']
					StreamUrl = sessStream['StreamUrl']
					StreamTypeName = norm_fn(sessStream['StreamTypeName'])
					Tag = norm_fn(sessStream['Tag'])
					PublicIDSafe = norm_fn(sessStream['PublicID'])
					#httpurlshort = StreamHttpUrl[:StreamHttpUrl.index("?")]
					#ext = httpurlshort[-3:]
					ext = 'mp4'
					#DownloadUrl = StreamUrl[:StreamUrl.index(".hls")] + '.vsp.' + ext
					urlshort = StreamUrl[:StreamUrl.index("?")]
					DownloadUrl = processurl(urlshort)
					if DownloadUrl != None:
						streamData = {}
						for key, item in sessStream.items():
							streamData[key] = item
						
						Folder = SessionGroup + '/' + name
						Path = Folder + '/' + Tag + '-' +  StreamTypeName + '-' + PublicIDSafe + '.' + ext
						streamData['Folder'] = Folder
						streamData['Path'] = Path
						streamData['DownloadUrl'] = DownloadUrl
						streamData['Tag'] = Tag
						streamData['StreamTypeName'] = StreamTypeName
						streamData['PurgedEncodeStream'] = False
						session['streams'].append(streamData)
				return session
			else:
				print('Error, invalid repsonse for session: ' + sessionid)
				if 'ErrorMessage' in data:
					print('Reason given: ' + data['ErrorMessage'])
				#print(data)
				return None
		else:
			return None

	def GetSessionsInfo(self, records):
		to_print_d('Getting Session Info')
		global queueLock, workQueue, SessionsInfo, SessionsMeta, groupsfile, threads
		
		if not os.path.exists(cachefolder) and os.path.exists(seshfile):
			window.add_txt('old seshfile processing')
			OldSeshfile = self.json_file(seshfile)
			if not isinstance(OldSeshfile, str) and len(OldSeshfile) > 0:
				numSessions = 0
				for key, group in OldSeshfile.items():
					window.add_txt('old seshfile group: ' + key + ', num sessions: ' + str(len(group)))
					numSessions += len(group)
				
				window.add_txt('number of old seshfile sessions: ' + str(numSessions))
				save_cache(OldSeshfile, 0)
				
		SessionsMeta = self.get_stored_metadata(csvfile)
		
		# for entry in os.scandir(cachefolder):
			# if entry.is_file() and entry.path.endsWith('.json') and entry.name.startsWith('cache'):
				# window.add_txt('loading: ' + entry.name)
				# print('loading: ' + entry.name)
				
		
		queueLock.acquire()
		for groupid, sessionids in records.items():
			grouplist = list(sessionids)
			group = self.groups[groupid]
			window.add_txt('Adding to queue for Group: ' + group['Name'])
			rowdata = (group['Name'], "Excluded")
			if group_included(group['Name']):
				rowdata = (group['Name'], "Included")
			window.add_node('tree1', iid=groupid, text='', row=rowdata, index='end')
			SessionsInfo[groupid] = {}
			cachePath = cache_fldr(groupid);
			window.add_txt('Checking for group cache: ' + cachePath)
			cacheGroup, cacheVer = self.get_cached_sessions(cachePath)
			window.add_txt('Number of cached sessions: ' + str(len(cacheGroup)))
			
			for sessionidtmp in sessionids:
				sessionid = sessionidtmp['DeliveryID']
				sessionindex = len(grouplist) - grouplist.index(sessionidtmp)
				window.add_txt('Session: ' + sessionid + ": ", end="")
				
				if sessionid in cacheGroup:
					SessionCached = cacheGroup[sessionid]
					if cacheVer >= 4.0:
						window.add_txt('Using previous data')
						if sessionid in SessionsMeta:
							for key, value in SessionsMeta[sessionid].items():
								if key in SessionCached:
									SessionCached[key] = value
						SessionsInfo[groupid][sessionid] = SessionCached
						add_session_row(SessionCached, groupid)
					else:
						window.add_txt('Updating cache from old version')
						workQueue.put({'GetSession': {'sessionid':sessionid, 'groupid':groupid, 'sessionindex':sessionindex, 'cachedData': cacheGroup[sessionid]}})	
				else:
					output = 'Not cached, Using new data'
					window.add_txt(output)
					workQueue.put({'GetSession': {'sessionid':sessionid, 'groupid':groupid, 'sessionindex':sessionindex}})		
		queueLock.release()
		window.add_txt('Processing queue')
		
	def get_cached_sessions(self, path):
		window.add_txt('Checking for cached data downloaded')
		previousData = self.json_file(path)
		data = {}
		preVersion = 0
		if 'data' in previousData:
			data = previousData['data']
		if 'version' in previousData:
			preVersion = previousData['version']
			
		return data, preVersion
	
	def get_stored_metadata(self, path):
		window.add_txt('Checking for custom metadata')
		metaData = self.csv_file(path)
		return metaData

	def json_file(self, path):
		data = {}
		if os.path.exists(path):
			window.add_txt('Decoding json ' + path)
			with open(path, "r") as text_file:
				data=text_file.read()
				if data.strip() != "":
					data = json.loads(data)
		return data
		
	def csv_file(self, path):
		data = {}
		if os.path.exists(csvfile):
			window.add_txt('Decoding csv ' + path)
			with open(csvfile, "r") as csv_file:
				fieldnames=['StartTime', 'SessionName','SessionAbstract','SessionID']
				csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
				for row in csv_reader:
					if row['SessionID'] != "" and row['SessionID'] != "SessionID":
						StartTime = time.mktime(datetime.datetime.strptime(row['StartTime'], '%Y-%m-%d %H-%M').timetuple())
						data[row['SessionID']] = {'StartTime':StartTime,'SessionName':row['SessionName'], 'SessionAbstract':row['SessionAbstract']}
		return data

	def decode_json(self, string):
		data = json.loads(string)
		return data

	def decode_gzip(self, data_bytes):
		try:
			data_decompressed=zlib.decompress(data_bytes, zlib.MAX_WBITS|16)
			data = data_decompressed.decode("utf-8")
			return data
		except zlib.error as e: 
			print(f'zlib.error: {e}')
			return None

def add_session_row(sessionInfo, groupid):
	logging.info(json.dumps(sessionInfo))
	#print(groupid)
	SessionID = str(sessionInfo['SessionID'])
	SessionName = str(sessionInfo['SessionName'])
	SessionAbstract = str(sessionInfo['SessionAbstract'])
	if float(sessionInfo['StartTime']) > 0:
		StartTime = datetime.datetime.fromtimestamp(float(sessionInfo['StartTime'])).strftime('%Y-%m-%d %H-%M')
	else:
		StartTime = ""
	Duration = str(int(float(sessionInfo['Duration'])/60)) + 'mins'
	streams = len(sessionInfo['streams'])
	row = (SessionName,SessionAbstract,StartTime,Duration,streams)
	window.add_node('tree1', iid=SessionID, parent=groupid, text=SessionID, row=row)


def to_print_d(inputstr, widget="output"):
	to_print(inputstr, widget, date=True)

def to_print(inputstr, widget="output", date=False):
	global win_outputs
	if not widget in win_outputs:
		win_outputs[widget] = []
	timesmp = ""
	if date:
		timesmp = time.strftime('%y-%m-%d %H:%M:%S') + " "
	win_outputs[widget].append( timesmp + inputstr)

def jsontofile(file, data):
	with open(file, "w") as text_file:
		window.add_txt('Dumping JSON Data for ' + file)
		encodedinfo = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
		window.add_txt('Writing JSON Data')
		text_file.write(encodedinfo)

def csvtofile(file, data):
	with open(file, 'w') as csv_file:
		fieldnames=['StartTime', 'SessionName','SessionAbstract','SessionID', 'SessionGroup']
		csv_writer = csv.DictWriter(csv_file, dialect='excel', fieldnames=fieldnames, lineterminator='\n')
		window.add_txt('Dumping CSV')
		csv_writer.writeheader()
		for groupname, group in data.items():
			for sessionid, session in group.items():
				StartTime = '2000-01-01 00-00'
				if float(session['StartTime']) > 0:
					StartTime = datetime.datetime.fromtimestamp(float(session['StartTime'])).strftime('%Y-%m-%d %H-%M')
				csv_writer.writerow({'SessionID': sessionid, 'StartTime': StartTime, 'SessionName': session['SessionName'], 'SessionAbstract': session['SessionAbstract'], 'SessionGroup': session['SessionGroup']})


def save_cache(records, ver):
	chkflexst(cachefolder)
	for group, record in records.items():
		cache = {
			'version': ver,
			'data': record,
		}
		
		jsontofile(cache_fldr(group), cache)

def cache_fldr(group):
	return f'{cachefolder}/gcache-{group}.json'

def processurl(url):
	print(url)
	matcheswmv = re.match( r'(.*)\.wmv', url)
	if matcheswmv:
		return processwmv(matcheswmv)

	else:
		matcheshls = re.match( r'(.*\.hls)', url)
		if matcheshls:
			return maxbrhls(matcheshls)
		else:
			return url

def processwmv(matches):
	return None

def maxbrhls(matches):
	url = matches.group(1)
	print(f'attempting to access {url}')
	html = urllib.request.urlopen(url + '/master.m3u8').read()
	string =  html.decode("UTF-8").strip()
	data = string.strip().splitlines()
	#print(data)
	maxbitrate = 0 
	maxurlapp = "xx"
	for index, item in enumerate(data):
		#print(item)
		match = re.match(r'.*BANDWIDTH\=(\d+),.*', item,  flags=re.IGNORECASE|re.UNICODE)
		if match:
			#print(match.group(1))
			#print(data[index+1])
			bitrate = int(match.group(1))
			if bitrate > maxbitrate:
				maxbitrate=bitrate
				maxurlapp= data[index+1]
				print(maxbitrate)
	if maxurlapp != "xx":
		maxbitrateurl = url + '/'  + maxurlapp
		to_print_d(maxbitrateurl)
		return maxbitrateurl
	else:
		print(f'Error processing bitrate of {url}')
		window.add_txt(f'Error processing bitrate')
		return url

def json2ts(string):
	timestamp = ""
	match = re.search(r"Date\((\d+)(\d{3})\)", str(string))
	if match:
		timestamp = match.group(1) + "." +  match.group(2)
	return timestamp

def win2unixts(wints):
	timestamp = ""
	match = re.search(r"(\d+).(\d+)", str(wints))
	if match:
		integers = int(match.group(1))-11644473600
		timestamp = str(integers) + "." +  match.group(2)
	return timestamp

def regexgroup(group):
	group_regex = r"^.*?\:\s(\d{2})\/(\d{2})\-(.*)"
	if group:
		match = re.match(group_regex, group)
		if match:
			group = match.group(1) + '-' + match.group(2) + ' ' + match.group(3)
	else:
		group = "Miscellaneous"
	return group

def fixsessionname(name, group, sessionindex):
	newname = gp_year = gp_module = gp_title = ""
	group_split_regex = r"^(\d{2})\-(\d{2})\s(\w{2}\d{4})\s(.*)"
	date_regex = r"([\d]{2,4}[\/\\\-\.]\d{2}[\/\\\-\.]\d{2,4})"
	if name:
		newname = re.sub(date_regex, "", name)
		groupmatch = re.match(group_split_regex, group)
		if groupmatch:
			gp_year1 = groupmatch.group(1) +"-"+groupmatch.group(2)
			gp_year2 = groupmatch.group(1) +"/"+groupmatch.group(2)
			gp_year3 = groupmatch.group(1) + groupmatch.group(2)
			gp_module, gp_title= groupmatch.group(3), groupmatch.group(4)
			
			newname = newname.replace(gp_year1, "").replace(gp_year2, "").replace(gp_year3, "").replace(gp_module, "").replace(gp_title, "")
		newname = re.sub(r"^\s*\-\s*", "", newname)
		newname = re.sub(r"\s+", " ", newname.strip())
		if newname != None and newname != "" and re.sub(r"[^\w]", "", newname) != "":
			if newname == "Lecture":
				return f'Lecture {sessionindex}'
			elif newname == "Tutorial":
				return f'Tutorial {sessionindex}'
			else:
				return newname
		else:
			return f'Session {sessionindex}'
	else:
		return f'Session {sessionindex+1}'
		
def norm_fn(inp):
	string = str(inp)
	string = re.sub('[\[]', '(', string)
	string = re.sub('[\]]', ')', string)
	string = re.sub('[^\w\,\(\)_\.:\-\s\\//]', '_', string)
	string = re.sub('[\\//\.:]', '-', string)
	return string

def chkflexst(fl):
	if not os.path.exists(fl):
		os.makedirs(fl)


def read_csv(loc):
	output = []
	window.add_txt("getting csv data")
	with open(loc, 'r') as theFile:
		reader = csv.DictReader(theFile)
		for row in reader:
			output.append(row)
	return output

def write_csv_dict(loc, listdict, headers):
	window.add_txt("writing csv data")
	if os.path.exists(loc):
		shutil.move(loc, loc + ".old")
	with open(loc, 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, dialect='excel', quoting=csv.QUOTE_ALL, fieldnames=headers)
		writer.writeheader()
		for row in listdict:
			writer.writerow(row)

def ffmpegprog(args, thread="output", name=""):
	global processes
	progfn = 'ffmpeg.exe'
	to_print("ffmpeg processing " + name, widget=thread + '-ffmpeg')
	with subprocess.Popen([progfn]+shlex.split(args), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
		processes.append(proc)
		to_print_d(str(proc.communicate()), widget=thread + '-ffmpeg')
	to_print("ffmpeg stopped", widget=thread + '-ffmpeg')
	#process = subprocess.Popen([progfn]+shlex.split(args), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#processes.append(process)
	#while process.poll():
	#	time.sleep(5)
	#subprocess.call([progfn]+shlex.split(args))

def gen_date_strs(datetimets):
	date="?"
	YearStr=""
	DateStrSave=""
	DateStrMeta=""
	DateStrUser=""
	if datetimets > 0:
		date = datetime.datetime.fromtimestamp(datetimets)
		YearStr = date.strftime('%Y')
		DateStrSave = date.strftime('%Y-%m-%d %H-%M')
		DateStrMeta = date.strftime('%Y-%m-%d %H:%M:%S')
		DateStrUser = date.strftime('%Y-%m-%d %H:%M:%S')

	return YearStr, DateStrSave, DateStrMeta, DateStrUser

def gen_dwnld_fn(DateStrSave, session):
		#name = date.strftime('%Y-%m-%d') + ' ' + session
	name = f'{DateStrSave} - {session}'
	return name

def get_download_locs(group, name):
	x265_loc, raw_loc, meta_loc, sources_loc = get_download_flrs(group)
	fn_compress = x265_loc + name + '.mp4'
	fn_raw = raw_loc + name + '.mp4'
	fn_meta = meta_loc + name + '.meta'
	fn_slides = sources_loc + name + '.source'
	return fn_raw, fn_compress, fn_meta, fn_slides

def check_download_flrs(group):
	x265_loc, raw_loc, meta_loc, sources_loc = get_download_flrs(group)

	#chkflexst(x265_loc)
	chkflexst(raw_loc)
	chkflexst(meta_loc)
	chkflexst(sources_loc)

def get_download_flrs(group):
	global basedir
	group_norm = norm_fn(group)
	locbasedir = basedir
	if basedir != "":
		locbasedir += "/"
	x265_loc = locbasedir + group_norm + ' (x265)/'
	raw_loc = locbasedir + group_norm + '/'
	meta_loc = locbasedir + 'metadata/' + group_norm + '/'
	sources_loc = locbasedir + 'sources/' + group_norm + '/'
	return x265_loc, raw_loc, meta_loc, sources_loc

def group_included(group):
	global excluded_groups, only_groups
	included = False
	#print(group.lower(), excluded_groups)
	if (len(only_groups) > 0 and group in only_groups) or (len(only_groups) < 1 and group not in excluded_groups):
		included = True
	return included


def get_session(file):
	path = os.path.dirname(file)
	videoname = os.path.basename(path)
	grouppath = os.path.dirname(path)
	groupname = os.path.basename(grouppath)
	files = []
	for f in os.listdir(path):
		if os.path.isfile(os.path.join(path, f)):
			fpath = path + '/' +f
			files.append({'path':fpath, 'name':f})
	return {'name':videoname, 'path':path, 'group':groupname, 'grouppath':grouppath, 'media':files}

def aquire_sessions(groups):
	global  queueLock, workQueue, threads, conn
	queueLock.acquire()
	for groupid, sessions in groups.items():
		group = conn.groups[groupid]['Name']
		for sessionid, session in sessions.items():
			if group_included(group):
				check_download_flrs(group)
				workQueue.put({'aquire_session': session})
	queueLock.release()

def compress_sessions(groups):
	global excluded_groups, queueLock, workQueue, threads
	queueLock.acquire()	
	for groupid, sessions in groups.items():
		group = conn.groups[groupid]['Name']
		for sessionid, session in sessions.items():
			if group_included(group):
				check_download_flrs(group)
				workQueue.put({'compress_session': session})
	queueLock.release()

def aquire_session(sessiondec, thread="output"):

	global defaultOptions, targets
	
	session = sessiondec['SessionName']
	group = sessiondec['SessionGroup']
	media = sessiondec['streams']
	datetimets = float(sessiondec['StartTime'])
	print(f'session: {session}, datetimets:  {datetimets}')
	date = datetime.datetime.fromtimestamp(datetimets)
	chaptersraw = sessiondec['Timestamps']
	abstract = sessiondec['SessionAbstract']
	duration = sessiondec['Duration']
	
	
	if 'Owner' in sessiondec:
		author = sessiondec['Owner']
	else :
		if 'Contributors' in sessiondec and len(sessiondec['Contributors']) > 0:
			author = sessiondec['Contributors'][0]['DisplayName']
		else:
			author = defaultOptions['author']
		
	

	YearStr, DateStrSave, DateStrMeta, DateStrUser = gen_date_strs(datetimets)

	name = gen_dwnld_fn(DateStrSave, session)

	fn_raw, fn_compress, fn_meta, fn_slides = get_download_locs(group, name)

	if not (os.path.exists(fn_raw)):
		to_print_d('Aquiring Session: ' + name, widget=thread)
		outloc = ""
		#chaptertemp = "ffmetatemp"+thread+".data"
		#outname = "test-" + name + ".mp4"
		title = f'{session} ({DateStrUser})'
		metadata = {"title":title, "Commercial_name":author,  "artist":author, "author":author, "album_artist":author, "publisher": author, "copyright": author, "grouping":group, "year":YearStr, "comment":"Created by PanoCap", "genre":"Educational", "tags":"Educational", "synopsis":abstract, "description":abstract, "synopsis":abstract, "creation_time":DateStrMeta, "DateTimeOriginal":DateStrMeta, "DateTime":DateStrMeta, "date":DateStrMeta, "episode_id": DateStrMeta, "show":group}

		#args = '-i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 -map 0 -map 1 -map 2 -map 3 -metadata:s:v:0 title=Cover -metadata:s:a:0 language=eng -t 30 -c:v copy  -c:a copy a.mp4'
		args_pre = args_i = args_map = args_v_meta = args_output = args_aud = args_other = ""
		count = 0
		
		slides = []
		
		with open(fn_slides, "w") as text_file:
			to_print_d('writing slide data to: ' + fn_slides, widget=thread)
			chapterno = 1
			lastusedindex = 0
			lastusedtitle = ""
			
			for index, slide in enumerate(chaptersraw):
				if ('ObjectIdentifier' in slide and 'ObjectSequenceNumber' in slide):
					slideID = slide['ObjectIdentifier']
					slideNum = slide['ObjectSequenceNumber']
					
					imageUrl = "file '" + targets['urltarget'] + "/Pages/Viewer/Image.aspx?id=" + slideID + "&number=" + slideNum + "'"
					
					
					startts = float(slide['Time'])
					
					if index == 0:
						startts = 0
					if index+1 == len(chaptersraw):
						endts = startts + 0.1
					else:
						endts = float(chaptersraw[index+1]['Time'])
					
					imageDuration = "duration " + str(endts - startts)
					
					slides.append({'url' : imageUrl, 'duration' : imageDuration})

			output = ""
			if len(slides) > 0:
				
				for slide in slides:
					output += slide['url'] + '\n'
					output += slide['duration'] + '\n'
				output += slides[len(slides)-1]['url'] #Due to a quirk, the last image has to be specified twice - the 2nd time without any duration directive) 
				
				
			text_file.write(output.encode('ascii','ignore').decode())
				
		
		if len(slides) > 0:
			args_i += ' -safe 0 -protocol_whitelist file,http,https,tcp,tls -f concat -i "' + fn_slides + '"'
			args_map += ' -map ' + str(count) + 'v:0'
			args_v_meta += ' -metadata:s:v:' + str(count) + ' title="Slides"'
			args_v_meta += ' -metadata:s:v:' + str(count) + ' language=eng'
			count +=1
		
		for file in media:
			streamtype = file['StreamTypeName']
			if (streamtype in StreamTypes):
				streamtype = StreamTypes[streamtype]

			args_i += ' -i "' + file['DownloadUrl'] + '"'
			args_map += ' -map ' + str(count)
			args_v_meta += ' -metadata:s:v:' + str(count) + ' title="' + streamtype + ' - ' + file['PublicID'] + '"'
			args_v_meta += ' -metadata:s:v:' + str(count) + ' language=eng'
			count +=1
		
		with open(fn_meta, "w") as text_file:
			to_print_d('writing chapter data to: ' + fn_meta, widget=thread)
			chapterno = 1
			lastusedindex = 0
			lastusedtitle = ""
			output = ";FFMETADATA1\n"
			for key, value in metadata.items():
				output += str(key) + '=' + str(value) + '\n'
			chapters = []
			for chapter in chaptersraw:
				startts = float(chapter['Time'])
				titletemp=""
				if chapter['Caption']:
					titletemp=re.sub(r'[\t\s]{2,}', ' ', re.sub(r'[\n\r]', ' ', chapter['Caption'].strip()))
				chapters.append({'start':startts, 'title':titletemp})
			lengthchap = len(chapters)
			for index, chapter in enumerate(chapters):
				
				startts = chapter['start']
				if index == 0:
					if startts > 30:
						output += "[CHAPTER]\nTIMEBASE=1/1000\n"
						output += "START=0\nEND=" + str(int(startts*1000))  + "\ntitle=" + "Chapter 0\n"
					else:
						startts = 0
				
				if index == 0 or (startts - chapters[lastusedindex]['start'] >= 30):
					if index != 0:
						output += "END=" + str(int(startts*1000)) + "\n" + lastusedtitle
					title = "Chapter " + str(chapterno)
					if chapter['title'] != "":
						title += " - " + chapter['title']
					output+= "[CHAPTER]\nTIMEBASE=1/1000\n"
					output += "START=" + str(int(startts*1000)) + "\n"
					chapterno+=1
					lastusedtitle = "title=" + title + "\n" 
					lastusedindex = index
				if index+1 == lengthchap:
					output += "END=" + str(int(duration*1000)) + "\n" + lastusedtitle
			text_file.write(output.encode('ascii','ignore').decode())
		
		
		
		args_i += ' -i "' + fn_meta + '"'
		args_v_meta += ' -map_metadata ' + str(count)
		#args_pre += "-y -hwaccel cuvid -c:v h264_cuvid"
		args_aud += " -metadata:s:a:0 language=eng"
		args_codec = " -c:v copy  -c:a copy"
		#args_processed = " -codec:a aac -c:v libx265 -crf 20 -preset fast"
		#args_other += " -codec:a aac -c:v libx265"
		#args_other += " -codec:a aac -c:v h264_nvenc -preset slow"
		if istest:
			args_other += " -t 30"
		
		args_output = ' "' +  fn_raw + '"'
		args = args_pre + args_i + args_map + args_v_meta + args_aud + args_codec + args_output

		#to_print_d(args, widget=thread)
		logging.debug(args)
		to_print_d('Downloading Raw Video: ' + name, widget=thread)
		ffmpegprog(args, thread, name)
		to_print_d('Finished: ' + name, widget=thread)
		netdir = netloc + group + '/' + name + '.raw.mp4'
		#shutil.copy2(fn_raw, netdir)
 		
	else:
		to_print_d("Already exsists: " + name, widget=thread)

def compress_session(sessiondec, thread="output"):
	session = sessiondec['SessionName']
	group = sessiondec['SessionGroup']
	media = sessiondec['streams']
	datetimets = float(sessiondec['StartTime'])
	date = datetime.datetime.fromtimestamp(datetimets)
	chapters = sessiondec['Timestamps']
	abstract = sessiondec['SessionAbstract']
	duration = sessiondec['Duration']

	YearStr, DateStrSave, DateStrMeta, DateStrUser = gen_date_strs(datetimets)

	name = gen_dwnld_fn(DateStrSave, session)

	fn_raw, fn_compress, fn_meta, fn_slides= get_download_locs(group, name)

	if os.path.exists(fn_compress) and os.path.getsize(fn_compress) < 100000000:
		os.remove(fn_compress)

	if not (os.path.exists(fn_compress)):
		#args = '-i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 -map 0 -map 1 -map 2 -map 3 -metadata:s:v:0 title=Cover -metadata:s:a:0 language=eng -t 30 -c:v copy  -c:a copy a.mp4'
		args_pre = args_i = args_map = args_meta = args_v_meta = args_output = args_aud = args_codec = ""
		count = 0
		
		args_codec = " -codec:a aac -c:v libx265 -crf 18 -preset fast"
		#args_other += " -codec:a aac -c:v libx265"
		#args_other += " -codec:a aac -c:v h264_nvenc -preset slow"
		args_i = ' -i "' +  fn_raw + '"'
		args_output = ' "' +  fn_compress + '"'
		args_i += ' -i "' + fn_meta + '"'
		args_map += ' -map 0'
		args_v_meta += '-map_metadata:s:v 0:s:v' # copies video stream metadata from input 1 to output
		args_v_meta += '-map_metadata:s:a 0:s:a' # copies audio stream metadata from input 1 to output
		args_v_meta += ' -map_metadata 1'
		args = args_pre + args_i + args_map + args_meta + args_codec + args_output

		logging.debug(args)
		to_print_d('Processing Raw Video: ' + name, widget=thread)
		ffmpegprog(args, thread, name)
		to_print_d('Finished: ' + name, widget=thread)
		#netdir = netloc + "\\" + group + '\\' + name + '.raw.mp4'
		#shutil.copy2(fn_raw, netdir)
	else:
		to_print_d("Already exsists: " + name, widget=thread)

def ffmpegexst():
	if not os.path.exists("ffmpeg.exe"):
		window.add_txt("downloading ffmpeg")
		getffmpeg()

def getffmpeg():
	window.add_txt('No ffmpeg, downloading')
	url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
	window.add_txt('Downloading: ' +url)
	
	timeout = 30
	req = urllib.request.Request(url=url)
    
	try:
		resp = urllib.request.urlopen(req, timeout=timeout)
        
		window.add_txt("Downloaded ")
		print("Downloaded " + resp.url)
		try: 
			#extractffmpeg7z(resp.read())
			extractffmpegzip(resp.read())
			#extractffmpegtar(resp.read())
		except tarfile.ReadError as e:
			print('tarfile ReadError: ' + str(e))
			window.add_txt('tarfile ReadError: ' + str(e))
			getffmpegbackup()
		
	except urllib.error.HTTPError as e:
		window.add_txt('HTTPError: ' + str(e.code))
		getffmpegbackup()
	except urllib.error.URLError as e:
		window.add_txt('URLError: ' + str(e.reason))
		getffmpegbackup()
	except socket.timeout as e:
		window.add_txt('Timeout: ' + str(e.reason))
		getffmpegbackup()

def getffmpegbackup():
	window.add_txt('Trying backup due to error')
	url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2020-11-03-12-33/ffmpeg-N-99830-g112fe0ff19-win64-gpl.zip"
	window.add_txt('Downloading: ' +url)
	
	timeout = 30
	
	req = urllib.request.Request(url=url)
	try: 
		resp = urllib.request.urlopen(req, timeout=timeout)
		window.add_txt("Downloaded ")
		print("Downloaded " + resp.url)
		extractffmpegzip(resp.read())
	except urllib.error.HTTPError as e:
		print('HTTPError: ' + str(e.code))
		window.add_txt('HTTPError: ' + str(e.code))
		exit()
	except urllib.error.URLError as e:
		print('URLError: ' + str(e.reason))
		window.add_txt('URLError: ' + str(e.reason))
		exit()
	except socket.timeout as e:
		print('Timeout: ' + str(e.reason))
		window.add_txt('Timeout: ' + str(e.reason))
		exit()
def extractffmpegzip(binFile):
	targetdir = "/bin/"
	window.add_txt("Accessing ZIP")
	with zipfile.ZipFile(io.BytesIO(binFile)) as zip:
		window.add_txt("Searching ZIP")
		for contained_file in zip.namelist():
			if targetdir in contained_file and  '.exe' in contained_file:
				window.add_txt("Processing: " + contained_file)
				zip.extract(member=contained_file, path='tmp')
				shutil.move('tmp/' + contained_file, os.getcwd())
		shutil.rmtree('tmp')
	window.add_txt("Extraction complete")

def extractffmpegtar(binFile):
	targetdir = "/bin/"
	window.add_txt("Accessing tarfile")
	with tarfile.open(mode='r|xz', fileobj=io.BytesIO(binFile)) as tar:
		window.add_txt("Searching tarfile")
		print(tar.getmembers())
		for contained_file in tar.getmembers():
			print(contained_file)
			if targetdir in contained_file and  '.exe' in contained_file:
				tar.extract(member=contained_file)
				shutil.move(contained_file, os.getcwd())
		#shutil.rmtree('tmp')
		
# def extractffmpeg7z(binFile):
	# filter_pattern = re.compile(r'.*/bin/.*')
	# window.add_txt("Accessing SevenZipFile")
	# with py7zr.SevenZipFile(io.BytesIO(binFile), 'r') as archive:		
		# allfiles = archive.getnames()
		# window.add_txt("Searching SevenZipFile")
		# selective_files = [f for f in allfiles if filter_pattern.match(f)]
		# print(selective_files)
		# archive.extract(targets=selective_files)
	
def createthreads(amount):
	threads = []
	for i in range(amount):
		thread = threaders(i, "Thread-"+str(i))
		thread.start()
		threads.append(thread)
	return threads


def get_settings(configloc):
	print("Looking for Config File")
	if not os.path.exists(configloc):
		default_settings(configloc)
	print("Loading config file")
	config = configparser.ConfigParser(allow_no_value=True)
	config.read(configloc)
	for key, section in defaults.items():
		if key in config:
			settings[key]={}
			for setting, value in section.items():
				if setting in config[key]:
					settings[key][setting]=config[key][setting]
				else:
					settings[key][setting]=value
		else:
			settings[key]=section
	write_settings(settings, configloc)

def default_settings(configloc):
	global defaults
	print("First time run, setting defaults")
	write_settings(defaults, configloc)

def write_settings(config_dict, configloc):
	config = configparser.ConfigParser(allow_no_value=True)
	for key, group in config_dict.items():
		config[key] = group
	with open(configloc, 'w') as configfile:
		config.write(configfile)

global defaults, settings

defaults={}
settings={}
defaults['Targets'] = {'urltarget': 'https://cardiff.cloud.panopto.eu/Panopto'}
defaults['Directories'] = {'basedir': 'C:/streams',
						 'netloc': '//server/unimplemented',
						 'seshfile': 'sessionstore.json',
						 'cachefolder': 'cache',
						 'groupsfile': 'groupstore.json',
						 'csvfile': 'session_meta.csv',
						 'logfile': 'debug.log'}
defaults['Cookies'] = {'ASPXAUTH': '', 'yourid': ''}
defaults['Defaults'] = {'author': 'Default Author'}

excluded_groups_data =["Getting Started with Panopto", "Featured Videos - Panopto Homepage (Not open links)"]
defaults['Modifiers']= {'group_regex': r"^.*?\:\s(\d{2})\/(\d{2})\-(.*)", 'excluded_groups': json.dumps(excluded_groups_data), 'only_groups': "[]", 'excluded_session_ids': "[]"}
defaults['Settings'] = {'istest':False, 'num_treads': 3, 'queueLength':1000}
defaults['StreamTypes'] = {'Archival': 'Camera', 'Streaming':'Projector', 'Encoded':'Encoded'}

global targets, basedir, netloc, excluded_groups, only_groups, group_regex, istest, defaultOptions, window, queueLock, exitFlag, pauseFlag, csvfile, cachefolder, groupsfile, workQueue, threads, win_outputs, SessionsInfo, processes

get_settings(settingsfl)
#print (settings)

targets = settings['Targets']
basedir = settings['Directories']['basedir']
netloc = settings['Directories']['netloc']
seshfile = settings['Directories']['seshfile']
cachefolder = settings['Directories']['cachefolder']
groupsfile = settings['Directories']['groupsfile']
csvfile = settings['Directories']['csvfile']
logfile = settings['Directories']['logfile']

group_regex = settings['Modifiers']['group_regex']
excluded_groups = json.loads(settings['Modifiers']['excluded_groups'])
only_groups = json.loads(settings['Modifiers']['only_groups'])
excluded_session_ids = json.loads(settings['Modifiers']['excluded_session_ids'])


istest = bool(settings['Settings']['istest'])
num_treads = int(settings['Settings']['num_treads'])
queueLength = int(settings['Settings']['queueLength'])

StreamTypes = settings['StreamTypes']

defaultOptions = settings['Defaults']

logging.basicConfig(filename=logfile,level=logging.DEBUG)

title = "PanoCap v" + str(version) + " " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

win_outputs = {}
exitFlag = pauseFlag = 0

queueLock = threading.Lock()
workQueue = queue.Queue(queueLength)
SessionsInfo = {}
processes =[]

python_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(python_path)

cafileMain = certifi.where()

threads = createthreads(num_treads)


window = gui(title)
window.add_txt('Welcome!\n')


ffmpegexst()
	
#if len(sys.argv) <= 1 :	
#	window.setup_next_stage()
#else:
#	arg = sys.argv[1]
#	if arg == "call_compress_sessions" or arg == "call_aquire_sessions":
#		window.arg = arg
#		window.setup_auto()
#		
#	else:
#		window.setup_next_stage()

window.main.mainloop()

exitFlag = 1
