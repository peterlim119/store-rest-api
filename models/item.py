from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self,name,price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price, 'store_id': self.store_id}

    @classmethod
    def get_items(cls):
        result = {'items': [item.json() for item in cls.query.all()]}
        # or using lambda
        # result = {'items': list(map(lambda x: x.json(), cls.query.all()))}
        return result

    @classmethod
    def find_by_name(cls,name):
        return  cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name = name LIMIT 1

    def save_to_db(self):  #for both insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


