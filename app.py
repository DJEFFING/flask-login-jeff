# import os
# from flask import Flask, render_template, url_for,redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, LoginManager, login_user,login_required,logout_user,current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt

# app = Flask(__name__)
# bcrypt = Bcrypt(app = app)
# # Ajoute la configuration de la base de données (exemple avec SQLite)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LoginDatabase.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_login"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config["SECRET_KEY"] = "this_is_secret_key"

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# db = SQLAlchemy(app)


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


# class RegisterForm(FlaskForm):
#     username = StringField(
#         validators=[InputRequired(), Length(min=4, max=20)],
#         render_kw={"placeholder": "Username"},
#     )

#     password = PasswordField(
#         validators=[InputRequired(), Length(min=8, max=20)],
#         render_kw={"placeholder": "Password"},
#     )

#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(username=username.data).first()
#         if existing_user_username:
#             raise ValidationError(
#                 "That username already exists. Please choose a different one."
#             )


# class LoginForm(FlaskForm):
#     username = StringField(
#         validators=[InputRequired(), Length(min=4, max=20)],
#         render_kw={"placeholder": "Username"},
#     )

#     password = PasswordField(
#         validators=[InputRequired(), Length(min=8, max=20)],
#         render_kw={"placeholder": "Password"},
#     )

#     submit = SubmitField("Login")


# @app.route("/")
# def home():
#     return render_template("home.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username = form.username.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password,form.password.data):
#                 login_user(user)
#                 return redirect('dashboad')
        
#     return render_template("login.html", form=form)


# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))



# @app.route("/register", methods= ["GET", "POST"])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data)
#         new_user = User(username = form.username.data, password = hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
    
#     return render_template("register.html", form=form)

# @app.route('/dashboad', methods = ["GET", "POST"] )
# @login_required
# def dashboad():
#     return render_template('dashboad.html')


# if __name__ == "__main__":
#     # with app.app_context():
#     #     # if not os.path.exists("database.db"):
#     #     db.create_all()
#     #     print("Base de données créée !")
#     #     print(db.inspect(db.engine).get_table_names())  # Nouvelle méthode
#     # # print("Base de données créée !")

#     app.run(debug=True)
