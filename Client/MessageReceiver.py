# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
	"""
	This is the message receiver class. The class inherits Thread, something that
	is necessary to make the MessageReceiver start a new thread, and permits
	the chat client to both send and receive messages at the same time
	"""

	def __init__(self, client, connection):
		"""
		This method is executed when creating a new MessageReceiver object
		"""

		# Flag to run thread as a deamon
		Thread.__init__(self)
		self.daemon = True
		self.connection = connection
		self.client = client
		self.run()

	def run(self):
		"""
		Creates a loop that listens for new messages.
		"""
		while True:
			received_string = self.connection.recv(4096)
			
			#This will occur when the server closes the connection
			if not received_string:
				self.client.disconnect()
				return
				
			self.client.receive_message(received_string)