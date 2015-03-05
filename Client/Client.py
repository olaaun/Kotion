# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json
import threading
import sys


class Client:
	"""
	This is the chat client class
	"""

	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""

		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.server_port = server_port
		self.run()

	def run(self):
		"""
		Creates connection between client and server. Creates threads that handles receiving and sending of data.
		"""
		# Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		print "Welcome! Type in your input"
		try:
		#Create sender-thread
			message_sender = threading.Thread(target=self.input_loop)
			message_sender.daemon = True
			message_sender.start()

			#Create receiver-thread
			message_receiver = MessageReceiver.MessageReceiver(self, self.connection)
			message_receiver.start()
		except KeyboardInterrupt:
			print "losing"
		finally:
			sys.exit()

	def input_loop(self):
		"""
		Ask the user repeatedly for commands to send to the server
		"""
		while True:
			command = raw_input('')
			self.send_payload(command)
	def disconnect(self):
		"""
		Closes the connection to the server
		"""
		print "disconnecting from server"
		self.connection.close()
		return

	def receive_message(self, message):
		"""
		Recieve_message is used by the MessageReciever-class to handle incoming messages.
		"""
		payload = json.loads(message)

		timestamp = payload["timestamp"]
		sender = payload["sender"]
		response = payload["response"]
		content = payload["content"]

		output = "{1} - {0} [{2}]:\n".format(timestamp, sender, response)

		# Make indentation. Split when response = history.
		output += "\t" + content.replace("\n","\n\t")

		print(output)
	def send_payload(self, command):
		"""
		Parses command and sends the payload to the server.
		"""
		payload = Payload(command)
		self.connection.sendto(str(payload), (self.host, self.server_port))

class Payload:
	"""
	Payload that handles outgoing payloads. The data-field is a dictionary.
	"""
	def __init__(self,command):
		"""
		Put command into payload-object.
		"""
		if " " in command:
			request, content = command.split(" ",1)
		else:
			request = command
			content = ""
		self.data = {"request": request, "content": content}
	def __str__(self):
		"""
		Create json-string from dictionary.
		"""
		return json.dumps(self.data)

if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations is necessary
	"""
	client = Client('localhost', 9998)
