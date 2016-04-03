# coding: utf-8

import ui
import time
import socket
import sys
import math
import io

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

from datetime import datetime
from collections import deque

#from sys import exit
from Bravo_coms import get_checksum
from Bravo_coms import send_mess
from Bravo_coms import convert_bravo_vars_list_to_dict
from Plot_Strip import plot_strip

exitter = False
variables = ['BS','TWA','TWS','AWA']


def timer_loop_action(all_data):
# this teh loop that reads the data then loads teh vvarianbles

#	print( 'IN THE DECODE LOOP' + str(all_data))
	
	rows = all_data.split('\n')
	split_dat = rows[0].split(',')	
	# print ('split_dat = ' + str(split_dat))
	dat = []
	for idx,x in enumerate(split_dat):
		if idx%2 == 0 and idx > 0 :
			dat.append(float(split_dat[idx]))
			
	#print('DAt = ' + str(dat))
	return (dat)

	# print( 'v = ' + str(v))
	
#	lab_1 =	 v['Label1']
#	lab_1.text = 'value = ' + str(i)
#	d1 = v['Data1']
#	d2 = v['Data2']
#	d3 = v['Data3']

	
def button_quit(sender):
	# print('in exit button code')
	global exitter
	exitter = True
	# print('exitter = ' + str(exitter) )
	raise SystemExit
	
def cover0_pressed(sender):
#	print('Button 0 PRESSED')
	global variavbles
	plot_strip( dqt , dq[0], variables[0])
	
def cover1_pressed(sender):
#	print('Button 1 PRESSED')
	global variavbles
	plot_strip( dqt , dq[1], variables[1])
	
def cover2_pressed(sender):
#	print('Button 2 PRESSED')
	global variavbles
	plot_strip( dqt , dq[2], variables[2])
	
def cover3_pressed(sender):
#	print('Button 3 PRESSED')
	global variavbles
	plot_strip( dqt , dq[3],variables[3])

def main():
	v = ui.load_view('Bravo_ui')
	v.present('sheet')
	

	time_count = 120
	
	global exitter
	exitter = False
	
	# ip 10.200.2.3
	server_ip = '10.200.2.3'
	server_port = 4503
	
	TCP_IP= server_ip
	TCP_PORT = server_port
	BUFFER_SIZE = 1024
	
	REAL_DATA = False
	
	if REAL_DATA:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#		print ('TCP_IP = ' + str(TCP_IP) + '-- PORT = ' + str(TCP_PORT))

		s.connect((TCP_IP,TCP_PORT))
		s.setblocking(0)
	
		#chk_sum =get_checksum('VARSLIST')
		#mess = '#VARSLIST,' + str(chk_sum) + '\n'
	
		# chk_sum = get_checksum('PING')
		#mess = '#PING,'+str(chk_sum)+'\n'	
	
		#mess = 'ERROR,CheckSum failed'
		#mess = 'PING'
		mess = 'LISTVARS'
	
#		print ('mess = ' + mess)
	
		var_list = send_mess(s,mess)
		#var_list = '#VARSLIST,6,XX\n#0,TWD,XX\n#1,TWS,XX\n#2,TWA,XX\n#3,AWA,XX\n#4,AWS,XX\n#5,BS,XX,\n'
		var_dict = convert_bravo_vars_list_to_dict(var_list)
	
#		print ('var_dict' + str(var_dict))
	
		# look up the variable names in the list 
		chan = []
		for yy in variables:
			chan.append(var_dict[yy])
	
	
	
	# kill Bravo broadcast on this port
	
		mess = 'DISABLEREFRESHEDVARS'
		var_list = send_mess(s,mess)

		mess = 'CLEARREFRESHEDVARS'
		var_list = send_mess(s,mess)
	
		mess = 'CLEARREMOTEVARS'
		var_list = send_mess(s,mess)
	
	
	
	lab = []
#	print ('setting labels')
	lab.append(v['Label0'])
	lab.append(v['Label1'])
	lab.append(v['Label2'])
	lab.append(v['Label3'])
	
	d = []
	
	d.append(v['Data0'])
	d.append(v['Data1'])
	d.append(v['Data2'])
	d.append(v['Data3'])
	
	#lab[1].text = 'blah blah blah'
	global dq
	dq =[]
	
	global dqt
	dqt = deque(maxlen=time_count)	
	
	for idx in range(len(d)):
		dq.append(deque(maxlen=time_count))
	
	
	for idx,yy in enumerate(variables):
#		print 'yy = ' + yy
		lab[idx].text = yy 
		
		if REAL_DATA:
			var_name = yy
			var_chan = var_dict[yy]
		
			mess = 'SETREFRESHEDVAR,'+str(idx)+','+str(var_name)+','+str(var_name)+','+str(1)
			var_list = send_mess(s,mess)
	
			mess = 'ENABLEREFRESHEDVARS,1.0' # NOTE frequency = 1 Hz
			var_list = send_mess(s,mess)
	
#	mess = 'LISTREFRESHEDVARS'
#	var_list = send_mess(s,mess)
	

	data = ''
	
	looper = 1
	time_out = 0.5
	while True:
		#print(str(exitter))
		if exitter:
			#print('in exitter code')
			v.close()
			raise SystemExit
			break
		total_data = []		
		all_data = []
		begin = time.time()
		while True:
			if total_data and time.time()-begin > time_out:
				#print ('exiting 1')
				break
			elif time.time()- begin > 3 * time_out :
				#print('exiting 2')
				break
				
			try:
				if REAL_DATA:
					data = s.recv(2048)
#					print('data = '+ data)
					if data:	
						total_data.append(data)
						begin = time.time()
						break
					else:
						time.sleep(0.1)
				else:
					var0 = looper * 1.2
					var1 = looper/0.3445
					var2 = looper * looper
					var3 = looper +looper
					total_data = '#SV,0,'+str(var0)+',1,'+str(var1)+',2,'+str(var2)+',3,'+str(var3)+',A6\n'
					looper = looper +1
					if looper >11:
						looper = 1	
			except:	
				pass
			
		all_data = ''.join(total_data)	
#		print ('this is the recieved biffer data ' + str(all_data))
	
#		print('out of loop ')		
		
		if len(all_data)>0:  # this is the place where the data is marshalled and orgainsed then used.
			data_arr = timer_loop_action(all_data)
#			print ('length all_data = ' + str(len(all_data)))
			
			time_now = datetime.now()
			dqt.append(time_now)			
			for idx, xx in enumerate(data_arr):
				dq[idx].append(data_arr[idx])
				d[idx].text =  "{0:.1f}".format(data_arr[idx]) 
		
		time.sleep(0.5)
		
		#Now update the buffers for plotting
		
	

if __name__ == '__main__':
	main()