from app import app, db
from app.models import *
from app.utils.request_handler import *
from app.utils.validation.jwt_token import *
from sqlalchemy_get_or_create import get_or_create
import sqlalchemy

md = sqlalchemy.MetaData()

def index():
    db.create_all()
    return "welcome to the Home page"


def create_parent(pk):
    get_or_create(db.session,Parents,defaults=None,name=pk)
    db.session.commit()
    return ok_request({"message":"created successfully"})

def create_child(pk):
    get_or_create(db.session,Childs,defaults=None,name=pk)
    db.session.commit()
    return ok_request({"message":"created successfully"})

def one_mapping():
    parent = request.json.get("parent")
    child = request.json.get("child")
    if parent and child:
        if Childs.query.filter_by(id=int(child)).update({'parent_id':parent}):
            db.session.commit()
            return ok_request({"message": "Added successfully"})
        return notok_request({"message": "Child Id not found"})
    return notok_request({"message": "Invalid Keys"})

def many_related():
    parent = request.json.get("parent")
    child1 = request.json.get("child1")
    child2 = request.json.get("child2")
    if parent and child1 and child2:
        var = get_or_create(db.session,ManyRelated,defaults=None,parent_id=int(parent),child_id1=int(child1),child_id2=int(child2))
        if var:
            db.session.commit()
            return ok_request({"message":"created successfully"})
    return notok_request({"message": "Invalid Keys"})


def all_tables():
    data = db.engine.table_names()
    return ok_request({"data":data})

def all_columns(pk):
    if db.engine.has_table(pk):
        sql = sqlalchemy.Table(pk,md,autoload=True, autoload_with=db.engine)
        col = sql.c
        data = [i for i,j in col.items()]
        return ok_request({"data":data})
    return notok_request({"message":f'{pk} table not found'})