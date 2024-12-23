from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort


'''
This is a simple REST API that allows you to create, read, update and delete users.
The API has two endpoints:
    1. /api/users/ - This endpoint allows you to create a new user and get all users.
    2. /api/users/<id> - This endpoint allows you to get, update and delete a user by id.
'''

'''
The UserModel class is a model class that represents the user table in the database.
The class has three columns: id, name and email.
The __repr__ method returns a string representation of the user object.
'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

 
class UserModel(db.Model):
    # This is the user model class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    
    # This method returns a string representation of the user object
    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"
    

# Create the database
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

# Define the fields to be returned in the response
userFields = id = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

# Define the endpoints
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(
            name = args["name"],
            email=args['email']
        )
        db.session.add(user)
        db.session.commit()
        user = UserModel.query.all()
        return user, 201

# Define the endpoints   
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 200
    
        
# Add the endpoints to the api   
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1> Flask Rest API<h1>'

# Run the app
if __name__  == '__main__':
    app.run(debug=True)