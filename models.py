"""SQLAlchemy models and utility functions for Pet Tracking App"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Create Pet Table
class Pet(db.Model):
    """Pet Tracking Table with ID, Name, and Breed"""
    ID = db.Column(db.Integer, primary_key=True) # ID of the pet as a primary key for sqlite table
    Name = db.Column(db.String(100), nullable=False) # Stores Pet name in sqlite table
    Breed = db.Column(db.String(3), nullable=False) # Stores Pet breed in sqlite table (can be only "dog" or "cat")

    def __repr__(self):
        return "<Pet: {}>".format(self.Name)

    def to_json(self) -> str:
        return

