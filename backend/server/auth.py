from .model import User
from main import db
from flask import Blueprint,request, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from flask_cors import cross_origin


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['POST','GET'])
@cross_origin()
def login():
    if request.method == 'POST':
        email = request.json["email"]
        password = request.json["password"]
        user = User.query.filter_by(email = email).first()
        if user:
            print("*******************")
            print(user.__dict__)
            if check_password_hash(user.password,password):
                login_user(user,remember= True)
                return {"status":200, "user": formatUser(user)}
            else:
                return {"status":403, "message": "Incorrect password"}
        else:
            return {"status":403, "message": "No Such Email In our System"}

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/sign_up', methods = ['POST','GET'])

@cross_origin()
def sign_up():
    if request.method == 'POST':
        name = request.json["name"]
        email = request.json["email"]
        pass1 = request.json["password"]
        pass2 = request.json["password2"]
        user = User.query.filter_by(email = email).first()
        if user:
            return {"status":422, "message": "User already exist"}
            
        else:
            new_user = User(name = name, email = email, password = generate_password_hash(pass1,method = 'sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return {"status":200, "user":formatUser(new_user)}
      

def formatUser(user):
    return {
        "id" :user.id,
        "email":user.email,
        "password":user.password,
        "projects": user.projects
    }