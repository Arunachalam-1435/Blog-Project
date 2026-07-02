from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
load_dotenv('config.env')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def main():
    return render_template('index.html', heading="Welcome all!")

@app.route('/post')
def post():
    return render_template('post.html', heading='Create a Post')

if __name__ == "__main__":
    app.run()