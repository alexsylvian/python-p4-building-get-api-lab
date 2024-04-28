#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    result = []
    for bakery in bakeries:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at,
            'baked_goods': [{'id': good.id, 'name': good.name, 'price': good.price, 'created_at': good.created_at, 'updated_at': good.updated_at} for good in bakery.baked_goods]
        }
        result.append(bakery_data)
    return jsonify(result)

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_data = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at,
        'updated_at': bakery.updated_at,
        'baked_goods': [{'id': good.id, 'name': good.name, 'price': good.price, 'created_at': good.created_at, 'updated_at': good.updated_at} for good in bakery.baked_goods]
    }
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    result = []
    for good in baked_goods:
        bakery_data = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'created_at': good.created_at,
            'updated_at': good.updated_at,
        }
        # Check if good.bakery is not None before accessing its attributes
        if good.bakery:
            bakery_data['bakery'] = {
                'id': good.bakery.id,
                'name': good.bakery.name,
                'created_at': good.bakery.created_at,
                'updated_at': good.bakery.updated_at
            }
        else:
            bakery_data['bakery'] = None  # or any default value you prefer
        result.append(bakery_data)
    return jsonify(result)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    result = {
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price,
        'created_at': baked_good.created_at,
        'updated_at': baked_good.updated_at,
    }
    # Check if baked_good.bakery is not None before accessing its attributes
    if baked_good.bakery:
        result['bakery'] = {
            'id': baked_good.bakery.id,
            'name': baked_good.bakery.name,
            'created_at': baked_good.bakery.created_at,
            'updated_at': baked_good.bakery.updated_at
        }
    else:
        result['bakery'] = None  # or any default value you prefer
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
