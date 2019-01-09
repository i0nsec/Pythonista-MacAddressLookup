import ui, dialogs, sys
import sqlite3
from random import randint
from console import hud_alert
from clipboard import set as Set_

"""
App by: Eric @i0nsec
App Version: 1.0
Last updated: 11-18-2017
Database Version: 06102017
"""

Copy = False

def GEN_LOG(err_msg):
	
	# Log errors to a log file
	try:
		with open('ERR_LOG', 'a') as LOG_F:
			LOG_F.write(str(err_msg)+'\n')
	except Exception as ERR:
		with open('ERR_LOG', 'a') as LOG_F:
			LOG_F.write('ERROR LOG FILE:'+str(ERR))
		

def __Main__(sender):
	global Copy
	
	# main function for everything
	# Getting user input
	user = sender.superview['user-input'].text
	if not user:
		sys.exit()
	ml = sender.superview['main-label']

	User_1 = user[:8].split(':')
	get_results = ''.join(User_1)
		
	try:
		# Connect to database
		conn = sqlite3.connect('mac.db')
		c = conn.cursor()
		c.execute("SELECT vendor FROM mac_vendors WHERE mac=?", (get_results.upper(),))
		res = c.fetchone()
		ml.text = "{}\n{}".format(str(res[0].strip()), user)
		
		if res:
			Copy = True
			with open('history', 'a') as f:
				f.write(str("{}: {}\n".format(user,res[0].strip())))
	except Exception as err_msg:
		Copy = False
		ml.text = 'UnKnown Vendor'
		GEN_LOG('__Main__'+err_msg)
	
def Copy(sender):
	global Copy
	
	# if Copy is True, copy results to clipboard
	if Copy:
		ml = sender.superview['main-label']
		Set_(ml.text)
		hud_alert('Copied')
	else:
		hud_alert('Nothing to Copy','error')
		
def Clear(sender):
	global Copy
	
	# Clear results
	ml = sender.superview['main-label']
	ml.text = 'Enter Mac Address to lookup'
	user = sender.superview['user-input']
	user.text = ''
	user.placeholder = "XX:XX:XX:XX:XX:XX"
	Copy = False
	
def Generate_mac(sender):
	
	# generate a random mac address
	try:
		user = sender.superview['user-input']
		conn = sqlite3.connect('mac.db')
		c = conn.cursor()
		ran = str(randint(1,22900))
		c.execute("SELECT mac FROM mac_vendors WHERE mac_id=?", (ran,))
		data = c.fetchone()[0]
		res = ':'.join(data[i:i+2] for i in range(0,6,2))
		user.text = str(res)
	except Exception as err_msg:
		GEN_LOG('_Generate_mac'+err_msg)
	
def History(sender):
	
	# if the history file exsist
	data = set([])
	pre_set = []
	try:
		with open('history') as F:
			for i in F.readlines():
				data.add(i)
			for c in data:
				pre_set.append(c)
		Set_(dialogs.list_dialog(title='History', items=pre_set))
		hud_alert('Copied')
	except Exception as err_msg:
		GEN_LOG('_History'+str(err_msg))

def Share(sender):
	
	# if Copy is True, share results
	global Copy
	if Copy:
		ml = sender.superview['main-label']
		dialogs.share_text(ml.text)
	else:
		hud_alert('Nothing to Share','error')
	
v = ui.load_view()
v.background_color = '#005392'
v.present(orientations=['portrait'])
