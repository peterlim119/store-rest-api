from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from models.store import StoreModel


class StoreRes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot left blank")

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {'message':'cannot find that store name'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with name {} already exists'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message', 'An Error occor while creating a store'}, 500

        return store.json(),200

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message':'Store has been deleted'},200
        return {'message':'Store is not found'}

class StoreListRes(Resource):
    def get(self):
        return StoreModel.get_stores(),200
