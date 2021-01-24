from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as C:
    params = json.load(C)['params']
local_server = params['local_server']
app = Flask(__name__)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


class Contact(db.Model):
    sl = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def index():
    return render_template(params['index'], params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')

        entry = Contact(name=name, email=email, phone=phone,
                        date=datetime.now(), msg=msg)

        db.session.add(entry)
        db.session.commit()

    return render_template(params['contact'], params=params)


@app.route("/about")
def about():
    return render_template(params['about'], params=params)


app.run(debug=True)
