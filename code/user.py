import sqlite3
from flask_restful import Resource,reqparse
class User :
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def findbyusername(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        x = (username,)
        find_user = "Select * from users where username = ?"
        y = cursor.execute(find_user, x)
        row = y.fetchone()
        if row :
            user = cls(*row)
        else :
            user = None
        connection.close()
        return user


    @classmethod
    def findbyuserid(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        x = (_id,)
        find_user = "Select * from users where id = ?"
        y = cursor.execute(find_user, x)
        row = y.fetchone()
        if row :
            id_ = cls(*row)
        else :
            id_ = None
        connection.close()
        return id_

class UserRegister(Resource) :
    TABLE_NAME = 'users'
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.findbyusername(data['username']) is not None :
            return {'message': "An user with name '{}' already exists."}
        else :
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "Insert into {table} values (?, ?, ?)".format(table=self.TABLE_NAME)
            cursor.execute(query, (data['id'], data['username'], data['password']))
            connection.commit()
            connection.close()
        return {"user has been created"}







