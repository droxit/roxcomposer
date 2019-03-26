import json
import requests

roxconnector = 'localhost:7475'
service_file_dir = 'services'
logobs_session = None
logobs_session_timeout = 3600

f = {
  "classpath": "roxcomposer.tests.classes.delay_service.DelayService",
  "params": {
    "ip": "127.0.0.1",
    "port": 4007,
    "name": "delay_service"
  }
}


headers = {'Content-Type': 'application/json'}
r = requests.post('http://{}/start_service'.format(roxconnector), json=f, headers=headers)


d = {'name': "pipe1", 'services': [{'service': 'delay_service', 'params':{'param1':'someparam'}}]}
r = requests.post('http://{}/set_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
print(r.text)