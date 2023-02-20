from app.utils.request_handler import *
from app import app
from flask import jsonify
from datetime import timedelta
from flask_jwt_extended import *

app.config["JWT_SECRET_KEY"] = app.config['ENVIRONMENT']['flask']['secret_key']
app.config['JWT_TOKEN_LOCATION'] =  ["headers", "json"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=45)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)
jwt = JWTManager(app)

@jwt.expired_token_loader
def my_expired_token_callback(callback):
    print(callback['type'],'callback')
    if callback['type'] == 'refresh':
        response = ok_request({'message': 'Token has expired', 'success': False,'access_token':None})
    else:
        response = unauth_request({'message': 'Token has expired', 'success': False,'access_token':None})
    return response

##################      Creating Access_token and Refresh_token for valid user     ####################
def create_jwt_tokens(var='xxx'):
    access = create_access_token(identity = var)
    refresh = create_refresh_token(identity = var)
    return [access,refresh]

####################        Refreshing accesss token by using refresh_token        ########################
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access = create_access_token(identity=identity)
    response = ok_request({'success': True,'access_token':new_access,'message':'Token Success'})
    return response
