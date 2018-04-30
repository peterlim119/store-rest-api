from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from datetime import datetime, timedelta
from user import UserRegister, UserList, UserList2

app = Flask(__name__)
app.secret_key = 'peter'
api = Api(app)

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) # expired in 30 minutes

jwt = JWT(app,authenticate,identity)

        # JWT will create a new end point call '/auth' with POST method
        # 1. when we call /auth give username and password send to authenticate function
        # 2. in authenticate funtion will get the user and compare the password
        # 3. if match return the user

items = []
class Item(Resource):
    @jwt_required() # ==> mean need to authenticate before call get method below
    def get(self,name):
        item = next(filter(lambda x: x['name'] == name, items),None)
        #same as item = next(filter(lambda x: x['name'] == name, items),{'item':None})

        return {'item':item}, 200 if item else 404
        # same as ==> return {'item':item}, 200 if item is not None else 404
        # filter may return more than one, we use list() to put into list if have more than one item
        # we use next() to get only first item, if not find item it return None (Null)
        # and we can use next() again to get next item

    @jwt_required()
    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items),None):
            # same as ==> if next(filter(lambda x: x['name'] == name, items),None) is not None:
            return {'message':'item with name {} is already exists'.format(name)}, 400
        else: # else may not need because it will stop after return
            data = request.get_json()
            price = data['price']
            item = {'name':name, 'price':price}
            items.append(item)
            return item, 201

    @jwt_required()
    def delete(self,name):
        item = next(filter(lambda x: x['name'] == name, items),None)
        if item:
            items.remove(item)
            return {'message':'item: {} has been deleted'.format(name)}, 303
        return {'message': 'item {} is not exists'.format(name)}, 400

    @jwt_required()
    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type = float,
                            required = True,
                            help = "this field cannot be left blank")

        data = parser.parse_args()
        #data = request.get_json()

        item = next(filter(lambda x:x['name'] == name, items),None)
        if item: # exists then update price
            item.update(data)
            return item, 201
        else:
            item = self.post(name)
            return item


class ItemList(Resource):
    def get(self):
        return {'items' : items}


api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(UserList,'/users')
api.add_resource(UserList2,'/users2')


if __name__ == '__main__':
    app.run()