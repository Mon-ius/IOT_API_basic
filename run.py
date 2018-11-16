from app import create_app
from app.models import User,Data,Sensor
from ext import db
import click
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Data': Data, 'Sensor': Sensor}

if __name__ == '__main__': 
    app.run(debug=True)  


