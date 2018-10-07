# IOT_API

Example_url : https://xxiot.herokuapp.com

## Main Function

### Index

hello world!
- GET https://xxiot.herokuapp.com/
- 
### Temperature API

List Operation
- GET https://xxiot.herokuapp.com/api/temps
- POST (VALUE,PLACE) => https://xxiot.herokuapp.com/api/temps

Single Operation
- GET https://xxiot.herokuapp.com/api/temps/<id>
- PUT (VALUE,PLACE) => https://xxiot.herokuapp.com/api/temps/<id>
- DELETE  https://xxiot.herokuapp.com/api/temps/<id>

Structure

- id(Int)
- value(String)
- place(String)
- creation_date(DateTime)

## Requirements

- Flask
- Flask-Restful
- Flask-Sqlalchemy
- Flask-WTF
- Flask-Bootstrap
- Flask-Migrate
- Psycopg2-binary
- Gunicorn