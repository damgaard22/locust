import time
import json
import gevent

from locust import events

import websocket


class SocketClient(object):
	"""
	Class that defines a WebSocket client
	"""
	def __init__(self):
		pass

	def connect_no_auth(self, host):
		"""
		Connects to host without passing a cookie for authentication
		"""
		self.ws = websocket.WebSocket()
		self.ws.connect(host)
		
		events.quitting += self.on_close

	def connect(self, cookie, host):
		"""
		Connects to host and authenticates via a cookie.
		Cookie should be a string of following format: "Cookie: COOKIE-STRING-HERE"
		"""
		
		self.ws = websocket.WebSocket()
		self.ws.connect(host, header = [cookie])
		
		events.quitting += self.on_close


	def send_and_recv(self, payload):
		"""
		Sends payload to host and waits for response.
		Times out after 10 seconds of no response.
		"""
		json_data = json.dumps(payload, ensure_ascii = False).encode('utf8')

		g = gevent.spawn(self.ws.send, json_data)
		g.get(block = True, timeout = 2)
		g = gevent.spawn(self.ws.recv)
		json_data = g.get(block = True, timeout = 10)

		return json_data


	def send(self, payload, name):
		"""
		Sends payload and handles the error checking and the locust events.
		name is displayed in the Web GUI.
		"""
		start_time = time.time()
		e = None
		try:
			data = self.send_no_error_check(payload)
			print(data)
			assert 'id' in data 
		except AssertionError as exp:
			e = exp
			print('Error: ', exp)
		except Exception as exp:
			e = exp
			self.ws.close()
			self.connect()
		elapsed = int((time.time() - start_time) * 1000)
		if e:
			events.request_failure.fire(request_type='WebSocket', name=name, 
										response_time=elapsed, exception=e)
		else:
			events.request_success.fire(request_type='WebSocket', name=name,
										response_time=elapsed, response_length=0)
	

	def on_close(self):
		"""
		This is run when the locust service is terminated.
		"""
		self.ws.close()
