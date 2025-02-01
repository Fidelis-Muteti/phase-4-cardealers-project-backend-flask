from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association table for Many-to-Many relationship between cars and features
car_features = db.Table(
    "car_features",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("car_id", db.Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False),
    db.Column("feature_id", db.Integer, ForeignKey("features.id", ondelete="CASCADE"), nullable=False),
)

class Dealer(db.Model, SerializerMixin):
    __tablename__ = "dealers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Relationship: One dealer has many cars
    cars = relationship("Car", back_populates="dealer", cascade="all, delete-orphan")

    # Serialization rules
    serialize_rules = ("-cars.dealer",)

    def __repr__(self):
        return f"<Dealer {self.name}>"

class Car(db.Model, SerializerMixin):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dealer_id = db.Column(db.Integer, ForeignKey("dealers.id", ondelete="CASCADE"), nullable=False)
    picture_url = db.Column(db.String, nullable=True)  # Add picture_url column

    # Relationships
    dealer = relationship("Dealer", back_populates="cars")
    features = relationship("Feature", secondary=car_features, back_populates="cars", cascade="all, delete")

    # Serialization rules
    serialize_rules = ("-dealer.cars", "-features.cars")

    def __repr__(self):
        return f"<Car {self.name}>"

class Feature(db.Model, SerializerMixin):
    __tablename__ = "features"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Many-to-Many Relationship
    cars = relationship("Car", secondary=car_features, back_populates="features")

    # Serialization rules
    serialize_rules = ("-cars.features",)

    def __repr__(self):
        return f"<Feature {self.name}>"
