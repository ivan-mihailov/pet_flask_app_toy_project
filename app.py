import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import db, Pet

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create pet tracking table
    with app.app_context():
        db.create_all()

    @app.route('/')
    def root():
        return render_template("base.html", title='home', pets=Pet.query.all())

    @app.route('/newestpet', methods=['GET'])
    def get_newest_pet():

