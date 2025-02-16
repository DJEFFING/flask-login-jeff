Voici un fichier `README.md` bien structuré pour expliquer comment mettre en place l'authentification dans un projet Flask en utilisant `Flask-Login`.  

---

# 🚀 **Authentification avec Flask-Login**  

Ce projet met en place un **système d'authentification** dans une application Flask en utilisant **Flask-Login**, **Flask-WTF**, **Flask-Bcrypt** et **Flask-SQLAlchemy**.  
L'authentification inclut :  
✅ **Inscription des utilisateurs**  
✅ **Connexion sécurisée avec un mot de passe hashé**  
✅ **Protection des routes avec `@login_required`**  
✅ **Déconnexion des utilisateurs**  

---

## 📌 **1. Installation des dépendances**
Avant de commencer, assure-toi d'avoir **Python 3** installé. Puis, installe les bibliothèques requises avec :

```sh
pip install flask flask-login flask-sqlalchemy flask-wtf flask-bcrypt pymysql
```

### **Explication des bibliothèques :**
| Bibliothèque       | Description |
|--------------------|------------|
| `flask`           | Framework web minimaliste pour Python |
| `flask-login`     | Gestion de l'authentification des utilisateurs |
| `flask-sqlalchemy`| ORM pour interagir avec une base de données |
| `flask-wtf`       | Gestion des formulaires HTML avec WTForms |
| `flask-bcrypt`    | Hashage sécurisé des mots de passe |
| `pymysql`         | Connexion entre Flask et MySQL |

---

## 📌 **2. Configuration du projet**
### **📁 Arborescence du projet**
```
/flask-login-jeff
│── /templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│── app.py
│── config.py
│── models.py
│── forms.py
│── requirements.txt
│── README.md
```

---

## 📌 **3. Configuration de la base de données**
Ce projet utilise **MySQL** (via XAMPP), mais SQLite peut aussi être utilisé.  

### **Créer une base de données MySQL avec XAMPP**
1. Ouvre **XAMPP** et démarre **Apache** et **MySQL**.
2. Accède à **phpMyAdmin** 👉 [http://localhost/phpmyadmin/](http://localhost/phpmyadmin/)
3. Crée une nouvelle base de données nommée `flask_login` :

```sql
CREATE DATABASE flask_login;
```

### **Configuration de la connexion MySQL dans Flask**
Dans `app.py`, configure la connexion à la base de données :

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "this_is_secret_key"
```
> **🔹 Remarque :**  
> - `root` est l'utilisateur MySQL par défaut sous XAMPP.  
> - Il n’y a pas de mot de passe (`""`) par défaut, mais tu peux en définir un.  

---

## 📌 **4. Définition des modèles SQLAlchemy**
Dans `models.py`, nous définissons la table `User` :

```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
```

---

## 📌 **5. Définition des formulaires Flask-WTF**
Dans `forms.py`, nous créons les **formulaires de connexion et d'inscription** :

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Ce nom d'utilisateur existe déjà.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField("Login")
```

---

## 📌 **6. Routes Flask pour l'authentification**
Dans `app.py`, nous définissons les routes :

### **📍 Page d'accueil**
```python
@app.route("/")
def home():
    return render_template("home.html")
```

### **📍 Inscription d'un utilisateur**
```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)
```

### **📍 Connexion d'un utilisateur**
```python
from flask_login import login_user, login_required, logout_user, current_user

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template("login.html", form=form)
```

### **📍 Déconnexion**
```python
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
```

### **📍 Dashboard (Protégé)**
```python
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

---

## 📌 **7. Initialisation de la base de données**
Avant de démarrer l'application, exécute ce script pour créer la base :

```python
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Créer les tables si elles n'existent pas
        print("Base de données initialisée !")
    app.run(debug=True)
```

---

## 📌 **8. Lancer l'application**
Démarre le serveur Flask avec :

```sh
python app.py
```
Ensuite, ouvre ton navigateur et va sur :  
👉 **http://127.0.0.1:5000/**  

---

## 📌 **9. Vérifier la base de données**
Si tu veux voir les utilisateurs inscrits, ouvre MySQL dans **phpMyAdmin**, sélectionne `flask_login`, puis exécute :

```sql
SELECT * FROM user;
```

---

## 🎯 **Conclusion**
✅ Installation des dépendances  
✅ Connexion à MySQL avec SQLAlchemy  
✅ Définition des modèles et formulaires  
✅ Routes pour l'inscription, connexion et déconnexion  
✅ Protection des pages avec `@login_required`  
✅ Gestion des sessions avec `Flask-Login`  

---

## 🎉 **Améliorations possibles**
🔥 Ajout d'un système de rôles (`admin`, `user`)  
🔥 Utilisation de Flask-Mail pour la récupération de mot de passe  
🔥 Intégration avec OAuth (Google, Facebook)  

💬 **Si tu as des questions, n'hésite pas à me demander !** 🚀