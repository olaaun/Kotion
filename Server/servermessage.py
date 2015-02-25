"""
Functions that returns json-response-payloads as text.
"""

def msg():
	return  """{"timestamp": "{0}","sender": "{1}","response": "{2}","content": "{3}"}"""

def error(content):
	"""
	Make error-payload given a description of the error.
	"""		
	timestamp = get_timestamp()
	response = "error"
	sender = "server"
	return msg.format(timestamp,sender,response,content)

def greeting(username):
	"""
	Make greeting-message given a username.
	"""
	timestamp = get_timestamp()
	response = "info"
	content = "Hello {0}! Welcome to the chat.".format(username)
	sender = "server"
	return msg().format(timestamp,sender,response,content)

def message(sender,content):
	"""
	Make message given username and content of the message.
	"""
	timestamp = get_timestamp()
	response = "message"
	return msg().format(timestamp,sender,response,content)
def users(usernames):
	"""
	Make list containing all usernames.
	"""	
	timestamp = get_timestamp()
	response = "info"
	sender = server
	content = "\n".join(usernames)
	return msg().format(timestamp,sender,response,content)
	
def get_timestamp():
	"""
	Gets current timestamp in HH:MM:SS
	"""
	current_time = time.localtime()
	
	hour = str(current_time.tm_hour).zfill(2)
	min = str(current_time.tm_min).zfill(2)
	sec = str(current_time.tm_sec).zfill(2)

	return "{0}:{1}:{2}".format(hour,min,sec)
