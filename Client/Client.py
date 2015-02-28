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
        self.host=host
        self.server_port=server_port
        self.run()
        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        message_receiver = MessageReceiver(self, self.connection)
        message_receiver.start()
        message_sender=threading.Thread(target=self.input_loop)
        message_sender.start()
        print "Welcome! Type in your input"


    def input_loop(self):
        while True:
            data=input('')
            self.send_payload(data)

    def disconnect(self):
		#self.connection.
        self.connection.close()
        #Do more here probably
        pass

    def receive_message(self, message):
		"""
		Recieve_message is used by the MessageReciever-class to handle incoming messages.
		"""
        payload = parse_message(message)
		
		timestamp = payload["timestamp"]
		sender = payload["sender"]
		response = payload["response"]
		content = payload["content"]
		
		output = "{1} - {0} [{2}]:\n".format(timestamp,sender,response)
		
		#Make indentation. Split when respnse = history.
		output = "\t" + "\t\n".join(content.split("\n"))
		
		print(output)
	def create_payload(command):
		"""
		Creates json of a command.
		"""
		request,content = command.split(" ")
		data = {"request":request,"content":content}
		return json.dumps(data)
	def parse_message(message):
		"""
		Parses message from string format to dictionary. If the payload is an invalid json-format, return None.
		"""
		try:
			return json.loads(message)
		except ValueError:
			return None
    def send_payload(self, data):
        # TODO: Handle sending of a payload
		data = create_payload(data)
        self.connection.sendto(data,(self.host,self.server_port))
        pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
