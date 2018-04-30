#from config import DBSQL
from flask_restful import Resource,Api, reqparse
from flask import Flask, request
from flask_jwt import JWT, jwt_required

from models.user import UserModel


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class UserList2(Resource):
    def get(self):
        return UserModel.get_users()
        # conn = DBSQL.connection()
        # conn.row_factory = dict_factory
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM users ORDER BY id")
        # result = cursor.fetchall()
        # conn.close()
        #
        # return {'users':result}

# ------------------------------------


class UserList(Resource):
    def get(self):
        return UserModel.get_users()
        # userlist = []
        # conn = DBSQL.connection()
        # cursor = conn.cursor()
        # sqlText = "SELECT * FROM users ORDER BY id"
        # result = cursor.execute(sqlText)
        # rows = result.fetchall()
        # for row in rows:
        #     userlist.append({'id':row[0],'username':row[1],'password':row[2]})
        # conn.close()
        # return {'users':userlist}


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type = str,
                        required=True,
                        help="This field cannot be blank")

    parser.add_argument('password',
                        type = str,
                        required=True,
                        help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_name(data['username']):
            return {'message':'A user with that name already exists'}, 400
        try:
            # new_user = UserModel(data['username'], data['password'])
            new_user = UserModel(**data)
            new_user.save_to_db()
        except:
            return {'message': 'An Error occur during inserting new user'}, 500

        return {"message" : "User created successfully"}, 201



