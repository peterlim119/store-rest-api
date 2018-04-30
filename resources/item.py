from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class ItemRes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="every item needs store id")

    #@jwt_required() # ==> mean need to authenticate before call get method below
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200 #     {'item':{'name':item[0],'price':item[1]}}, 200
        return {'message': "item not found"}, 404

    #@jwt_required()
    def post(self,name):
        item = ItemModel.find_by_name(name)  # return item object
        if item:
            return {'message':'item with name {} is already exists'.format(name)}, 400

        else: # else may not need because it will stop after return
            data = request.get_json()
            new_item = ItemModel(name,data['price'],data['store_id'])  # or (name, **data)

            try:
                new_item.save_to_db()  # ItemModel.add_item(name,price)
            except:
                return {'message': 'An Error occur during inserting the item'}, 500
        return new_item.json(), 201

    #@jwt_required()
    def put(self,name):
        data = ItemRes.parser.parse_args()
        item = ItemModel.find_by_name(name)  # return item object
        if item is None:
            try:
                print('insert')
                item = ItemModel(name, data['price'], data['store_id'])  # (name, **data)
                item.save_to_db()
            except:
                return {'message':'An Error occur during inserting the item'},500
        else:
            try:
                print('update')
                #item = ItemModel(name, data['price'], data['store_id'])  # (name, **data)
                item.price = data['price']
                item.store_id = data['store_id']
                item.save_to_db()  # for both insert and update
            except:
                return {'message': 'An Error occur during updating the item'}, 500
        return item.json(), 201

    #@jwt_required()
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
                return {'message':'{} has been deleted'.format(name)}, 303
            except:
                return {'message': 'An Error occur during deleting the item'}, 500
        return {'message': 'item {} is not exists'.format(name)}, 400




class ItemListRes(Resource):
    def get(self):
        return ItemModel.get_items(), 200

