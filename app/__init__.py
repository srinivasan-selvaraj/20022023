from flask import Flask,request
from flask_cors import CORS
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

logging.basicConfig(format='%(asctime)s:NAME:%(levelname)s:%(message)s:')

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)

db = SQLAlchemy(app)
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)


from app import urls


