


from flask_sqlalchemy import SQLAlchemy


db = 10
UserMixin =10
FlaskForm=10
StringField=10
PasswordField = 10
InputRequired=10
Length=20
SubmitField=20
ValidationError=20
app = 20
def Bcrypt():
    pass

SQLAlchemy=20
def LoginManager():
    pass
User = 20

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



class DatabaseInit(db.Model, UserMixin): # User database to store user info like username and password
    id = db.Column(db.Integer, primary_key=True) # primary key
    User_username = db.Column(db.String(25), nullable=False, unique=True) # username field
    User_password = db.Column(db.String(80), nullable=False) # password field


class SignUpFunction(FlaskForm): # Sign up page form validation
    User_username = StringField(validators=[InputRequired(), Length(min=1, max=25)], render_kw={"placeholder": "Username"})
    User_password = PasswordField(validators=[InputRequired(), Length(min=1, max=25)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = DatabaseInit.query.filter_by(username=username.data).first() # Check if user in db

        if existing_user_username:
            raise ValidationError("Username Already Taken")


class LoginFunction(FlaskForm): # login form validation
    User_username = StringField(validators=[InputRequired(), Length(min=1, max=25)], render_kw={"placeholder": "Username"})
    User_password = PasswordField(validators=[InputRequired(), Length(min=1, max=25)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")