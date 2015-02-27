import json
"""
Functions that returns json-response-payloads as text.
"""

def msg(timestamp,sender,response,content):
	"""
	Creates json in the specified format.
	"""
	return  """{'timestamp': '{0}','sender': '{1}','response': '{2}','content': '{3}'}""".format(timestamp,sender,response,content)

def error(content):
	"""
	Make error-payload given a description of the error.
	"""		
	timestamp = get_timestamp()
	response = "error"
	sender = "server"
	return msg(timestamp,sender,response,content)
def help():
	"""
	"""
	timestamp = get_timestamp()
	response = "history"
	sender = "server"
	content = """Usage of commands:
login <username>: Send a requet to server with specified username.
logout: Sends a request to log out and disconnect from the server.
msg <message>: Sends a message to the server that broadcasts to all connected clients.
names: Sends a list of usernames that are connected to the server.
	"""
	return msg(timestamp,sender,response,content)
def history(history):
	"""
	Make history message for user who logged in.
	"""
	timestamp = get_timestamp()
	response = "history"
	content = ""
	for entry in history:
		payload = json.loads(entry)
		time = payload["timestamp"]
		username = payload["sender"]
		message = payload["content"]
		content += '{0} {1}: "{2}"'.format(time,username,message)
	sender = "server"
	return msg(timestamp,sender,response,content)

def message(sender,content):
	"""
	Make message given username and content of the message.
	"""
	timestamp = get_timestamp()
	response = "message"
	return msg(timestamp,sender,response,content)
def users(usernames):
	"""
	Make list containing all usernames.
	"""	
	timestamp = get_timestamp()
	response = "info"
	sender = server
	content = "\n".join(usernames)
	return msg(timestamp,sender,response,content)
	
def get_timestamp():
	"""
	Gets current timestamp in HH:MM:SS
	"""
	current_time = time.localtime()
	
	hour = str(current_time.tm_hour).zfill(2)
	min = str(current_time.tm_min).zfill(2)
	sec = str(current_time.tm_sec).zfill(2)

	return "{0}:{1}:{2}".format(hour,min,sec)
