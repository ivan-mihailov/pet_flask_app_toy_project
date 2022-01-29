import simplejson
from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField

"""Create and configure an instance of the Flask application."""
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petdatabase.db'
app.config['SECRET_KEY'] = 'Test1'  # Flask-WTF requires an encryption key - the string can be anything
app.config['JSON_SORT_KEYS'] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Pet(db.Model):
    """Pet Tracking Table with ID, Name, and Breed"""
    ID = db.Column(db.Integer, primary_key=True)  # ID of the pet as a primary key for sqlite table
    Name = db.Column(db.String(100), nullable=False)  # Stores Pet name in sqlite table
    Breed = db.Column(db.String(3), nullable=False)  # Stores Pet breed in sqlite table (can be only "dog" or "cat")

    def to_json(pet) -> str:
        if isinstance(pet, __builtins__.list):
            pet_schema = PetSchema(many=True)
            output = pet_schema.dump(pet)
            return simplejson.dumps(output)
        else:
            pet_schema = PetSchema()
            output = pet_schema.dump(pet)
            return simplejson.dumps(output)


class PetSchema(ma.Schema):
    class Meta:
        model = Pet
        fields = ("Name", "Breed")


class AddRecord(FlaskForm):
    pet_name = StringField('Pet Name')
    breed_name = RadioField('Breed Name', choices=[('Dog', 'Dog'), ('Cat', 'Cat')])
    submit = SubmitField('Add Record')


class GetName(FlaskForm):
    pet_name = StringField('Pet Name')
    submit = SubmitField('Submit')


db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/newestpet', methods=['GET'])
def newest_pet():
    newest_pet = Pet.query.order_by(Pet.ID.desc()).first()
    if newest_pet:
        message = f"The newest pet in the app is {Pet.to_json(newest_pet)}."
    else:
        message = f"There are no pets currently stored in the app."
    return render_template('newest_pet.html', message=message)


@app.route('/petwithname', methods=['GET', 'POST'])
def pet_with_name():
    form1 = GetName()
    if form1.validate_on_submit():
        pet_name = request.form.get('pet_name')
        pet_with_name = Pet.query.filter_by(Name=pet_name).all()
        message = f"The pets with name {pet_name} are as follows: {Pet.to_json(pet_with_name)}"
        return render_template('pet_with_name.html', form1=form1, message=message)
    else:
        # show validation errors
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('pet_with_name.html', form1=form1)


@app.route('/addpet', methods=['GET', 'POST'])
def add_pet():
    form1 = AddRecord()
    if form1.validate_on_submit():
        pet_name = request.form.get('pet_name')
        breed_name = request.form.get('breed_name')
        pet = Pet(Name=pet_name, Breed=breed_name)
        db.session.add(pet)
        db.session.commit()
        message = f"The data for pet {pet_name} has been submitted."
        return render_template('add_pet.html', form1=form1, message=message)
    else:
        # show validation errors
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_pet.html', form1=form1)


if __name__ == '__main__':
    # db.drop_all() # Uncomment line if you want the database to be purged every time app is started
    db.create_all()
    app.debug = True
    app.run()
