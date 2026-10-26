import os
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

bcrypt = Bcrypt(app)

# Importar los controladores para registrar las rutas
from flask_app.controllers import usuarios
from flask_app.controllers import donaciones
