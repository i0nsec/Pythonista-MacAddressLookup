import ui, dialogs, sys, sqlite3
from random import randint
from console import hud_alert
from clipboard import set as Set_

"""
App by: @i0nsec
App Version: 1.0.2
Last updated: 05-08-2020
Database Version: 05082020
"""

copy = False

def log_errs(err_msg):
	# Log errors to a log file
	with open('ERR_LOG', 'a') as f_log:
		f_log.write(str(err_msg)+'\n')

def main(sender):
	global copy
	
	# main function for everything
	user = sender.superview['user-input'].text
	if not user:
		sys.exit()
	ml = sender.superview['main-label']

	user = user[:8].split(':')
	user = ''.join(user)
		
	try:
		# Connect to database
		conn = sqlite3.connect('mac.db')
		c = conn.cursor()
		c.execute("SELECT vendor FROM mac_vendors WHERE mac=?", (user.upper(),))
		res = c.fetchone()
		ml.text = "{}\n{}".format(str(res[0].strip()), user)
		
		if res:
			copy = True
			with open('history', 'a') as f:
				f.write(str("{}: {}\n".format(user, res[0].strip())))
	except Exception as err_msg:
		copy = False
		ml.text = 'UnKnown Vendor'
		log_errs(str(err_msg))
	
def Copy(sender):
	# if copy is True, copy results to clipboard
	global copy
	
	if copy:
		ml = sender.superview['main-label']
		Set_(ml.text)
		hud_alert('Copied')
	else:
		hud_alert('Nothing to copy','error')
		
def Clear(sender):
	# Clear results
	global copy
	
	ml = sender.superview['main-label']
	ml.text = 'Enter Mac Address to lookup'
	user = sender.superview['user-input']
	user.text = ''
	user.placeholder = "XX:XX:XX:XX:XX:XX"
	copy = False
	
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
		log_errs(str(err_msg))
	
def History(sender):
	# if the history file exsist, show its content
	
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
		log_errs(str(err_msg))

def Share(sender):
	# if copy is True, share results
	global copy	

	if copy:
		ml = sender.superview['main-label']
		dialogs.share_text(ml.text)
	else:
		hud_alert('Nothing to Share','error')
	
v = ui.load_view()
v.background_color = '#005392'
v.present(orientations=['portrait'])
