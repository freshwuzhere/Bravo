# coding: utf-8
# modules required to communicate with Bravo systems

import socket
import time

def send_mess(s,mess):

	# need to generate the checksum and also add /n
	chk_sum = get_checksum('#'+mess+',')
	MESSAGE = '#'+mess+','+ chk_sum + '\n' # str(unichr(13))
	
	print('MESSAGE = ' + MESSAGE)
	
	# now send message

	s.send(MESSAGE)
	
	print ('message sent')
	
	time_out = 1
	total_data = []
	data = ''
	
	begin = time.time()
	print 'begin = ' + str(begin)
	while True:
		#print('in loop')
		if total_data and time.time()-begin >time_out:
			print('exiting 1')
			break
		
		elif time.time()-begin > time_out * 2 :
			print ('exiting 2')
			break
			
		try:
			data = s.recv(20480)
			if data:
				#print('data read = ' + data)
				total_data.append(data)
				begin = time.time()
			else:
				#print ('waiting for more data')
				time.sleep(0.1)
		except:
			pass 

	all_data = ''.join(total_data)

	print ('buffer contents'+str(all_data))
	s.close
	
#	print 'received_data = ' + all_data
	return (all_data)
	
	
def get_checksum(s):
	print('starting s' + s)
	chk_sum = 0
	for j in range(len(s)):
		chk_sum ^= ord(s[j])
		
	str_val = str(hex(chk_sum))	
		
	if len(str_val) == 3:
		str_val =  	str_val[-1:]

	else:
		str_val = str_val[-2:]	
		
	str_val = str_val.zfill(2)
	str_val = str_val.upper()
	print('hex val = ' + str_val)

	return (str_val)
	
def convert_bravo_vars_list_to_dict(var_str):
	
	var_dict = {}
	var_list = var_str.split('\n')
	# print var_list
	for k in var_list:
		if len(k)>3:
			# print('k = ' + str(k))
			var_pair = k[1:].split( ',' )
			# print(str(var_pair))
			var_dict[var_pair[1]]=var_pair[0]
		
	return (var_dict)
	