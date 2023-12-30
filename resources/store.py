from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema
from DB import db

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(sel, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            return store
        except KeyError:
            return abort(404, message="Store not found")
    
    @jwt_required()
    def delete(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)   
            db.session.delete(store)
            db.session.commit()
            return {"massage": "Store deleted correctly"}, 200
        except KeyError:
            return abort(404, message="Item not found")
    
    @jwt_required()
    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, store_data, store_id):
        try:
            store = StoreModel.query.get(store_id)
            if store:
                store.name = store_data["name"]
                db.session.add(store)
                db.session.commit()
                return store

        except Exception:
            return abort(400, "Not found")
        
@blp.route("/store")
class Stroe2(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error ocurred creating the store.")
        return store
