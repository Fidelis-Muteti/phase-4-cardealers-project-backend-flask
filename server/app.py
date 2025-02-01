from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Dealer, Car, Feature
import os
from dotenv import load_dotenv
load_dotenv()
# App Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Root route
@app.route("/")
def index():
    return "<h1>Car Dealers API</h1>"

# --------------------- DEALERS ENDPOINTS ---------------------
@app.route("/dealers", methods=["GET", "POST"])
def handle_dealers():
    if request.method == "GET":
        dealers = Dealer.query.all()
        return jsonify([dealer.to_dict() for dealer in dealers])
    
    elif request.method == "POST":
        data = request.get_json()
        new_dealer = Dealer(name=data["name"])
        db.session.add(new_dealer)
        db.session.commit()
        return jsonify(new_dealer.to_dict()), 201

@app.route("/dealers/<int:id>", methods=["GET", "DELETE"])
def handle_dealer(id):
    dealer = Dealer.query.get(id)
    if not dealer:
        return make_response(jsonify({"error": "Dealer not found"}), 404)

    if request.method == "GET":
        return jsonify(dealer.to_dict())
    
    elif request.method == "DELETE":
        db.session.delete(dealer)
        db.session.commit()
        return "", 204

# --------------------- CARS ENDPOINTS ---------------------
@app.route("/cars", methods=["GET", "POST"])
def handle_cars():
    if request.method == "GET":
        query = request.args.get('search')  # Get the search query parameter
        if query:
            cars = Car.query.filter(Car.name.ilike(f"%{query}%")).all()
        else:
            cars = Car.query.all()
        return jsonify([car.to_dict() for car in cars])
    
    elif request.method == "POST":
        data = request.get_json()
        new_car = Car(
            name=data["name"],
            picture_url=data.get("picture_url"),  
            dealer_id=data["dealer_id"]
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify(new_car.to_dict()), 201

@app.route("/cars/<int:id>", methods=["GET", "DELETE", "PATCH"])
def handle_car(id):
    car = Car.query.get(id)
    if not car:
        return make_response(jsonify({"error": "Car not found"}), 404)

    if request.method == "GET":
        return jsonify(car.to_dict())
    
    elif request.method == "DELETE":
        db.session.delete(car)  # Delete the car
        db.session.commit()  # Commit the deletion to the database
        return "", 204  # Return a 204 No Content response to indicate successful deletion
    
    elif request.method == "PATCH":
        data = request.get_json()
        
        # Update name and picture_url
        if "name" in data:
            car.name = data["name"]
        if "picture_url" in data:
            car.picture_url = data["picture_url"]

        # 🔥 Fix: Update features if provided
        if "feature_ids" in data:
            features = Feature.query.filter(Feature.id.in_(data["feature_ids"])).all()
            car.features = features  # Update the relationship

        db.session.commit()
        return jsonify(car.to_dict()), 200

# --------------------- FEATURES ENDPOINTS ---------------------
@app.route("/features", methods=["GET", "POST"])
def handle_features():
    if request.method == "GET":
        features = Feature.query.all()
        return jsonify([feature.to_dict() for feature in features])
    
    elif request.method == "POST":
        data = request.get_json()
        new_feature = Feature(name=data["name"])
        db.session.add(new_feature)
        db.session.commit()
        return jsonify(new_feature.to_dict()), 201

@app.route("/features/<int:id>", methods=["DELETE"])
def delete_feature(id):
    feature = Feature.query.get(id)
    if feature:
        db.session.delete(feature)
        db.session.commit()
        return "", 204
    return make_response(jsonify({"error": "Feature not found"}), 404)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
