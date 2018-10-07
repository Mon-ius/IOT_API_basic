from app import create_app
from app.models import Temperature
from ext import db
import click
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Temp': Temperature}

if __name__ == '__main__': 
    app.run(debug=True)  


