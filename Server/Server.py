# -*- coding: utf-8 -*-
import SocketServer
import json
import servermessage
from validation import *

#Keeps track of running threads.
threads = set()


class History:
	"""
	History keeps track of the messages on the server. The messages are payloads previously sent from the server.
	"""

	def __init__(self):
		"""
		Initializes history with empty list.
		"""
		self.messages = []
	def getMessages(self):
		"""
		Givs the message history. Each entry is a payload.
		"""
		return self.messages
	def add(self, payload):
		"""
		Add a payload to the history.
		"""
		self.messages.append(payload)

hist = History()

class ClientHandler(SocketServer.BaseRequestHandler):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	def disconnect(self):
		"""
		Disconnects a user
		"""
		threads.remove(self)
		self.connection.close()
		return
	def handle(self):
		"""
		This method handles the connection between a client and the server.
		"""
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request
		self.username = None
		
		# Loop that listens for messages from the client
		while True:
			received_string = self.connection.recv(4096)
			payload = parse_message(received_string)
			response = None
			
			#Validate json
			if payload == None:
				response = servermessage.error("The message is invalid json.")
			
			#Validate request
			elif is_invalid_payload(payload):
				response = servermessage.error("The message does not contain the correct fields.")
			#Login
			elif payload["request"] == "login":
				if is_invalid_username(payload["content"]):
					response = servermessage.error("Invalid username. Can only contain characters [A-Z], [a-z] and numbers 0-9")
				elif is_username_taken(threads,payload["content"]):
					response = servermessage.error("Username already taken.")
				else:
					self.username = payload["content"]
					threads.add(self)
					response = servermessage.history(hist)
			#Help
			elif payload["request"] == "help":
				response = servermessage.help()
			elif self.username == None:
				response = servermessage.error("You have to login to write a message.")
			#Logout
			elif payload["request"] == "logout":
				self.disconnect()
				return
			#Msg
			elif payload["request"] == "msg":
				message = servermessage.message(self.username,payload["content"])
				hist.add(message)
				send_to_all_users(self,message)
				continue
			#Names
			elif payload["request"] == "names":
				response = servermessage.users(get_usernames())
			
			else:
				
				raise Exception("Error. Unhandled payloaid: " + str(payload)) #TODO: find out if able to trigger.
			self.connection.sendall(response)

def send_to_all_users(origin,payload):
	"""
	Send response-payload to all user except the sender.
	"""
	for thread in threads:
		if thread == origin:
			continue
		else:
			thread.connection.sendall(payload)
def get_usernames():
	"""
	Returns list of all usernames.
	"""
	return [thread.username for thread in threads]
def parse_message(message):
	"""
	Parses message from string format to dictionary. If the payload is an invalid json-format, return None.
	"""
	try:
		return json.loads(message)
	except ValueError:
		return None
			
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	"""
	This class is present so that each client connected will be ran as a own
	thread. In that way, all clients will be served by the server.

	No alterations is necessary
	"""
	allow_reuse_address = True

if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations is necessary
	"""
	HOST, PORT = 'localhost', 9998
	print('Server running...')

	# Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever()
