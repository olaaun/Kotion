# -*- coding: utf-8 -*-
import socket
import MessageReceiver

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
        print "Welcome! Type in your input"
        while True:
            data=input('')
            if data=='logout':
                self.disconnect()
                print('Disconnected')
                break
            self.send_payload(data)
            print(self.recieve_message)


    def disconnect(self):
        self.connection.close()
        #Do more here probably
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        #Use the MessageReceiver handle this
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.sendto(data,(self.host,self.server_port))
        pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
