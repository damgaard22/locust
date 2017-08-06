
## Description

Locust is an easy-to-use, distributed, user load testing tool. It is intended for load-testing web sites (or other systems) and
figuring out how many concurrent users a system can handle.

This repo introduces WebSocket functionality to the framework. 


## Installation
Install this repo using pip:

```bash
pip install git+https://github.com/damgaard22.git
```
Update to newest version using:
```bash
pip install git+https://github.com/damgaard22.git --upgrade
```
## Usage

The main purpose of this repository is to implement WebSockets as part of the testing framework.
For more in depth guides pertaining locust, please refer to http://docs.locust.io/en/latest/

### WebSocket Client

The repo introduces a WebSocket client referenced as ws_client, which is defined in websocketclient.py
The ws_client is a property of a locust instance, therefore it is called using

```python
self.ws_client.FUNCTION()
```

The ws_client has two functions useful for testing:
* connect() - Creates a WebSocket and connects to the broker with a session-cookie
* send() - Sends data over the WebSocket created in connect

#### connect()
Connect takes two arguments:
* cookie: **Dict** - Dict containing a string as such:  ['Cookie: COOKIESTRING']
* host: **String** - The url of the WebSocket broker as a string 

The connection is kept for the whole testing process.
Example:

```python
host = 'wss://github.com/broker'
cookie = ['Cookie: COOKIESTRING']
self.ws_client.connect()
```

#### send()
Send takes two arguments
* name: **String** - The tag that appears on the Web UI. For example could a connection to /state/ be called ws:/state/ as to indicate WebSocket usage
* payload: **Dict** - A dictionary containing the data to send.

An example sending some dummy data:
```python
name = 'ws:/dummy-endpoint/'
payload = {'Dummy': 'data'}
self.ws_client.send(payload, name)
```
### Basic Locust Usage and Test Case writing
A locust file is a file that describes the world of a single locust

Locust uses locust files to run the tests. A locust file contains 4 things:
* Imports - Every locust file will: from locust import Locust, TaskSet, task, HttpLocust
* A taskset: **Class** - A Class that inherits from TaskSet and describes the behaviour the locust
* Tasks: **Functions** - The individual tests defined as functions using the @task decorator
* A locust: **Class** - Defines the locust instance and assigns it a taskset and the minimum and maximum wait between task execution.

A very basic locust file could look something like this:

```python
from locust import Locust, TaskSet, task, HttpLocust

class MyTaskSet(TaskSet):
    def on_start(self):
    """
    This function is executed once at the creation of the locust. This is a good place to authenticate.
    """
        self.ws_client.connect()
        print('WebSocket connected')
    
    @task
    def send_data(self):
        name = 'ws:send_data'
        payload = {'Dummy': 'Data'}
        self.ws_client.send(payload, name)

class MyLocust(HttpLocust):
    taskset = MyTaskSet
    
    min_wait = 3000
    max_wait = 5000
    
```
The locust file defines a single locust that waits between 3 to 5 seconds before executing a random task in MyTaskSet.

#### Testing with HTTP
The following section is meant to give a quick introduction to using the Locust HTTP client for testing.
For a more in depth guide, please refer to: http://docs.locust.io/en/latest/writing-a-locustfile.html#making-http-requests

Locust implements its own HTTP client as a property of a locust.
Called using:

```python
self.client.METHOD()
```
8
When running locust you supply a host as an argument.
The url supplied will become the base_url, therefore it is important to be mindful of how you write that url.

##### GET requests
GET requests are made using the client as such:

```python
self.client.get(url)
```

If i supplied https://github.com as the base_url and wanted to GET https://github.com/damgaard22/ then i would pass
/damgaard22/ as the url parameter as it is appended to the base_url

Example printing the contents of response from GET https://github.com/damgaard22/

```python
r = self.client.get(/damgaard22/)
print(r.text)
```

##### POST requests
The same url logic applies to POST requests.
A POST request is made as follows:

```python
self.client.post(url, data)
```
Let's say i wanted to POST data to https://github.com/login/ i would pass /login/ as the url parameter.

```python
data = {'Dummy': 'data'}
self.client.post(url, data)
```

If your target is using SSL you might need to add a Referer to the request header.
Edit headers by changing the dict client.headers:

```python
data = {'Dummy': 'data'}
self.client.headers['Referer'] = 'https://github.com/login/'
self.client.post(/login/, data)
```

You might also need to add a CSRF token, which requires a get request first:

```python
r = self.client.get('/login/')
csrftoken = r.cookies['csrftoken']

data = {'Dummy': 'data','csrfmiddlewaretoken': csrftoken}
self.client.headers['Referer'] = 'https://github.com/login/'
self.client.post(/login/, data)
```

##### Authenticating with HTTP
Authenticating with the HTTP client can be done in a couple of ways.

One of the ways you can authenticate with the locust http client is as follows:
```python
r = self.client.get('/login/')
csrftoken = r.cookies['csrftoken']

data = {'csrfmiddlewaretoken': csrftoken, 'username': 'USERNAME', 'password': 'PASSWORD'}
self.client.headers['Referer'] = 'https://github.com/login/'
self.client.post(/login/, data)
```

For more information on alternative ways of authenticating, please refer to http://docs.locust.io/en/latest/writing-a-locustfile.html#making-http-requests


#### Running Locust

To actually run the locust service run:
```bash
locust -f LOCUST_FILE --host BASE_URL
```

Where LOCUST_FILE is the path to the locust_file and BASE_URL is the base_url of the host.

## To Do

* Streamline the process of getting a CSRF token before a POST request

## License

Open source licensed under the MIT license (see _LICENSE_ file for details).

