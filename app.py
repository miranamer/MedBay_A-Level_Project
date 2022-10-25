from enum import unique
from flask import Flask, render_template, url_for, flash, jsonify
from flask.templating import render_template_string
from flask import request, redirect
import pickle
from flask_wtf.recaptcha import validators
import numpy as np
import math
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from new_prediction_model import check
import os

# This is the diabetes model that makes a prediction
diab_model = pickle.load(open('diabetes_new.pkl', 'rb'))
heart_model = pickle.load(open('heart_new.pkl', 'rb'))


app = Flask(__name__)




db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin): # User database to store user info like username and password
    id = db.Column(db.Integer, primary_key=True) # primary key
    username = db.Column(db.String(20), nullable=False, unique=True) # username field
    password = db.Column(db.String(80), nullable=False) # password field


class RegisterForm(FlaskForm): # Sign up page form validation
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("Username Already Taken")


class LoginForm(FlaskForm): # login form validation
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")



@app.route('/')
def home():
    return render_template('index.html') # Home Page





@app.route('/diabetes_pre')
def diabetes_pre():
    return render_template('diabetes_page.html') # Before Page For Diabetes

@app.route('/diabetes', methods=['POST', 'GET']) # After Page Diabetes
def diabetes():
    
    if request.method == "POST":

        req = request.form # Input Values From User
        
        Pregnancies = req["Pregnancies"] 
        Glucose = req["Glucose"] 
        BloodPressure = req["BloodPressure"]
        SkinThickness = req["SkinThickness"]
        Insulin = req["Insulin"]
        BMI = req["BMI"]
        DiabetesPedigreeFunction = 0.471876
        Age = req["Age"]

        arr = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]) # Final Array Of User Values
        pred = diab_model.predict(arr)
        pred = np.round(pred[0], 2) * 100
        pred = pred[-1] # Final Prediction
        
        
        
        
        
        
        output = pred

        labels = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        values = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]

        return render_template('diabetes_after.html', output=output, labels=labels, values=values)
        
        
@app.route('/about')
def about():
    return render_template('about.html')


# NOT REALLY NEEDED
@app.route('/background_test')
def background_test():
    return render_template('background_test.html')






@app.route('/heart_disease_test_before')
def heart_disease_test_before():
    return render_template('form_test.html')




@app.route('/heart_disease_test_after', methods=['POST', 'GET'])
def heart_disease_test_after():

    if request.method == "POST":

        req = request.form
        
        age = req["age"]  # Value for age
        sex = req["sex"]  # Value for sex
        cp = req["cp"]    # Value for cp
        trestbps = req["trestbps"]    # Value for trestbps
        chol = req["chol"]  # Value for chol
        fbs = req["fbs"]  # Value for fbs
        restecg = req["restecg"]  # Value for restecg

        thalac = 220 - int(age)

        arr = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, 149.646865, 0.326733, 1.039604, 1.399340, 0.729373, 2.313531]]) # Final Array
        pred = heart_model.predict(arr)
        pred = pred[0]
        output = pred

        labels = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg'] # labels for graph
        values = [age, sex, cp, trestbps, chol, fbs, restecg] # user values in np array 


        


        return render_template('heart_disease_after.html', output=output, labels=labels, values=values, arr=arr)





@app.route('/heart_help')
def heart_help():
    return render_template('heart_help.html')


# Create a help page for the diabetes ai
@app.route('/diabetes_help')
def diabetes_help():
    return render_template('diabetes_help.html')
    

    
    


@app.route('/login', methods=['GET', 'POST']) # login page
def login():
    form = LoginForm()

    if form.validate_on_submit(): # valid credentials checker
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            
            if bcrypt.check_password_hash(user.password, form.password.data): # if hashed user entered password == database password -> allow login
                login_user(user)
                flash('Logged in successfully.') # aler to show successful login
                return redirect(url_for('login'))
        
            else:
                flash('Incorrect Login') # incorrect login
                return redirect(url_for('login'))
        else:
            flash('Incorrect Login') # incorrect login
            return redirect(url_for('login'))



    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    
    

    logout_user()
    flash('Logged Out! - See You Again')
    return redirect(url_for('login'))




@login_manager.unauthorized_handler     
def unauthorized_callback():            
       return redirect(url_for('login'))


@app.route('/success_login')
@login_required
def success_login():
    return render_template('success_login.html')


@app.route('/unsuccessful_login')
def unsuccessful_login():
    return render_template('unsuccessful_login.html')



@app.route('/signup', methods=['GET', 'POST']) # sign up page
def signup():
    form = RegisterForm()
    

    if form.validate_on_submit(): # If sign up credentials are valid
        hashed_password = bcrypt.generate_password_hash(form.password.data) # the hashed password
        new_user = User(username=form.username.data, password=hashed_password) # creates a new login
        db.session.add(new_user) # adds to database
        db.session.commit()
        flash('Account Created!') # verification that it worked
        return redirect(url_for('login')) # redirect to login page

    #else:
       # flash('Something Went Wrong!')
       # return redirect(url_for('login'))

    #message1 = 'User Already Taken!'

    return render_template('signup.html', form=form)



@app.route('/testpage')
def testpage():
    return render_template('testpage.html')



@app.route('/testpage2')
def testpage2():
    return render_template('testpage2.html')


# These below are just for fun -> prob best to remove them from final production or just not upload them to final report.

@app.route('/secret_page_pre')
def secret_page_pre():
    return render_template('secret_page_pre.html')



@app.route('/SECRET_PAGE', methods=['GET', 'POST'])
def SECRET_PAGE():


    if request.method == "POST":

        req = request.form

        secret_passcode = 'BLUEPILL'
        
        sec_code = req['manwqw']

        if sec_code == secret_passcode or sec_code == 'blue pill' or sec_code == 'BLUE PILL' or sec_code == 'blue' or sec_code == 'BLUE':
            return render_template('SECRET_PAGE.html')
        elif sec_code == 'REDPILL' or sec_code == 'red pill' or sec_code == 'RED PILL' or sec_code == 'red' or sec_code == 'RED':
            #flash('THIS PAGE ISNT MEANT FOR YOU! - Leave Now!')
            return render_template('REDPILL.html')
    
    return render_template('secret_page_pre.html')


## EVERYTHING UNDER HERE IS UNDER PROD
# Make sure images are in the images file !!!




APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/skin_disease_pre', methods=["GET", "POST"])
def skin_disease_pre():
    
    return render_template('skin_disease_before.html')


@app.route('/skin_disease_after', methods=["GET", "POST"])
def skin_disease_after():
    target = os.path.join(APP_ROOT, 'static/images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        print(filename)
        dest = '/'.join([target, filename])
        print(dest)
        file.save(dest)

    pred = check(filename)

    return render_template('skin_disease_after.html', pred=pred, image_name=filename)









if __name__ == '__main__':
    app.run(debug=True)
    
    