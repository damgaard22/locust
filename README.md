
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
connect() - Creates a WebSocket and connects to the broker with a session-cookie
send() - Sends data over the WebSocket created in connect

#### connect()
Connect takes no arguments, it authenticates using the cookie that is hardcoded in websocketclient.py.
The broker is also hardcoded in websocketclient.py
This is definately a process that can be improved.

The connection is kept for the whole testing process.
Example:

```python
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

##### GET requests

##### POST requests

##### Authenticating with HTTP

#### Running Locust

## To Do

## License

Open source licensed under the MIT license (see _LICENSE_ file for details).

