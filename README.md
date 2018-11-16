# IOT_API

Example_url : https://xxiot.herokuapp.com

## Main Function

### Index

hello world!
- GET https://xxiot.herokuapp.com

### Sensor API

List Operation
- GET https://xxiot.herokuapp.com/api/sensors
- POST ADD(TYPE) => https://xxiot.herokuapp.com/api/sensors

Single Operation
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

- curl  -i -H "Content-Type: application/json" -X POST -d '{"place":"pxl","value":"20"}' https://xxiot.herokuapp.com/api/temps
- curl  -i -H "Content-Type: application/json" -X POST -d '{"place":"pxl","value":"20"}' https://xxiot.herokuapp.com/api/temps
- curl  -i -H "Content-Type: application/json" -X POST -d '{"place":"pxl","value":"20"}' https://xxiot.herokuapp.com/api/temps
- curl  -i -H "Content-Type: application/json" -X GET  https://xxiot.herokuapp.com/api/temps

## Requirements

### Packages

- Flask
- Flask-Restful
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