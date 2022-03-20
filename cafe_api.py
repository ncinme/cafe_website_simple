# Copied form day #69
# The app will run at port 5000

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
import random
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

app_api = Flask(__name__)

# Connect to Database
app_api.config['JSON_SORT_KEYS'] = False  # Not recommended as JSON is supposed to be unordered
app_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app_api)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    map_url = Column(String(500), nullable=False)
    img_url = Column(String(500), nullable=False)
    location = Column(String(250), nullable=False)
    seats = Column(String(250), nullable=False)
    has_toilet = Column(Boolean, nullable=False)
    has_wifi = Column(Boolean, nullable=False)
    has_sockets = Column(Boolean, nullable=False)
    can_take_calls = Column(Boolean, nullable=False)
    coffee_price = Column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Initialize Marshmello (for serialization, needed for jasonify)
ma = Marshmallow(app_api)


# Create a Product Schema (to specify which fields to send to the client)
class CafeSchema(ma.Schema):
    class Meta:
        ordered = True  # The output will be ordered according to the order that the fields are defined in the class.
        fields = ('id', 'name', 'map_url', 'img_url', 'location', 'seats', 'has_toilet', 'has_wifi', 'has_sockets',
                  'can_take_calls', 'coffee_price')


# Initialize the Schema for one product
cafe_schema = CafeSchema()

# Initialize the Schema for many products
cafes_schema = CafeSchema(many=True)


@app_api.route("/")
def home():
    return render_template("index_api.html")


# HTTP GET - Read Record
# Get a random cafe
@app_api.route('/random')
def get_random_cafe():
    cafes = Cafe.query.all()  # returns a list of iterables
    random_cafe = random.choice(cafes)
    random_cafe = cafe_schema.dump(random_cafe)
    return jsonify({'status': 'success', 'cafe': random_cafe})


@app_api.route('/all')
def get_all_cafe():
    all_cafes = Cafe.query.all()
    all_cafes = cafes_schema.dump(all_cafes)
    return jsonify({'status': 'success', 'cafes': all_cafes})


# find a cafe by location
# http://127.0.0.1:5000/search?loc=Peckham
@app_api.route('/search')
def find_a_cafe():
    location = request.args.get('loc')  # passed through URL
    cafes = Cafe.query.filter_by(location=location).all()
    if cafes:
        return jsonify(cafes_schema.dump(cafes))
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a cafe at that location."})


# HTTP POST - Create Record
@app_api.route('/add', methods=['POST'])
def add_cafe():
    data = request.json
    cafe = Cafe()
    cafe.name = data.get('name')
    cafe.map_url = data.get('map_url')
    cafe.img_url = data.get('img_url')
    cafe.location = data.get('location')
    cafe.seats = data.get('seats')
    cafe.has_toilet = data.get('has_toilet')
    cafe.has_wifi = data.get('has_wifi')
    cafe.has_sockets = data.get('has_sockets')
    cafe.can_take_calls = data.get('can_take_calls')
    cafe.coffee_price = data.get('coffee_price')

    db.session.add(cafe)
    db.session.commit()

    return cafe_schema.jsonify(cafe)


# HTTP PUT/PATCH - Update Record
@app_api.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = request.form.get('coffee_price')
        db.session.commit()
        return cafe_schema.jsonify(cafe), 200
    else:
        return jsonify(error={'Not Found': 'Sorry, the cafe with that id was not found in the database'})


# HTTP DELETE - Delete Record
@app_api.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    if request.args.get('api-key') == API_KEY:
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={'success': f'The cafe with the id {cafe_id} is removed from the database'})
        else:
            return jsonify(error={'Not Found': f'Sorry, the cafe with the id {cafe_id} was not found in the database'})
    else:
        return jsonify(error={'Forbidden': "Sorry, that's not allowed. Make sure you have correct api-key"})


if __name__ == '__main__':
    # app_api.run(debug=True, host="127.0.0.1", port=5000)
    app_api.run(debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # app_api.run(debug=True, host='0.0.0.0', port=port)
