from app import create_app
from app.models import User,Data,Sensor,Temperature
from ext import db,desc
import click
app = create_app()

def clearDB():
    Data.query.delete()
    Sensor.query.delete()
    User.query.delete()
    Temperature.query.delete()
    db.session.commit()
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Sensor': Sensor, 'Data': Data,'Temp':Temperature,'cl':clearDB}

if __name__ == '__main__': 
    app.run(debug=True)  


