from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager,login_required,logout_user,current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt



app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'kipsiele98'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))



class User(db.model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False, unique=True)
    password = db.Column(db.String(40),nullable=False)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"password"})
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError;{"That username already exists"}



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"password"})
    submit = SubmitField('Login')
    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError;{"That username already exists"}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login' , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.routes('/dashboard',methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()



    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)