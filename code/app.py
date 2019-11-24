from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT,jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'ABCDEF'
api = Api(app)

jwt = JWT(app, authenticate, identity)


items = []


class Item(Resource) :
    @jwt_required()
    def get(self, name):
        return {'item': next(filter(lambda x: x['name'] == name, items), None)}

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = request.get_json()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item

    def delete(self, name):
        x = next(filter(lambda x: x['name'] == name, items))
        items.remove(x)
        return x, "this has been removed "

    def put(self, name):
        data = request.get_json()
        if next(filter(lambda x: x['name'] == name, items), None) is None :
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item
        else :
            dic = next(filter(lambda x: x['name'] == name, items))
            dic.update(data)
        return items

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
app.run(port=5000, debug= True)
