from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from datetime import datetime, timedelta

from resources.user import UserRegister, UserList, UserList2
from resources.item import ItemRes, ItemListRes
from resources.store import StoreRes, StoreListRes


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'peter'
api = Api(app)


app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) # expired in 30 minutes

jwt = JWT(app,authenticate,identity)

# JWT will create a new end point call '/auth' with POST method
# 1. when we call /auth give username and password send to authenticate function
# 2. in authenticate funtion will get the user and compare the password
# 3. if match return the user


api.add_resource(ItemRes,'/item/<string:name>')
api.add_resource(ItemListRes,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(UserList,'/users')
api.add_resource(UserList2,'/users2')
api.add_resource(StoreRes,'/store/<string:name>')
api.add_resource(StoreListRes,'/stores')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)