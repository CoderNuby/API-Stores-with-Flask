from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from DB import db


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            return item
        except KeyError:
            return abort(404, message="Item not found")
    
    
    @jwt_required()
    def delete(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return {"massage": "Item deleted correctly"}, 200
        except KeyError:
            return abort(404, message="Item not found")
    

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = ItemModel.query.get(item_id)
            if item:
                item.name = item_data["name"]
                item.price = item_data["price"]
            else:
                item = ItemModel(id=item_id, **item_data)
            db.session.add(item)
            db.session.commit()
        except Exception:
            return abort(400, "Not found")
        return item
        
@blp.route("/item")
class Item2(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items


    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        print(item)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")
        return item
        
