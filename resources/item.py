from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel





#every resource has to be class
class Item(Resource): #class Student becomes a copy of resource
#It inherits the property of Resource

    parser = reqparse.RequestParser()

    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field cannot be left blank"
    )




    parser.add_argument('store_id',
    type = int,
    required = True,
    help = "We need store id"
    )



    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(),200

        return {"message":"Items does not exists"},404
        
        


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message" : "Item '{}' alreay exists".format(name)}, 400 #request error

        data = Item.parser.parse_args()
        item = ItemModel(name,data["price"],data["store_id"])

        # try:
        #     item.insert()
        # except:
        #     return {"message" : "ERROR while inserting "}, 500 #internal server error
        item.save_to_db()
        
        return item.json(),201

    
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {"message" : "Item deleted" }

        return {"message" : "Item not found"}




    #TO CREATE ITEM OR UPDATE EXISTING ITEM
    def put(self, name):
        data = Item.parser.parse_args()


        item = ItemModel.find_by_name(name)
        

        if item is None:
            item = ItemModel(name,data["price"],data["store_id"])
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json()


    


class ItemList(Resource):
    def get(self):
 
        return {"items": [item.json() for item in ItemModel.query.all()] }

#list(map(lambda x:x.json(), ItemModel.query.all()))
#This will apply/map x.json to all the items 