# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json
import threading


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
		# TODO: Finish init process with necessary code

	def run(self):
		# Initiate the connection to the server
		print "Welcome! Type in your input"
		self.connection.connect((self.host, self.server_port))
		
		message_sender = threading.Thread(target=self.input_loop)
		message_sender.daemon = True
		message_sender.start()
		
		message_receiver = MessageReceiver.MessageReceiver(self, self.connection)
		message_receiver.start()

	def input_loop(self):
		while True:
			data = raw_input('')
			self.send_payload(data)
	def disconnect(self):
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

	def create_payload(self,command):
		"""
		Creates json of a command.
		"""
		if " " in command:
			request, content = command.split(" ",1)
		else:
			request = command
			content = ""
		data = {"request": request, "content": content}
		return json.dumps(data)

	def parse_message(self,message):
		"""
		Parses message from string format to dictionary. If the payload is an invalid json-format, return None.
		"""
		try:
			return json.loads(message)
		except ValueError:
			return None

	def send_payload(self, data):
		# TODO: Handle sending of a payload
		payload = self.create_payload(data)
		self.connection.sendto(payload, (self.host, self.server_port))


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations is necessary
	"""
	client = Client('localhost', 9998)
