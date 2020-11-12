"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Expense
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_get():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    return jsonify(users), 200


@app.route('/user/<int:id>', methods=['GET'])
def handle_user(id):
    user = User.query.filter_by(id=id)
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user), 200



@app.route('/user/<int:id>', methods=['PUT'])
def handle_income(id):
    body = request.get_json()
    user = User.query.get(id)
    # user = list(map(lambda x: x.serialize(), user))
    user.income = body["income"]
    db.session.commit()
    user = User.query.filter_by(id=id)
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200




@app.route('/user', methods=['POST'])
def handle_post():
    body = request.get_json()
    user = User(email=body['email'],income=body['income'],user_name=body['userName'] , is_active=body['is_active'])
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(user_name=body['userName'])
     
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200



@app.route('/expense', methods=['POST'])
def post_expense():
    body = request.get_json()
    expense = Expense(label=body['label'],value=body['value'])
    db.session.add(expense)
    db.session.commit()
    expense = Expense.query.all()
     
    expense = list(map(lambda x: x.serialize(), expense))
    return jsonify(expense),200



@app.route('/expense', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expenses = list(map(lambda x: x.serialize(), expenses))
    return jsonify(expenses),200







@app.route('/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense is None: 
        raise APIException("Expense doesnt exists",status_code=404)
    db.session.delete(expense)
    db.session.commit()
    expenses = Expense.query.all()
    expenses = list(map(lambda x: x.serialize(), expenses))
    return jsonify(expenses),200







    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



