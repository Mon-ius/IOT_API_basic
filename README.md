# IOT_API

Example_url : https://xxiot.herokuapp.com

## Main Function

### Index

hello world!
- GET https://xxiot.herokuapp.com

### User API

- GET (auth) https://xxiot.herokuapp.com/api/users
- POST (NAME,EMAIL,PASSWORD) https://xxiot.herokuapp.com/api/users
- PUT (auth) https://xxiot.herokuapp.com/api/users

### Sensor API

List Operation(auth)
- GET https://xxiot.herokuapp.com/api/sensors
- POST ADD(TYPE) => https://xxiot.herokuapp.com/api/sensors

Single Operation(auth)
- GET https://xxiot.herokuapp.com/api/sensors/<id>
- PUT UPDATE(UUID,TYPE) => https://xxiot.herokuapp.com/api/sensors/<id>
- DELETE  https://xxiot.herokuapp.com/api/sensors/<id>


### Data API

List Operation
- GET (UUID) https://xxiot.herokuapp.com/api/dataset
- POST ADD(UUID,VALUE) => https://xxiot.herokuapp.com/api/dataset

Single Operation
- GET (UUID) https://xxiot.herokuapp.com/api/dataset/<id>
- PUT UPDATE(UUID,VALUE) => https://xxiot.herokuapp.com/api/dataset/<id>
- DELETE (UUID) https://xxiot.herokuapp.com/api/dataset/<id>

**Structure**

User
- name(String)
- email(String)
- password_hash(String)

Sensor
- id(Int)
- UUID(String)
- stype(String)

Data
- id(Int)
- value(Float)
- IP(String)
- creation_date(DateTime)

  
## Test

### HTTP Test
- python api_http_test.py
- select correct service

### Basic API Test
- python api_basic_test.py
- select correct service

### Curl

- add user(no auth)

`curl  -i -H "Content-Type: application/json" -X POST -d '{"name":"Justest","email":"Justest@test.com","password":"Justest"}' https://xxiot.herokuapp.com/api/users`

- add sensor(auth)

`curl -u Justest:Justest -i -H "Content-Type: application/json" -X POST -d '{"stype":"temperature"}' https://xxiot.herokuapp.com/api/sensors`

- add data(uuid,no auth)

`curl  -i -H "Content-Type: application/json" -X POST -d '{"uuid": "53c103a1-fa69-4f6a-bc56-9df3ebe960dd","value":"20"}' https://xxiot.herokuapp.com/api/dataset`

- get current user's sensor(auth)

`curl  -u Justest:Justest -i  -X GET  https://xxiot.herokuapp.com/api/sensors`

`curl  -u Justest:Justest -i  -X GET  https://xxiot.herokuapp.com/api/sensors/11`

- get identified sensor's data(uuid)

`curl  -i -H "Content-Type: application/json" -X GET -d '{"uuid": "53c103a1-fa69-4f6a-bc56-9df3ebe960dd"}' https://xxiot.herokuapp.com/api/dataset/5`

`curl  -i -H "Content-Type: application/json" -X GET -d '{"uuid": "53c103a1-fa69-4f6a-bc56-9df3ebe960dd"}' https://xxiot.herokuapp.com/api/dataset`

`curl  -i -H "Content-Type: application/json" -X GET -d '{"uuid": "53c103a1-fa69-4f6a-bc56-9df3ebe960dd"}' https://xxiot.herokuapp.com/api/dataset\?token\='v-upper'`
  
----

- original feature

`curl  -i https://xxiot.herokuapp.com/api/temps`

`curl  -i -H "Content-Type: application/json" -X POST -d '{"value":"20","place":"home"}' https://xxiot.herokuapp.com/api/temps`



## Requirements

### Packages

- Flask
- Flask-Restful
- Flask_httpauth
- Flask-Sqlalchemy
- Flask-WTF
- Flask-Bootstrap
- Flask-Migrate
- Psycopg2-binary
- Gunicorn
- Gevent
- requests

### Runtime Version

- python=3.6.6

## Deploy 

- uwsgi 
- systemd
- docker


[How to deploy](deploy/README.MD)