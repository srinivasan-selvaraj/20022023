import os
from envyaml import EnvYAML
ENVIRONMENT = EnvYAML('env.yaml')


basedir = os.path.abspath(os.path.dirname(__file__))

db_name = ENVIRONMENT['db']['name']

SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_name}.db"