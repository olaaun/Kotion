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
        self.daemon = True
		self.connection = connection
		self.client = client
		self.run()

    def run(self):
        while True:
			received_string = self.connection.recv(4096)
			
			payload = parse_message(received_string)
			timestamp = payload["timestamp"]
			sender = payload["sender"]
			response = payload["response"]
			content = payload["content"]
			
			message = "{1} - {0} [{2}]:\n".format(timestamp,sender,response)
			
			#Make indentation. Split because when respnse = history.
			message = "\t" + "\t\n".join(content.split("\n"))
			
			print message
			
	def parse_message(message):
		"""
		Parses message from string format to dictionary. If the payload is an invalid json-format, return None.
		"""
		try:
			return json.loads(message)
		except ValueError:
			return None