import time
import json
import gevent

from locust import events

import websocket


class SocketClient(object):
	def __init__(self, host):
		self.host = 'wss://demokratiskolen.dk/broker'
		self.cookie = ["Cookie: sessionid=uskxhvmfga8s3xfma3mcitb29499kg2p; _pk_id.2.7f89=f02a0d400f4ec018.1499432889.8.1501599292.1501599281.; _pk_ses.2.7f89=*; csrftoken=Y8aKx0xjTmeEbJwNsngdGQXivmUnTgJ8"]

	def connect_no_auth(self):
		self.ws = websocket.WebSocket()
		
		g = gevent.spawn(self.ws.connect, self.host)
		g.get(block = True, timeout = 2)
		g = gevent.spawn(self.ws.recv)
		json_data = g.get(block = True, timeout = 10)

		print(json_data)
		
		events.quitting += self.on_close

	def connect(self):
		self.ws = websocket.WebSocket()
		self.ws.connect(self.host, header = self.cookie)
		#self.ws.connect(self.host)
		
		events.quitting += self.on_close


	def receive(self):
		response = self.ws.recv()
		return response


	def send_no_error_check(self, payload):
		json_data = json.dumps(payload, ensure_ascii = False).encode('utf8')

		g = gevent.spawn(self.ws.send, json_data)
		g.get(block = True, timeout = 2)
		g = gevent.spawn(self.ws.recv)
		json_data = g.get(block = True, timeout = 10)

		return json_data


	def send(self, payload, name):
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
		self.ws.close()
