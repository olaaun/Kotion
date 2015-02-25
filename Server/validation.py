"""
Functions that validates
"""

def is_invalid_username(username):
	"""
	Returns true if username is invalid
	"""
	return not username.isalnum()
	
def is_invalid_payload(payload):
	"""
	Returns true if payload is invalid
	"""
	if not payload.has_key("request"):
		return True
	if not payload["request"] in ["login","logout","msg","names","help"]:
		return True
	if not payload.has_key("content"):
		return True
	return False

def is_username_taken(threads,username):
	"""
	Returns true if username is found in one of the threads on the server.
	"""
	for thread in threads:
		if thread.username == username:
			return True
	return False
