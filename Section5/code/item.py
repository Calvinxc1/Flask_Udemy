import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank',
    )
    
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item, 200
        
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        query = 'SELECT * FROM items WHERE name=?;'
        result = cur.execute(query, (name,))
        row = result.fetchone()
        cur.close()
        conn.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
    
    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400
        
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price'],
        }
        try:
            self.insert(item)
        except:
            return {'message': 'An error occured inserting the item'}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        query = 'INSERT INTO items VALUES (?,?);'
        cur.execute(query, (item['name'], item['price']))

        conn.commit()
        cur.close()
        conn.close()
    
    def delete(self, name):
        if self.find_by_name(name) is None:
            return {'message': 'Item does not exist'}, 400

        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        query = 'DELETE FROM items WHERE name=?;'
        cur.execute(query, (name,))

        conn.commit()
        cur.close()
        conn.close()

        return {'message': 'Item deleted'}, 200
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occured inserting the item'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occured updating the item'}, 500
        return updated_item, 200

    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        query = 'UPDATE items SET price=? WHERE name=?;'
        cur.execute(query, (item['price'], item['name']))

        conn.commit()
        cur.close()
        conn.close()
    
class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        query = 'SELECT * FROM items;'
        result = cur.execute(query)
        items = [{'name': item[0], 'price': item[1]} for item in result]

        conn.commit()
        cur.close()
        conn.close()

        return {'items': items}, 200